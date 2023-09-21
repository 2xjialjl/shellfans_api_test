# Shellfans API Documentation

Welcome to Shellfans API documentation. This document provides information about Shellfans API.

## register_email_or_phone

- **Endpoint:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/register_email_or_phone/`
- **HTTP Method:** POST
- **Description:** This endpoint is used to check if an email address is already registered in the system.

### Request

- **URL:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/register_email_or_phone/`
- **Request Headers:**
  - `Authorization: Token YOUR_API_TOKEN` (Authentication required)
- **Request Body:**
- - **if your input is phone**
  ```json
  {
    "phone_number": "09123456789"
    "country_code" "TW"
  }
- - **if your input is email**
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
- **400 Bad Request: Email and phone are both empty.**
    ```json
      {
        "result":true,"message":"Email and phone are both empty","data":{"code":400}
      }
     ```
- **500 Bad Request: Email,Phone,Database server error.**
    ```json
      {
        "result":true,"message":"SMS server error","data":{"code":500}
      }
    ```
## check_register_verification_code

- **Endpoint:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/check_register_verification_code/`
- **HTTP Method:** POST
- **Description:** This endpoint is used to check if an email address is already registered in the system.

### Request

- **URL:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/check_register_verification_code/`
- **Request Headers:**
  - `Authorization: Token YOUR_API_TOKEN` (Authentication required)
- **Request Body:**
- - **if your input is phone**
  ```json
  {
    "phone_number": "09123456789"
    "verification_code" "123456"
  }
- - **if your input is email**
  ```json
  {
    "email": "user@example.com"
    "verification_code" "123456"
  }
### Responses
- **Status Codes:200 OK: Verification code is valid.**
    ```json
      {
        "result":true,"message":"Verification code is valid","data":{"code":200}
      }
     ```
- **400 Bad Request: Verification code has expired.**
    ```json
      {
        "result":true,"message":"Verification code has expired","data":{"code":400}
      }
     ```
- **400 Bad Request: Email verification code has expired.**
    ```json
      {
        "result":true,"message":"Email verification code has expired","data":{"code":400}
      }
    ```
## register_user

- **Endpoint:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/register_user/`
- **HTTP Method:** POST
- **Description:** This endpoint is used to verify a user's identity register a new user in the system.

### Request

- **URL:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/register_user/`
- **Request Body:**
- **if your input is email**
  ```json
  {
    "email": "user@example.com",
    "name": "jason",
    "gender": "0",
    "birthday": "1996-01-17",
  }
- **if your input is phone**
  ```json
  {
    "phone_number": "09123456789",
    "country_code": "TW",
    "name": "jason",
    "gender": "0",
    "birthday": "1996-01-17",
  }
### Responses
- **Status Codes:
200 OK:  User registration and verification were successful.**
    ```json
      {
       "result":true,"message":"Successfully registered","data":{"code":200,"token":"abc3.5n"}
      }
     ```
- **500 Bad Request: DB server error.**
    ```json
      {
        "result":false,"message":"DB server error","data":{"code":500}
      }
    ```
## login_email_or_phone

- **Endpoint:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/login_email_or_phone/`
- **HTTP Method:** POST
- **Description:** This is to send a login verification code.

### Request

- **URL:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/login_email_or_phone/`
- **Request Headers:**
  - `Authorization: Token YOUR_API_TOKEN` (Authentication required)
- **you can input phone or email**
  ```json
  {
    "account": "user@example.com",
  }

  ```json
  {
    "account": "09123456789",
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
## check_login_verification_code

- **Endpoint:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/check_login_verification_code/`
- **HTTP Method:** POST
- **Description:** This endpoint is used to check if an email address is already registered in the system.

### Request

- **URL:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/check_login_verification_code/`
- **Request Headers:**
  - `Authorization: Token YOUR_API_TOKEN` (Authentication required)
- **Request Body:**
- - **you can input phone or email**
  ```json
  {
    "account": "09123456789"
    "verification_code" "123456"
  }

  ```json
  {
    "account": "user@example.com"
    "verification_code" "123456"
  }
### Responses
- **Status Codes:200 OK: Verification code is valid.**
    ```json
      {
        "result":true,"message":"Verification code is valid","data":{"code":200,"token":"abc3.5n"}
      }
     ```
- **400 Bad Request: Verification code has expired.**
    ```json
      {
        "result":true,"message":"Verification code has expired","data":{"code":400}
      }
     ```
- **400 Bad Request: Email verification code has expired.**
    ```json
      {
        "result":true,"message":"Email verification code has expired","data":{"code":400}
      }
    ```

## quick_registration

- **Endpoint:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/quick_registration/`
- **HTTP Method:** POST
- **Description:** This endpoint is used to check if an email address is already registered in the system.

### Request

- **URL:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/quick_registration/`
- **Request Headers:**
  - `Authorization: Token YOUR_API_TOKEN` (Authentication required)
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
    "name" "jason"
    "third_party_registration_source":"0"
  }
### Responses
- **Status Codes:200 OK: Verification code is valid.**
    ```json
      {
        "result":true,"message":"User registration successful","data":{"code":200,"token":"abc3.5n"}
      }
     ```
- **500 Bad Request: DB server error.**
    ```json
      {
        "result":true,"message":"DB server error","data":{"code":500}
      }
    ```
## get_user_info

- **Endpoint:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/get_user_info/`
- **HTTP Method:** GET
- **Description:** Use token to get userinfo.
- **Request Header:**
  ```json
  {
    "Authorization": "uxsdsFSD200.sd"
### Request

- **URL:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/get_user_info/`
- **Request Headers:**
  - `Authorization: Token YOUR_API_TOKEN` (Authentication required)
### Responses
- **Status Codes:200 OK: Verification code is valid.**
    ```json
      {
        "result":true,"message":"User information retrieved successfully","data":{}
      }
     ```
- **500 Bad Request: DB server error.**
    ```json
      {
        "result":true,"message":"Token error","data":{"code":500}
      }
    ```