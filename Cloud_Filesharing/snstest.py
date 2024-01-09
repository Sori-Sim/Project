import json
import boto3

ACCESS_KEY = "AKIA26DYSGGADLEFRRL2"
SECRET_KEY="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"
AWS_REGION = 'us-east-1'
    
sns_client = boto3.client(
    'sns',
    aws_access_key_id = ACCESS_KEY,
    aws_secret_access_key = SECRET_KEY,
    region_name=AWS_REGION
    )

"""   
Creates a SNS notification topic.
"""
topic = sns_client.create_topic (Name= "newSNStest2")

print(topic)
def subscribe (topic, protocol, endpoint):
    """
    Subscribe to a topic using endpoint as email OR SMS
    """
    subscription = sns_client.subscribe(
        TopicArn=topic,
        Protocol=protocol, 
        Endpoint=endpoint,
        ReturnSubscriptionArn=True) 
    
    
if __name__ == '__main__':
    topic_arn = topic["TopicArn"]
    protocol = 'email'
    endpoint = "ssim@uab.edu"
    
    # Creates an email subscription
    response = subscribe(topic_arn, protocol, endpoint)