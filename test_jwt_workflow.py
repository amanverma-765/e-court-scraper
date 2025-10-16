#!/usr/bin/env python3
"""
Test script to demonstrate the new JWT workflow.
This script shows how to:
1. Generate a JWT token
2. Use the token to make authenticated requests
"""

import httpx
import json

BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_response(response):
    """Pretty print the response."""
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response Text: {response.text}")


def test_jwt_workflow():
    """Test the complete JWT workflow."""
    
    with httpx.Client() as client:
        # Step 1: Generate JWT Token
        print_section("Step 1: Generate JWT Token")
        print(f"POST {BASE_URL}/auth/token")
        
        try:
            response = client.post(f"{BASE_URL}/auth/token")
            print_response(response)
            
            if response.status_code == 200:
                token = response.json()["data"]["token"]
                print(f"\n✅ Token generated successfully!")
                print(f"Token: {token[:50]}...")
            else:
                print("\n❌ Failed to generate token")
                return
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return
        
        # Step 2: Test request WITHOUT token (should fail)
        print_section("Step 2: Test Request WITHOUT Token (Expected to Fail)")
        print(f"GET {BASE_URL}/court/states")
        print("Authorization: (none)")
        
        try:
            response = client.get(f"{BASE_URL}/court/states")
            print_response(response)
            
            if response.status_code == 401:
                print("\n✅ Correctly rejected request without token")
            else:
                print("\n⚠️  Unexpected response")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        # Step 3: Test request WITH token (should succeed)
        print_section("Step 3: Test Request WITH Token (Expected to Succeed)")
        print(f"GET {BASE_URL}/court/states")
        print(f"Authorization: Bearer {token[:20]}...")
        
        try:
            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = client.get(f"{BASE_URL}/court/states", headers=headers)
            print_response(response)
            
            if response.status_code == 200:
                print("\n✅ Successfully retrieved states with token!")
            else:
                print("\n❌ Failed to retrieve states")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        # Step 4: Test with invalid token format (should fail)
        print_section("Step 4: Test Request WITH Invalid Token Format")
        print(f"GET {BASE_URL}/court/states")
        print("Authorization: InvalidFormat token_here")
        
        try:
            headers = {
                "Authorization": f"InvalidFormat {token}"
            }
            response = client.get(f"{BASE_URL}/court/states", headers=headers)
            print_response(response)
            
            if response.status_code == 401:
                print("\n✅ Correctly rejected invalid token format")
            else:
                print("\n⚠️  Unexpected response")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        # Step 5: Test POST request with token
        print_section("Step 5: Test POST Request (Get Districts)")
        print(f"POST {BASE_URL}/court/districts")
        print(f"Authorization: Bearer {token[:20]}...")
        print("Body: {\"state_code\": \"1\"}")
        
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            data = {"state_code": "1"}
            response = client.post(f"{BASE_URL}/court/districts", headers=headers, json=data)
            print_response(response)
            
            if response.status_code == 200:
                print("\n✅ Successfully retrieved districts with token!")
            else:
                print("\n⚠️  Check if state_code '1' is valid")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Summary
    print_section("Summary")
    print("""
    ✅ JWT Workflow Implementation Complete!
    
    Key Points:
    1. Users must call POST /auth/token to get a JWT
    2. Include the token in Authorization header: "Bearer <token>"
    3. All endpoints (except /auth/token) require valid token
    4. Each request uses an isolated HTTP client
    5. Clients are automatically closed after requests
    
    Usage Pattern:
    - Generate token once
    - Reuse token for multiple requests
    - Regenerate token if expired (401 response)
    """)


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         E-Courts API - JWT Workflow Test                  ║
    ║                                                            ║
    ║  This script tests the new JWT authentication workflow    ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    try:
        test_jwt_workflow()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
