import boto3  # Import the boto3 library for AWS interactions

# Create an S3 client specifying the AWS region
s3 = boto3.client("s3", region_name="eu-central-1")

# Define the name of the S3 bucket to upload to
BUCKET_NAME = "medsecure-eden-tma-2025"

def upload_to_s3(local_path, s3_key):
    # Upload a local file to the specified S3 bucket and key
    try:
        s3.upload_file(local_path, BUCKET_NAME, s3_key)  # Perform the upload to S3
    except Exception as e:
        # Raise a ValueError with message if upload fails
        raise ValueError(f"S3 upload failed: {e}")
