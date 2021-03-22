import logging
from uuid import UUID, uuid4

from chalice import NotFoundError

from ..constants import APP_NAME
from ..data_layers.db import (
    create_file_metadata,
    query_file_metadata,
    read_file_metadata,
    remove_file_metadata,
    update_file_metadata,
)
from ..data_layers.s3 import s3_get_download_url, s3_get_upload_url
from ..utils.helpers import get_current_timestamp

logger = logging.getLogger(APP_NAME)

"""FileMetadata Schema
    file_uuid
    filename
    file_size
    description
    content_type
    record_created
    record_updated
"""


def list_file_metadata(app):
    context = app.current_request.context

    logger.info("Listing the file metadata.", extra=context)
    user_id = app.current_request.context.get("authorizer", {}).get("principalId")
    items = query_file_metadata(user_id)

    return items


def post_file_metadata(app):
    context = app.current_request.context

    logger.info("Posting a file metadata.", extra=context)
    user_id = app.current_request.context.get("authorizer", {}).get("principalId")
    file_metadata = app.current_request.json_body
    # Get the ID that API Gateway assigns to the API request.
    request_id = app.current_request.context.get("requestId")
    logger.info(f"API Gateway Request ID: {request_id}", extra=context)
    if request_id:
        file_uuid = UUID(request_id).hex
    else:
        file_uuid = uuid4().hex
    current_timestamp = get_current_timestamp()
    file_metadata = {
        **{"file_uuid": file_uuid, "user_id": user_id},
        **file_metadata,
        **{
            "record_created": current_timestamp,
            "record_updated": current_timestamp,
        },
    }
    item = create_file_metadata(file_metadata)

    return item


def get_file_metadata(app, file_uuid):
    context = app.current_request.context

    logger.info("Getting a file metadata.", extra=context)
    user_id = app.current_request.context.get("authorizer", {}).get("principalId")
    item = read_file_metadata(file_uuid, user_id)
    if not item:
        raise NotFoundError("File metadata not found.")

    return item


def put_file_metadata(app, file_uuid):
    context = app.current_request.context

    logger.info("Putting a file metadata.", extra=context)
    user_id = app.current_request.context.get("authorizer", {}).get("principalId")
    file_metadata = read_file_metadata(file_uuid, user_id)
    if not file_metadata:
        raise NotFoundError("File metadata not found.")

    updated_file_metadata = app.current_request.json_body
    updated_file_metadata["record_updated"] = get_current_timestamp()
    item = update_file_metadata(file_uuid, user_id, updated_file_metadata)
    if not item:
        raise NotFoundError("File metadata not found.")

    return item


def delete_file_metadata(app, file_uuid):
    context = app.current_request.context

    logger.info("Deleting a file metadata.", extra=context)
    user_id = app.current_request.context.get("authorizer", {}).get("principalId")
    remove_file_metadata(file_uuid, user_id)


def post_file_url(app, file_uuid):
    context = app.current_request.context

    logger.info("Posting a file upload url.", extra=context)
    user_id = app.current_request.context.get("authorizer", {}).get("principalId")
    file_metadata = read_file_metadata(file_uuid, user_id)
    if not file_metadata:
        raise NotFoundError("File metadata not found.")

    file_path = f"{file_metadata['file_uuid']}/{file_metadata['filename']}"
    upload_url = s3_get_upload_url(file_path, file_metadata.get("content_type"))
    logger.debug(f"upload_url: {upload_url}")

    return upload_url


def get_file_url(app, file_uuid):
    context = app.current_request.context

    logger.info("Getting a file download url.", extra=context)
    user_id = app.current_request.context.get("authorizer", {}).get("principalId")
    file_metadata = read_file_metadata(file_uuid, user_id)
    if not file_metadata:
        raise NotFoundError("File metadata not found.")

    file_path = f"{file_metadata['file_uuid']}/{file_metadata['filename']}"
    download_url = s3_get_download_url(
        file_path, file_metadata["filename"], file_metadata.get("content_type")
    )
    logger.debug(f"download_url: {download_url}")

    return download_url
