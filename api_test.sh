#!/bin/bash

# Base API endpoint URL
url="http://localhost:5000/api"


# Function to perform a POST request
execute_post_request() {
    endpoint=$1
    data=$2
    response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$url$endpoint" -H "Content-Type: application/json" -d "$data")
    echo $response
}

# Function to perform a GET request
execute_get_request() {
    endpoint=$1
    token=$2
    response=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$url$endpoint" -H "Authorization: Bearer $token")
    echo $response
}

# Test Signup
echo "Testing Signup..."
signup_response=$(execute_post_request "/signup" '{"username":"user","email":"user@example.com","password":"password123456"}')
if [ "$signup_response" == "200" ] || [ "$signup_response" == "400" ]; then
    echo "PASS: Signup test completed with response code: $signup_response"
else
    echo "FAIL: Signup test failed with response code: $signup_response"
fi

# Test Login and retrieve token
echo "Testing Login..."
login_response=$(execute_post_request "/login" '{"username":"user","password":"password123456"}')
if [ "$login_response" == "200" ]; then
    echo "PASS: Login test completed with response code: $login_response"
else
    echo "FAIL: Login test failed with response code: $login_response"
    exit 1
fi

# Wait for user input before closing
read -p "Press Enter to close..."
