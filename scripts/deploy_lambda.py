import boto3
from botocore.exceptions import ClientError
import time

# -------------------------
# Config
# -------------------------
FUNCTION_NAME = "lambda-browser-tests"
IMAGE_URI = "345041926710.dkr.ecr.us-east-2.amazonaws.com/lambda-browser-tests:latest"
ROLE_ARN = "arn:aws:iam::345041926710:role/lambda-execution-role"

lambda_client = boto3.client("lambda")


def wait_for_update(function_name):
    """Wait for Lambda to finish updating (important for image functions)."""
    print("Waiting for Lambda to finish updating...")
    while True:
        resp = lambda_client.get_function(FunctionName=function_name)
        status = resp["Configuration"]["LastUpdateStatus"]
        if status in ("Successful", "Failed"):
            print("Update status:", status)
            return
        time.sleep(2)


def create_lambda():
    print("Creating new Lambda function...")

    response = lambda_client.create_function(
        FunctionName=FUNCTION_NAME,
        PackageType="Image",
        Role=ROLE_ARN,
        Code={"ImageUri": IMAGE_URI},
        Timeout=900,
        MemorySize=2048,
        Publish=True,
        Architectures=["x86_64"],  # required for Chrome-based images
    )

    print("Lambda created:")
    print(response)
    return response


def update_lambda():
    print("Updating existing Lambda function...")

    response = lambda_client.update_function_code(
        FunctionName=FUNCTION_NAME,
        ImageUri=IMAGE_URI,
        Publish=True
    )

    wait_for_update(FUNCTION_NAME)
    print("Lambda updated.")
    return response


# -------------------------
# Main
# -------------------------
try:
    # Check if Lambda exists
    lambda_client.get_function(FunctionName=FUNCTION_NAME)
    update_lambda()

except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceNotFoundException":
        create_lambda()
    else:
        raise
