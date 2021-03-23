import logging

from botocore.exceptions import ClientError

from .. import aws_session, s3_file_bucket_name
from ..constants import APP_NAME, S3_PRESIGNED_URL_EXPIRES_IN_SECONDS

logger = logging.getLogger(APP_NAME)

s3 = aws_session.client("s3")


def s3_get_upload_url(file_path, content_type=None):
    logger.info("Generating a pre-signed upload URL for a file in S3.")
    try:
        params = {
            "Bucket": s3_file_bucket_name,
            "Key": file_path,
        }
        if content_type:
            logger.debug(f"content_type: {content_type}")
            params["ContentType"] = content_type
        presigned_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params=params,
            ExpiresIn=S3_PRESIGNED_URL_EXPIRES_IN_SECONDS,
        )

        return presigned_url
    except ClientError as e:
        logger.error(e)
        raise


def s3_get_download_url(file_path, filename, content_type=None):
    logger.info("Generating a pre-signed download URL for a file in S3.")
    try:
        params = {
            "Bucket": s3_file_bucket_name,
            "Key": file_path,
            "ResponseContentDisposition": f"attachment; filename={filename}",
        }
        if content_type:
            logger.debug(f"content_type: {content_type}")
            params["ResponseContentType"] = content_type
        presigned_url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params=params,
            ExpiresIn=S3_PRESIGNED_URL_EXPIRES_IN_SECONDS,
        )

        return presigned_url
    except ClientError as e:
        logger.error(e)
        raise


def head_file(file_path):
    logger.info("Getting the metadata for a file in S3.")
    try:
        head_file_metadata = s3.head_object(Bucket=s3_file_bucket_name, Key=file_path)
        logger.debug(f"head_file_metadata: {head_file_metadata}")

        return head_file_metadata
    except ClientError as e:
        logger.error(e)
        raise
