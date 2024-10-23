import json
import boto3

s3_client = boto3.client('s3')
glue_client = boto3.client('glue')
step_client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    step_response = step_client.start_execution(stateMachineArn="arn",)
    
    print("started step...!")
    return {
        'statusCode': 200,
        'body': json.dumps('completed')
    }
