import boto3
import json

class ClaudeClient:
    def __init__(self, region_name="us-east-1", model_id="anthropic.claude-3-sonnet-20240229-v1:0"):
        self.client = boto3.client(service_name="bedrock-runtime", region_name=region_name)
        self.model_id = model_id

    def chat(self, messages, max_tokens=500, temperature=0.7, system=None):
        """
        messages: list of { "role": "user"|"assistant", "content": "..." }
        system: optional system prompt string
        """
        # Filter out system messages from messages array
        filtered_messages = [msg for msg in messages if msg.get("role") != "system"]
        
        # Extract system message if it exists in messages
        if not system:
            for msg in messages:
                if msg.get("role") == "system":
                    system = msg.get("content")
                    break

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": filtered_messages
        }

        # Add system prompt as top-level parameter if provided
        if system:
            body["system"] = system

        response = self.client.invoke_model(
            modelId=self.model_id,
            accept="application/json",
            contentType="application/json",
            body=json.dumps(body)
        )

        response_body = json.loads(response["body"].read())
        return response_body["content"][0]["text"]