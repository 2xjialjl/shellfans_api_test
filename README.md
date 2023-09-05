# Shellfans API Documentation

Welcome to Shellfans API documentation. This document provides information about Shellfans API.

## Check Email

- **Endpoint:** `/api/check_email/`
- **HTTP Method:** POST
- **Description:** This endpoint is used to check if an email address is already registered in the system.

### Request

- **URL:** `/api/check_email/`
- **Request Headers:**
  - `Authorization: Token YOUR_API_TOKEN` (Authentication required)
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
  }
### Responses
- **Status Codes:
200 OK: The email address does not exist in the system.**
    ```json
      {
        "result":true,"message":"Email does not exist","data":{"code":200}
      }
     ```
- **400 Bad Request: The email address already exists or there is another request error.**
    ```json
      {
        "result":true,"message":"Email already exists","data":{"code":400}
      }
    ```


## Check Phone

- **Endpoint:** `/api/check_phone/`
- **HTTP Method:** POST
- **Description:** This endpoint is used to check if a phone number is already registered in the system and sends an SMS verification code.

### Request

- **URL:** `/api/check_phone/`
- **Request Body:**
  ```json
  {
    "phone_number": "1234567890"
  }
  
### Responses
- **Status Codes:
200 OK:  The phone number does not exist in the system, and the verification code has been sent.**
    ```json
      {
        "result":true,"message":"Sending SMS successfully","data":{"code":200}
      }
     ```
- **400 Bad Request: The phone number already exists**
    ```json
      {
        "result":true,"message":"Phone Number already exists","data":{"code":400}
      }
    ```
- **500 INTERNAL_SERVER_ERROR:  Failed to send the SMS or other server-related errors.**
    ```json
      {
        "result":true,"message":"Sending SMS error","data":{"code":500}
      }
    ```

## Verify and Register User

- **Endpoint:** `/api/verify_and_register_user/`
- **HTTP Method:** POST
- **Description:** This endpoint is used to verify a user's identity with a verification code and register a new user in the system.

### Request

- **URL:** `/api/verify_and_register_user/`
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "name": "jason",
    "gender": "Male",
    "birthday": "1996-01-17",
    "phone_number": "1234567890",
    "verification_code": "123456"
  }
  
### Responses
- **Status Codes:
200 OK:  User registration and verification were successful.**
    ```json
      {
       "result":true,"message":"Successfully registered","data":{"code":200}
      }
     ```
- **400 Bad Request: User already exists**
    ```json
      {
        "result":false,"message":"Email or Phone Number already exists","data":{"code":400}
      }
    ```
- **400 Bad Request: catch dont have data.**
    ```json
      {
        "result":false,"message":"Verification code not found or has expired","data":{"code":400}
      }
    ```
- **400 Bad Request: Invalid verification code.**
    ```json
      {
       "result":false,"message":"Invalid verification code","data":{"code":400}
      }
    ```
- **400 Verification code has expired.**
    ```json
      {
        "result":false,"message":"Verification code has expired","data":{"code":400}
      }
    ```