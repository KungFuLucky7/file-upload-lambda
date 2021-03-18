import logging
from uuid import UUID, uuid4

from ..constants import APP_NAME
from ..data_layers.db import (
    create_file_metadata,
    query_file_metadata,
    read_file_metadata,
    remove_file_metadata,
    update_file_metadata,
)
from ..utils.helpers import get_current_timestamp

logger = logging.getLogger(APP_NAME)

"""FileMetadata
    file_uuid
    filename
    file_size
    description
    content_type
    media_uploaded
    created_on
    updated_on
"""


def list_file_metadata(app):
    context = app.current_request.context

    logger.info("Listing the file metadata.", extra=context)
    user_id = None
    items = query_file_metadata(user_id)

    return items


def post_file_metadata(app, file_metadata):
    context = app.current_request.context

    logger.info("Posting a file metadata.", extra=context)
    user_id = None
    # Get the ID that API Gateway assigns to the API request.
    request_id = app.current_request.context.get("requestId")
    logger.info(f"API Gateway Request ID: {request_id}", extra=context)
    if request_id:
        file_uuid = UUID(request_id).hex
    else:
        file_uuid = uuid4().hex
    file_metadata["file_uuid"] = file_uuid
    file_metadata["user_id"] = user_id
    file_metadata["record_created"] = file_metadata[
        "record_updated"
    ] = get_current_timestamp()
    item = create_file_metadata(file_metadata)

    return item


def get_file_metadata(app, file_uuid):
    context = app.current_request.context

    logger.info("Getting a file metadata.", extra=context)
    user_id = None
    item = read_file_metadata(file_uuid, user_id)

    return item


def put_file_metadata(app, file_uuid, file_metadata):
    context = app.current_request.context

    logger.info("Putting a file metadata.", extra=context)
    user_id = None
    file_metadata["user_id"] = user_id
    file_metadata["record_updated"] = get_current_timestamp()
    item = update_file_metadata(file_uuid, user_id, file_metadata)

    return item


def delete_file_metadata(app, file_uuid):
    context = app.current_request.context

    logger.info("Deleting a file metadata.", extra=context)
    user_id = None
    remove_file_metadata(file_uuid, user_id)


def put_file(app, file_uuid):
    context = app.current_request.context

    logger.info("Putting a file.", extra=context)


def get_file(app, file_uuid):
    context = app.current_request.context

    logger.info("Getting a file.", extra=context)
