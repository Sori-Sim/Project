import json
import boto3

ACCESS_KEY = "AKIA26DYSGGADLEFRRL2"
SECRET_KEY="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"

lambda_client = boto3.client ('lambda',
    aws_access_key_id=ACCESS_KEY, 
    aws_secret_access_key=SECRET_KEY,
    region_name='us-east-1')

email="testEmail@gmail.com"
lambda_payload={"email":email, "arn": "arn:aws:sns:us-east-1:751872127360:newSNStest2"}
lambda_client.invoke(FunctionName='mylambdatest',
                     InvocationType= 'Event',
                     Payload=json.dumps(lambda_payload))