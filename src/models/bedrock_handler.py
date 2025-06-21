import boto3
import json
from .base_model import BaseModel

class BedrockHandler(BaseModel):
    def __init__(self, model_name, region="us-east-1"):
        self.model_name = model_name
        self.region = region
        self.bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=self.region
        )

    def generate_response(self, input_text, **kwargs):
        try:
            body = json.dumps({"prompt": input_text, "max_tokens": 100})
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_name,
                body=body,
                accept='application/json',
                contentType='application/json'
            )
            response_body = json.loads(response.get('body').read().decode())
            if 'results' in response_body and len(response_body['results']) > 0:
                return response_body['results'][0].get('outputText', '')
            else:
                return "No response"
        except Exception as e:
            return f"Error generating response: {str(e)}"