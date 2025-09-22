import boto3
import json

# Create bedrock client
client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# Input prompt
prompt = "Hello Claude, give me a one-line motivational message."

# Claude 3 requires a `messages` payload, not `prompt`
body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 200,
    "temperature": 0.7,
    "messages": [
        {"role": "user", "content": prompt}
    ]
}

response = client.invoke_model(
    modelId="anthropic.claude-3-sonnet-20240229-v1:0",  # correct Claude 3 Sonnet Bedrock model
    accept="application/json",
    contentType="application/json",
    body=json.dumps(body)
)

# Response body is a stream, need to parse json
response_body = json.loads(response["body"].read())
print(response_body["content"][0]["text"])