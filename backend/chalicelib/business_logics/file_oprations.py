import logging

from ..constants import APP_NAME
from ..data_layers.db import db

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
    items = db.query_file_metadata(user_id)

    return items


def post_file_metadata(app, file_metadata):
    context = app.current_request.context

    logger.info("Posting a file metadata.", extra=context)
    user_id = None
    file_metadata["user_id"] = user_id
    item = db.create_file_metadata(file_metadata)

    return item


def get_file_metadata(app, file_uuid):
    context = app.current_request.context

    logger.info("Getting a file metadata.", extra=context)
    user_id = None
    item = db.get_file_metadata(file_uuid, user_id)

    return item


def put_file_metadata(app, file_uuid, file_metadata):
    context = app.current_request.context

    logger.info("Putting a file metadata.", extra=context)
    user_id = None
    item = db.update_file_metadata(file_uuid, user_id, file_metadata)

    return item


def delete_file_metadata(app, file_uuid):
    context = app.current_request.context

    logger.info("Deleting a file metadata.", extra=context)
    user_id = None
    db.remove_file_metadata(file_uuid, user_id)


def put_file(app, file_uuid):
    context = app.current_request.context

    logger.info("Putting a file.", extra=context)


def get_file(app, file_uuid):
    context = app.current_request.context

    logger.info("Getting a file.", extra=context)
