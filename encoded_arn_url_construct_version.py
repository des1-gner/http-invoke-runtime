import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests
import json
from urllib.parse import quote

# Create session
session = boto3.Session()
credentials = session.get_credentials()
region = '<your-aws-region>'
service = 'bedrock-agentcore'

# Define ARN and encode it for URL
agent_runtime_arn = "<your-agentcore-runtime-arn>"
encoded_arn = quote(agent_runtime_arn, safe='')

# Prepare request with encoded ARN
url = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded_arn}/invocations"

body = json.dumps({"prompt": "why sky is blue"})

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Amzn-Bedrock-AgentCore-Runtime-Session-Id': '<your-session-id>'
}

# Create and sign request
request = AWSRequest(method='POST', url=url, data=body, headers=headers)
SigV4Auth(credentials, service, region).add_auth(request)

# Make the request
signed_headers = dict(request.headers)
response = requests.post(url, headers=signed_headers, data=body)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
