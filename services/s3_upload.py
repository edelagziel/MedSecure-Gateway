import boto3
s3 = boto3.client("s3", region_name="eu-central-1")
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
BUCKET_NAME = "medsecure-eden-tma-2025"

def upload_to_s3(local_path, s3_key):
    try:
        s3.upload_file(local_path, BUCKET_NAME, s3_key)
    except Exception as e:
        raise ValueError(f"S3 upload failed: {e}")
