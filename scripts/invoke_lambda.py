
import boto3
import json

lambda_client = boto3.client('lambda', region_name='us-east-2')

response = lambda_client.invoke(
    FunctionName="lambda-browser-tests",
    InvocationType="RequestResponse"
)

# Read the payload
payload = response['Payload'].read().decode("utf-8")

# Print nicely
try:
    data = json.loads(payload)
    print(json.dumps(data, indent=2))
except json.JSONDecodeError:
    print(payload)
