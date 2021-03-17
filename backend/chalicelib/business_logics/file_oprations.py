import logging

from ..constants import APP_NAME
from ..data_layers.db import db

logger = logging.getLogger(APP_NAME)

"""FileMetaData
    file_uuid
    filename
    file_size
    description
    content_type
    media_uploaded
    created_on
    updated_on
"""


def list_file_metadata():
    user_id = None
    items = db.query_file_metadata(user_id)

    return items


def post_file_metadata(file_metadata):
    user_id = None
    file_metadata["user_id"] = user_id
    db.create_file_metadata(file_metadata)


def get_file_metadata(file_uuid):
    user_id = None
    db.get_file_metadata(file_uuid, user_id)


def put_file_metadata(file_uuid, file_metadata):
    user_id = None
    db.update_file_metadata(file_uuid, user_id, file_metadata)


def delete_file_metadata(file_uuid):
    user_id = None
    db.remove_file_metadata(file_uuid, user_id)


def put_file(file_uuid):
    pass


def get_file(file_uuid):
    pass
