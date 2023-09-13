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
  ```json
  {
    "email": "user@example.com"
    "phone_number": "09123456789"
    "country_code" "TW"
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
  ```json
  {
    "email": "user@example.com"
    "phone_number": "09123456789"
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
       "result":true,"message":"Successfully registered","data":{"code":200}
      }
     ```
- **500 Bad Request: DB server error.**
    ```json
      {
        "result":false,"message":"DB server error","data":{"code":500}
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