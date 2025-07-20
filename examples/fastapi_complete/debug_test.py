"""Debug the FastAPI test issues - Atlas Coder fixing real bugs!"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Debug the registration issue
test_user_data = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpassword123"
}

print("🐛 DEBUGGING FASTAPI REGISTRATION ISSUE")
print("=" * 50)

# Test registration
response = client.post("/auth/register", json=test_user_data)
print(f"Registration Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code != 201:
    print("\n🔍 ANALYZING BUG...")
    print("Expected: 201 Created")
    print(f"Actual: {response.status_code}")
    
    try:
        error_detail = response.json()
        print(f"Error Detail: {error_detail}")
    except:
        print("Could not parse error JSON")

# Test with different data
print("\n🧪 TESTING ALTERNATIVE DATA...")
simple_data = {
    "email": "simple@test.com",
    "username": "simple",
    "password": "password"
}

response2 = client.post("/auth/register", json=simple_data)
print(f"Simple Registration Status: {response2.status_code}")
print(f"Simple Response: {response2.text}")

# Test health endpoint
print("\n🩺 HEALTH CHECK...")
health_response = client.get("/health")
print(f"Health Status: {health_response.status_code}")
print(f"Health Response: {health_response.json()}")