import json
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

import xlwt
import sys
sys.path.append('../../')

from dt_api_security_results.client import ApiSecurityResultsClient, AssetGroupField, AssetTagAppliedToAssetField
from dt_api_security_results.models.assets import ApiOperation, DiscoveredViaEnum
from dt_api_security_results.models.policy_violations import AssetTypeEnum, PolicyViolationAffectingAsset, SeverityEnum


@dataclass
class ExportedViolationRow:
    asset_url: Optional[str]
    asset_aws_arn: Optional[str]
    violation_uuid: UUID
    title: str
    severity: SeverityEnum
    affected_asset_name: str
    affected_asset_type: str
    affected_asset_cloud_console_url: Optional[str]
    description: str
    additional_information: Optional[str]
    recommendation: str
    date_discovered: datetime

    @property
    def violation_portal_url(self) -> str:
        return f"https://www.securetheorem.com/api/inspect/policy-violations/{self.violation_uuid}"


@dataclass
class ExportedAssetRow:
    asset_uuid: UUID
    name: str
    url: Optional[str]
    asset_type: str
    asset_type_icon_url: str
    asset_type_name: str
    belongs_to_asset_group: Optional[AssetGroupField]

    open_urgent_policy_violations_count: int
    open_important_policy_violations_count: int
    open_proactive_policy_violations_count: int

    discovered_via: str
    discovered_via_icon_url: str
    discovered_via_name: str

    hosted_on: str
    hosted_on_icon_url: str
    hosted_on_name: str

    status: str
    date_created: datetime
    date_no_longer_accessible: Optional[datetime]

    tags: List[AssetTagAppliedToAssetField]

    violations: List[PolicyViolationAffectingAsset]

    api_operations: Optional[List[ApiOperation]]

    @property
    def asset_portal_url(self) -> str:
        return f"https://www.securetheorem.com/api/inspect/assets/{self.asset_uuid}"


def fetch_all_violations_affecting_asset(
    client: ApiSecurityResultsClient, asset_id: UUID, cursor: Optional[str]
) -> List[PolicyViolationAffectingAsset]:
    all_violations = []
    while True:
        violation_response = client.policy_violations_affecting_asset_list(id=asset_id, cursor=cursor)
        print(f"Fetched {len(violation_response.policy_violations)} policy violations")

        # Make the data easy to query
        all_violations.extend(violation_response.policy_violations)

        cursor = violation_response.pagination_information.next_cursor
        if not cursor:
            # We went through all the pages; all done here
            break

    return all_violations


def fetch_all_api_operations_of_restful_api(
    client: ApiSecurityResultsClient, restful_api_id: UUID
) -> List[ApiOperation]:
    restful_api_response = client.restful_apis_get(id=restful_api_id)
    print("Fetched api operations")

    return restful_api_response.restful_apis[0].api_operations


def retrieve_assets(
    api_key: str,
    filter_by_asset_tags: Optional[Dict[str, Optional[List[str]]]] = None,
    filter_by_text: Optional[str] = None,
    filter_by_asset_types: Optional[List[AssetTypeEnum]] = None,
    filter_by_discovered_vias: Optional[List[DiscoveredViaEnum]] = None,
) -> List[ExportedAssetRow]:  # noqa: C901 (complexity)
    client = ApiSecurityResultsClient(api_key=api_key)
    print("Fetching all assets")
    cursor = None

    # We have to go through all the pages
    all_assets = []
    while True:

        response = client.assets_list(
            cursor=cursor,
            filter_by_asset_tags=filter_by_asset_tags,
            filter_by_text=filter_by_text,
            filter_by_asset_types=filter_by_asset_types,
            filter_by_discovered_vias=filter_by_discovered_vias,
        )
        print(f"Fetched {len(response.assets)} assets")

        # Make the data easy to query
        all_assets.extend(response.assets)

        cursor = response.pagination_information.next_cursor
        if not cursor:
            # We went through all the pages; all done here
            break

    exported_assets = []
    for asset in all_assets:
        violations = fetch_all_violations_affecting_asset(client=client, asset_id=asset.id, cursor=cursor)
        if asset.asset_type == "RESTFUL_API":
            api_operations = fetch_all_api_operations_of_restful_api(client=client, restful_api_id=asset.id)
        else:
            api_operations = None

        exported_assets.append(
            ExportedAssetRow(
                asset_uuid=asset.id,
                name=asset.name,
                url=asset.url,
                asset_type=asset.asset_type,
                asset_type_icon_url=asset.asset_type_icon_url,
                asset_type_name=asset.asset_type_name,
                belongs_to_asset_group=asset.belongs_to_asset_group,
                open_urgent_policy_violations_count=asset.open_urgent_policy_violations_count,
                open_important_policy_violations_count=asset.open_important_policy_violations_count,
                open_proactive_policy_violations_count=asset.open_proactive_policy_violations_count,
                discovered_via=asset.discovered_via,
                discovered_via_icon_url=asset.discovered_via_icon_url,
                discovered_via_name=asset.discovered_via_name,
                hosted_on=asset.hosted_on,
                hosted_on_icon_url=asset.hosted_on_icon_url,
                hosted_on_name=asset.hosted_on_name,
                status=asset.status,
                date_created=asset.date_created,
                date_no_longer_accessible=asset.date_no_longer_accessible,
                tags=asset.tags,
                violations=violations,
                api_operations=api_operations,
            )
        )

    return exported_assets


def make_argument_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("api_key")
    return parser


#adding some automation to the filename and filter enum
def make_choice():
    global DiscVia
    global xlsName
    sel= input('Which "DiscoveredVia" you like to pull? RE/reverse eng, WC/Web crawler, MI/Manual Import, AWS/Amazon Web Services? (enter anything else to bypass)')
    if sel.upper() == "RE":
        DiscVia= "WEB_APPLICATION_SCANS"
        xlsName= "exported_assetsRE.xls"
        return DiscVia, xlsName
    elif sel.upper() == "WC":
        DiscVia= "WEBSITE_CRAWLER"
        xlsName= "exported_assetsWC.xls"
        return DiscVia, xlsName
    elif sel.upper() == "AWS":
        DiscVia= "AMAZON_WEB_SERVICES"
        xlsName= "exported_assetsAWS.xls"
        return DiscVia, xlsName
    elif sel.upper() == "MI":
        DiscVia= "MANUAL_IMPORT"
        xlsName= "exported_assetsMI.xls"
        return DiscVia, xlsName
    else: 
        print('bypassed')
        pass


def main() -> None:
    make_choice()
    args = make_argument_parser().parse_args()
    xls_file = xlsName 

    # MODIFY FILTERS HERE
    exported_assets = retrieve_assets(
        args.api_key,
        # filter_by_asset_tags={"lifecycle": ["prod"]},
        # filter_by_asset_types=[AssetTypeEnum("RESTFUL_API")],  # uncomment to only show restful apis
        # filter_by_text="prod",  # uncomment to filter by keywords
        # note: see other accepted string enum values in the comment section where DiscoveredViaEnum is defined
        filter_by_discovered_vias=[DiscoveredViaEnum(DiscVia)]
    )

    print(f"Dumping {len(exported_assets)} to {xls_file}...")

    book = xlwt.Workbook()
    sheet = book.add_sheet("Assets")

    sheet.write(0, 0, "Unique ID")
    sheet.write(0, 1, "Asset Type")
    sheet.write(0, 2, "Asset Name")
    sheet.write(0, 3, "Asset Url")
    sheet.write(0, 4, "Open Important Policy Violations Count")
    sheet.write(0, 5, "Open Proactive Policy Violations Count")
    sheet.write(0, 6, "Open Urgent Policy Violations Count")
    sheet.write(0, 7, "Hosted On")
    sheet.write(0, 8, "Discovered Via")
    sheet.write(0, 9, "Status")
    sheet.write(0, 10, "Discovery Date")
    sheet.write(0, 11, "Asset Tags")
    sheet.write(0, 12, "Policy Violation Titles & Severity (combined)")
    # sheet.write(0, 13, "Policy Violation info (json)")
    sheet.write(0, 13, "API Operations (if applicable)")

    for index, asset_row in enumerate(exported_assets, start=1):
        violations_combined_info = []
        for v in asset_row.violations:
            violations_combined_info.append(
                {
                    # "id": str(v.id),
                    # "title": v.violated_policy_rule.policy_rule_type.title,
                    "severity": v.violated_policy_rule.relevance,
                }
            )

        sheet.write(index, 0, str(asset_row.asset_uuid))
        sheet.write(index, 1, str(asset_row.asset_type))
        sheet.write(index, 2, str(asset_row.name))
        sheet.write(index, 3, str(asset_row.url))
        sheet.write(index, 4, str(asset_row.open_important_policy_violations_count))
        sheet.write(index, 5, str(asset_row.open_proactive_policy_violations_count))
        sheet.write(index, 6, str(asset_row.open_urgent_policy_violations_count))
        sheet.write(index, 7, str(asset_row.hosted_on))
        sheet.write(index, 8, str(asset_row.discovered_via_name))
        sheet.write(index, 9, str(asset_row.status))
        sheet.write(index, 10, str(asset_row.date_created))
        sheet.write(index, 11, str({o.tag: o.value for o in asset_row.tags}))
        sheet.write(
            index, 12, ",\n".join({v.violated_policy_rule.policy_rule_type.title +" Severity: " +v.violated_policy_rule.relevance+"\r\n " for v in asset_row.violations})
        ),
        # sheet.write(index, 13, json.dumps(violations_combined_info)),
        sheet.write(
            index,
            13,
            "\n".join(f"{op.http_method} at {op.path}" for op in asset_row.api_operations)
            if asset_row.api_operations
            else "",
        ),

    book.save(xls_file)
    print("All done!")


if __name__ == "__main__":
    main()
