public class SeleniumIntro {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		// invoking drivers
		// Chrome - ChromeDriver -> methods close, get
		// FireFox - FireFoxDriver -> methods close,get
		// Safari - SafariDriver -> methods close,get
		// WebDriver methods + methods
		
		//turns off selenium manager (needed here for permission error)
		System.setProperty("webdriver.chrome.driver","/C:\\Program Files (x86)\\Google\\ChromeDriver\\chromedriver.exe");
		//creates object of chromedriver using webdriver interface
		WebDriver driver = new ChromeDriver();	
		
		// Firefox launch
        // WebDriver driver1 = new FirefoxDriver();
		// turns off selenium manager (needed here for permission error)
        // System.setProperty("webdriver.gecko.driver","/C:\\Program Files (x86)\\firefox\\geckodriver\\geckodriver.exe");
		
		// MS Edge launch
        // WebDriver driver2 = new EdgeDriver();
		// turns off selenium manager (needed here for permission error)
        // System.setProperty("webdriver.edge.driver","/C:\\Program Files (x86)\\edge\\edgedriver\\edgedriver.exe");
		
		//get request to desired website url
		driver.get("https://go0.cdxms.acpt-etss.aws.fanniemae.com/#/asset-list");
		System.out.println(driver.getCurrentUrl());
		System.out.println(driver.getTitle());
		// closes browser
		driver.close();
	}//end of main

}//end of class
