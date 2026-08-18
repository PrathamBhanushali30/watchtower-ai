# MinIO/S3 helpers, hashing
import boto3
from botocore.client import Config
from app.core.config import settings

s3 = boto3.resource(
    's3',
    endpoint_url=settings.S3_ENDPOINT,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

def ensure_bucket(bucket_name: str):
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except Exception:
        s3.create_bucket(Bucket=bucket_name)

def upload_bytes(bucket: str, key: str, data: bytes, acl="private"):
    ensure_bucket(bucket)
    obj = s3.Object(bucket, key)
    obj.put(Body=data)
    return f"s3://{bucket}/{key}"
