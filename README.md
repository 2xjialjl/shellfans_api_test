# Shellfans API Documentation

Welcome to Shellfans API documentation. This document provides information about Shellfans API.

## register_email_or_phone

- **Endpoint:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/register_email_or_phone/`
- **HTTP Method:** POST
- **Description:** This endpoint is used to check if an email address is already registered in the system.

### Request

- **URL:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/register_email_or_phone/`
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
- **you can input phone or email**
  ```json
  {
    "account": "user@example.com",
  }
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
- **Request Body:**
- - **you can input phone or email**
  ```json
  {
    "account": "09123456789"
    "verification_code" "123456"
  }
  
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
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
    "name" "jason"
    "third_party_registration_source":"0"
  }
- **explain data:**
  ```json
  {
    "third_party_registration_source": "0(normal)",
    "third_party_registration_source": "1(Google)",
    "third_party_registration_source": "2(FB)"
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
    "Authorization": "uxsdsFSD200.sddsfDSVZX"
  }
### Request

- **URL:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/get_user_info/`
- **Request Headers:**
  - `Authorization: YOUR_API_TOKEN`
- **explain data:**
  ```json
  {
    "name": "user name",
    "email": "user email",
    "gender": "user gender",
    "birthday": "user birthday",
    "phone_number": "user phone_number",
    "profile_picture": "user headshot",
    "level": "0(normal)",
    "level": "1(免費會員)",
    "level": "2(高級會員)",
    "level": "3(頂級會員)",
    "is_email_verified": "true(email已驗證)",
    "is_email_verified": "false(email未驗證)",
    "is_phone_verified": "true(phone已驗證)",
    "is_phone_verified": "false(phone未驗證)",
    "third_party_registration_source": "0(normal)",
    "third_party_registration_source": "1(Google)",
    "third_party_registration_source": "2(FB)",
    "backup_email": "if third_party_registration_source email is not use, user can add  backup_email.",
    "is_backup_email_verified": "true(email已驗證)",
    "is_backup_email_verified": "false(email未驗證)",
    "security_code": "download bill details password, The security code consists of a combination of 4 alphanumeric characters."
  }
### Responses
- **Status Codes:200 OK: Verification code is valid.**
    ```json
      {
        "result":true,"message":"User information retrieved successfully","data":{"name":"jackssd1232","email":"jason.huang@shell.fans","gender":"男","birthday":"1996-01-17","phone_number":null,"profile_picture":"","level":0,"is_email_verified":true,"is_phone_verified":false,"third_party_registration_source":null,"backup_email":null,"is_backup_email_verified":false,"security_code":null}
      }
     ```
- **500 Bad Request: DB server error.**
    ```json
      {
        "result":true,"message":"Token error","data":{"code":500}
      }
    ```
  
## edit_profiles

- **Endpoint:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/edit_profiles/`
- **HTTP Method:** PUT
- **Description:** This api is edit user data EX:name,gender,security_code.

### Request

- **URL:** ` https://shellfans-api-test-rr7tb4kqva-de.a.run.app/api/edit_profiles/`
- **Request Headers:**
  ```json
  {
    "Authorization": "uxsdsFSD200.sddsfDSVZX"
  }
- **Request Body:**
  ```json
  {
    "name": "user@example.com"
    "gender": "0"
    "security_code":"EX18"
  }
- **explain data:**
  ```json
  {
    "name": "user name",
    "gender": "0(男)",
    "gender": "1(女)",
    "gender": "2(不透露)",
    "security_code": "The security code consists of a combination of 4 alphanumeric characters."
  }
### Responses
- **Status Codes:200 OK: Verification code is valid.**
    ```json
      {
        "result":true,"message":"User registration successful","data":{"code":200}
      }
     ```
- **500 Bad Request: DB server error.**
    ```json
      {
        "result":true,"message":"DB server error","data":{"code":500}
      }
    ```
## edit_profiles_sent_verification_code

- **Endpoint:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/edit_profiles_sent_verification_code/`
- **HTTP Method:** POST
- **Description:** This is to send a login verification code.

### Request

- **URL:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/edit_profiles_sent_verification_code/`
- **you can input phone or email**
  ```json
  {
    "account": "user@example.com",
  }
  {
    "account": "09123456789",
    "country_code":"TW"
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
## edit_profiles

- **Endpoint:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/edit_profiles/`
- **HTTP Method:** POST
- **Description:** This is to send a login verification code.

### Request

- **URL:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/edit_profiles/`
- **you can input phone or email**
  ```json
  {
    "name": "jason",
    "gender":"0",
    "email":"jsaiok@example.com",
    "backup_email":"jsaiok@example.com",
    "verification_codes":"123456",
    "security_code":"security_code",
    "profile_picture":"base64"
  }
### Responses
- **Status Codes:
200 OK: edit_profiles is successfully.**
    ```json
      {
        "result":true,"message":"edit_profiles is successfully","data":{"code":200}
      }
     ```
- **400 Bad Request: Verification code has expired.**
    ```json
      {
        "result":true,"message":"Verification code has expired","data":{"code":400}
      }
    ```
- **400 Bad Request: Email is empty.**
    ```json
      {
        "result":true,"message":"Email is empty","data":{"code":400}
      }
    ```
  ## refresh_token

- **Endpoint:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/refresh_token/`
- **HTTP Method:** POST
- **Description:** This is to refresh_token.

### Request

- **URL:** `https://shellfans-api-test-rr7tb4kqva-uc.a.run.app/api/refresh_token/`
- **you can input token**
  ```json
  {
    "Authorization": "Bearer eyJhbGciOiJI",

  }
### Responses
- **Status Codes:
200 OK: edit_profiles is successfully.**
    ```json
      {
        "result":true,"message":"Token refresh successful","data":{"code":200,"token":"eyJhbG"}
      }
     ```
- **400 Bad Request: Verification code has expired.**
    ```json
      {
        "result":true,"message":"Token refresh failed","data":{"code":400}
      }
    ```