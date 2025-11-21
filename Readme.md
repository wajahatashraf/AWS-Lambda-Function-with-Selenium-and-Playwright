# AWS Lambda Function with Selenium and Playwright

This repository provides an AWS Lambda setup for running browser automation using **Selenium** and **Playwright** in a serverless environment. The project uses **Docker** to package the Lambda function with all dependencies, including Chrome and Node.js.

---

## Features

- Run **Selenium** scripts on AWS Lambda.
- Run **Playwright** scripts on AWS Lambda.
- Package Lambda with all browser dependencies using Docker.
- Push Docker images to **AWS ECR**.
- Easily deploy Lambda functions using the pre-built Docker image.

---

## Prerequisites

- AWS CLI configured with appropriate permissions.
- Docker installed on your local machine.
- Python 3.10+ (if running scripts locally).
- Node.js (for Playwright if building locally).

---

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/wajahatashraf/AWS-Lambda-Function-with-Selenium-and-Playwright.git
cd AWS-Lambda-Function-with-Selenium-and-Playwright
```

2. **Create ECR Repository**
```bash
aws ecr create-repository --repository-name lambda-browser-tests --region us-east-2
```
```bash
it show like this```
{
  "repository": {
    "repositoryArn": "arn:aws:ecr:us-east-2:345041926710:repository/lambda-browser-tests",
    "registryId": "345041926710",
    "repositoryName": "lambda-browser-tests",
    "repositoryUri": "345041926710.dkr.ecr.us-east-2.amazonaws.com/lambda-browser-tests",
    "createdAt": "2025-11-21T00:56:27.988000+05:00",
    "imageTagMutability": "MUTABLE",
    "imageScanningConfiguration": { "scanOnPush": false },
    "encryptionConfiguration": { "encryptionType": "AES256" }
  }
}
```

3. **Authenticate Docker to ECR**
```bash
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 345041926710.dkr.ecr.us-east-2.amazonaws.com
```
## Build & Push Docker Image

1. **Build & Push Docker Image**
```bash
docker build -t lambda-browser-tests .
```

2. **Tag Docker image for ECR**
```bash
docker tag lambda-browser-tests:latest 345041926710.dkr.ecr.us-east-2.amazonaws.com/lambda-browser-tests:latest
```

3. **Push Docker image to ECR**
```bash
docker push 345041926710.dkr.ecr.us-east-2.amazonaws.com/lambda-browser-tests:latest
```
---


## 🚀 Deploy Lambda Function

After pushing your Docker image to ECR, deploy the Lambda function using the Python script:

```bash
python scripts/deploy_lambda.py
python scripts/invoke_lambda.py
```
It return like this:
```bash
{
  "playwright_html": "<html>...</html>",
  "selenium_title": "Google"
}
```