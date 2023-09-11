# Shellfans API Documentation

Welcome to Shellfans API documentation. This document provides information about Shellfans API.

## Check Email

- **Endpoint:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/check_email/`
- **HTTP Method:** POST
- **Description:** This endpoint is used to check if an email address is already registered in the system.

### Request

- **URL:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/check_email/`
- **Request Headers:**
  - `Authorization: Token YOUR_API_TOKEN` (Authentication required)
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
  }
### Responses
- **Status Codes:200 OK: Sending email successfully.**
    ```json
      {
        "result":true,"message":"Sending email successfully","data":{"code":200}
      }
     ```
- **500 Bad Request: Email or phone has be registered.**
    ```json
      {
        "result":true,"message":"Email or phone has be registered","data":{"code":400}
      }
     ```
- **500 Bad Request: Email or Database server error.**
    ```json
      {
        "result":true,"message":"Email or Database server error","data":{"code":500}
      }
    ```


## Check Phone

- **Endpoint:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/check_phone/`
- **HTTP Method:** POST
- **Description:** This endpoint is used to check if a phone number is already registered in the system and sends an SMS verification code.

### Request

- **URL:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/check_phone/`
- **Request Body:**
  ```json
  {
    "phone_number": "+88693960123"
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

- **Endpoint:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/verify_register_user//`
- **HTTP Method:** POST
- **Description:** This endpoint is used to verify a user's identity with a verification code and register a new user in the system.

### Request

- **URL:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/verify_register_user//`
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "name": "jason",
    "gender": "0",
    "birthday": "1996-01-17",
    "phone_number": "+886123456789",
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
## Login Email

- **Endpoint:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/send_login_email/`
- **HTTP Method:** POST
- **Description:** This is to send a login email verification code.

### Request

- **URL:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/send_login_email/`
- **Request Headers:**
  - `Authorization: Token YOUR_API_TOKEN` (Authentication required)
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
  }
### Responses
- **Status Codes:
200 OK: Sending email successfully.**
    ```json
      {
        "result":true,"message":"Sending email successfully","data":{"code":200}
      }
     ```
- **400 Bad Request: The email address is not exist in the system.**
    ```json
      {
        "result":true,"message":"Email does not exist","data":{"code":400}
      }
    ```
- **500 Bad Request: The email address server error.**
    ```json
      {
        "result":true,"message":"Email server error","data":{"code":400}
      }
    ```
## Confirm Email Verification Code

- **Endpoint:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/check_login_email/`
- **HTTP Method:** POST
- **Description:** This is confirm email verification code.

### Request

- **URL:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/check_login_email/`
- **Request Headers:**
  - `Authorization: Token YOUR_API_TOKEN` (Authentication required)
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "verification_code": "123456"
  }
### Responses
- **Status Codes:
200 OK: Successfully login.**
    ```json
      {
        "result":true,"message":"Successfully login","data":{"code":200}
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
- **500 Bad Request: The email address server error.**
    ```json
      {
        "result":true,"message":"Email server error","data":{"code":400}
      }
    ```