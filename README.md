# E-Commerce-Agility-With-Advanced-ETL-Pipeline

Overview
This project aims to create an end-to-end automated data processing workflow for the Order and Returns teams in an e-commerce environment. By utilizing AWS services like Glue, Lambda, S3, Redshift, SNS, and Step Functions, the workflow will process uploaded data files, perform necessary transformations, and provide notifications about the status of the pipeline.

Workflow Steps
Data Upload:

Streamlit Application: Create a web application for the Order and Returns teams to securely upload their data files to designated S3 buckets:
s3://your-bucket/orders/ for order data.
s3://your-bucket/returns/ for returned data.
AWS Lambda Function:

Set up an AWS Lambda function to trigger when new files are uploaded to the S3 buckets.
The function will:
Identify the newly uploaded files.
Invoke the AWS Glue ETL job.
AWS Glue ETL Job:

Create a Glue ETL job that:
Reads the uploaded order and return data files from S3.
Uses PySpark to perform transformations and joins on the datasets based on the "Order ID".
Outputs the joined dataset.
Data Storage in Redshift:

After joining the datasets, store the resulting table in an Amazon Redshift data warehouse.
Define a table schema that accommodates all necessary fields from both datasets.
Querying with Athena:

Enable querying of the final table in Redshift using AWS Athena for ad-hoc analysis and reporting.
AWS Step Functions:

Create a Step Function to orchestrate the ETL process:
Steps include Lambda invocation, Glue job execution, and Redshift data loading.
Implement error handling to capture any failures during the process.
SNS Notifications:

Set up AWS SNS to send notifications based on the pipeline’s execution status:
Configure two email subscription endpoints for notification.
Send notifications indicating whether the pipeline succeeded or failed after each execution.
Streamlit UI Integration:

Enhance the Streamlit UI to display the status of the pipeline execution:
Show success or failure messages based on the SNS notifications.
Implementation Steps
1. Streamlit Application
python
Copy code
import streamlit as st
import boto3

def upload_file(file, bucket_name, file_name):
    s3 = boto3.client('s3')
    s3.upload_fileobj(file, bucket_name, file_name)

st.title("Data Upload for Order and Returns")
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    team = st.selectbox("Select Team", ["Order", "Returns"])
    bucket_name = "your-bucket"
    if st.button("Upload"):
        upload_file(uploaded_file, bucket_name + ("/orders/" if team == "Order" else "/returns/"), uploaded_file.name)
        st.success("File uploaded successfully.")
2. AWS Lambda Function
python
Copy code
import json
import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    
    # Extract bucket and file name from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Invoke Glue Job
    glue_job_name = "your_glue_job_name"
    response = glue.start_job_run(JobName=glue_job_name)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Glue job started!')
    }
3. AWS Glue ETL Job
python
Copy code
import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

# Load order and returned data
order_df = glueContext.create_dynamic_frame.from_catalog(database = "your_database", table_name = "orders")
returned_df = glueContext.create_dynamic_frame.from_catalog(database = "your_database", table_name = "returns")

# Join dataframes
joined_df = Join.apply(order_df, returned_df, 'Order ID', 'Order ID')

# Write to Redshift
glueContext.write_dynamic_frame.from_catalog(frame = joined_df, database = "your_redshift_db", table_name = "joined_orders_returns")
4. AWS Step Functions
Define a state machine that includes Lambda and Glue job executions with error handling.
5. SNS Notifications
Configure SNS to notify after Glue job execution, updating the execution status.
6. Streamlit Integration
Update the Streamlit app to reflect the pipeline execution status based on SNS notifications.
