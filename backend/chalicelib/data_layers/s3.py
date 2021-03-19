import logging

from botocore.exceptions import ClientError

from .. import aws_session, s3_file_bucket_name
from ..constants import APP_NAME

logger = logging.getLogger(APP_NAME)

s3 = aws_session.client("s3")


def s3_upload_file(file, file_path):
    logger.info("Uploading a file to S3.")
    try:
        response = s3.put_object(Body=file, Bucket=s3_file_bucket_name, Key=file_path)
        logger.debug(f"S3 put_object() response: {response}")
    except ClientError as e:
        logging.error(e)
        raise


def s3_download_file(file_path):
    try:
        response = s3.get_object(Bucket=s3_file_bucket_name, Key=file_path)
        logger.debug(f"S3 get_object() response: {response}")

        return response.get("Body", b"").read()
    except ClientError as e:
        logging.error(e)
        raise


def s3_get_upload_url(file_path, content_type):
    logger.info("Generating a pre-signed upload URL for a file in S3.")
    try:
        params = {
            "Bucket": s3_file_bucket_name,
            "Key": file_path,
        }
        if content_type:
            params["ContentType"] = content_type
        presigned_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params=params,
            ExpiresIn=604800,
        )
        logger.debug(f"S3 generate_presigned_url() response: {presigned_url}")

        return presigned_url
    except ClientError as e:
        logging.error(e)
        raise


def s3_get_download_url(file_path, content_type):
    logger.info("Generating a pre-signed download URL for a file in S3.")
    try:
        params = {
            "Bucket": s3_file_bucket_name,
            "Key": file_path,
        }
        if content_type:
            params["ContentType"] = content_type
        presigned_url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params=params,
            ExpiresIn=604800,
        )
        logger.debug(f"S3 generate_presigned_url() response: {presigned_url}")

        return presigned_url
    except ClientError as e:
        logging.error(e)
        raise
