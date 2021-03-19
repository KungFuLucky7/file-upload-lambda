import logging

from .. import aws_session, s3_file_bucket_name
from ..constants import APP_NAME

logger = logging.getLogger(APP_NAME)

s3 = aws_session.client("s3")


def s3_upload_file(file, file_path):
    logger.info("Uploading a file to S3.")
    response = s3.put_object(Body=file, Bucket=s3_file_bucket_name, Key=file_path)
    logger.debug(f"S3 put_object() response: {response}")


def s3_download_file(file_path, file_name):
    response = s3.get_object(Bucket=s3_file_bucket_name, Key=f"{file_path}/{file_name}")
    logger.debug(f"S3 get_object() response: {response}")

    return response
