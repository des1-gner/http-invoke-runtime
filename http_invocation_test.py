import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests
import json

# Create session
session = boto3.Session()
credentials = session.get_credentials()
region = '<your-aws-region>'
service = 'bedrock-agentcore'

# Prepare request
url = "https://bedrock-agentcore.us-east-1.amazonaws.com/runtimes/<your-ENCODED-agentcore-runtime-arn>/invocations" # note this must be the encoded arn version see encoded_test.py to use ARN to construct URL more easily.
body = '{"prompt": "why sky is blue"}'

headers = {
    'X-Amzn-Bedrock-AgentCore-Runtime-Session-Id': '<your-session-id>'
}

# Create and sign request
request = AWSRequest(method='POST', url=url, data=body, headers=headers)
SigV4Auth(credentials, service, region).add_auth(request)

# ============================================================
# Print curl command for reference
# ============================================================
print("=" * 60)
print("GENERATED CURL COMMAND:")
print("=" * 60)
print("curl -X POST \\")
print(f'  "{url}" \\')
for key, value in request.headers.items():
    print(f'  -H "{key}: {value}" \\')
print(f"  -d '{body}'")
print("=" * 60)

# ============================================================
# Make the actual HTTP request using requests library
# ============================================================
print("\nMAKING REQUEST...")
print("=" * 60)

# Convert AWSRequest headers to dict
signed_headers = dict(request.headers)

# Make the request
response = requests.post(
    url,
    headers=signed_headers,
    data=body
)

# Print response details
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print("=" * 60)
print("RESPONSE BODY:")
print("=" * 60)

try:
    # Try to parse as JSON
    response_json = response.json()
    print(json.dumps(response_json, indent=2))
except:
    # If not JSON, print raw text
    print(response.text)

print("=" * 60)
