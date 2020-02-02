package com.springws.demo.controller;

import javax.validation.Valid;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import springws.demo.model.request.UserDetailsRequestModel;
import springws.demo.model.response.UserModel;

@RestController 

@RequestMapping("/users") //http://localhost:8080/users

public class UserController {
	
@GetMapping
	public String getUser(@RequestParam(value="page", defaultValue="1")int page,
			@RequestParam(value="limit", defaultValue="50") int limit, 
			@RequestParam(value="sort", defaultValue="desc" ) String sort){
		
		//if (sort != null) {
		return "get user was called with with params of" +  " Page = " + page + ", Limit = " + limit + " and sort = "+ sort;
//		}//closes if
//		else {
//			return "get user was called with with params of" +  " Page = " + page + ", Limit = " + limit;
//		}//closes else
		}//closes getUser
	
@GetMapping(path="/{userId}",
	produces = { MediaType.APPLICATION_XML_VALUE, 
				 MediaType.APPLICATION_JSON_VALUE
				})
	
	public ResponseEntity<UserModel> getUser(@PathVariable String userId) {
		UserModel returnValue = new UserModel();
		returnValue.setEmail("test@test.com");
		returnValue.setFirstName("Jhuan");
		returnValue.setLastName("Pressley");
		//returnValue.setUserId("123456789");
		
		return new ResponseEntity<UserModel>( returnValue, HttpStatus.OK);
 		
	}//closes getUser

@PostMapping (
		consumes = { 
				MediaType.APPLICATION_XML_VALUE, 
		 		MediaType.APPLICATION_JSON_VALUE},
		produces = { 
				MediaType.APPLICATION_XML_VALUE, 
				MediaType.APPLICATION_JSON_VALUE
		})

	public ResponseEntity<UserModel> createUser(@Valid @RequestBody UserDetailsRequestModel userDetails) 
	{
		
		UserModel returnValue = new UserModel();
		returnValue.setEmail(userDetails.getEmail());
		returnValue.setFirstName(userDetails.getFirstname());
		returnValue.setLastName(userDetails.getLastname());
	
	
	return new ResponseEntity<UserModel>( returnValue, HttpStatus.OK);
	
	}//closes create user

@PutMapping
	public String putUser() {
		return "put user was called";
	}//closes put

@DeleteMapping
	public String deleteUser() {
		return "delete user was called";
	}//closes delete user

}//closes main method
