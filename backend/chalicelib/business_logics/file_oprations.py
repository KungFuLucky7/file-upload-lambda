import logging
from uuid import UUID, uuid4

from chalice import BadRequestError, NotFoundError
from requests_toolbelt import MultipartDecoder

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

"""FileMetadata Schema
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
            "file_size": None,
            "media_uploaded": False,
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
    file_metadata = app.current_request.json_body
    file_metadata["record_updated"] = get_current_timestamp()
    item = update_file_metadata(file_uuid, user_id, file_metadata)
    if not item:
        raise NotFoundError("File metadata not found.")

    return item


def delete_file_metadata(app, file_uuid):
    context = app.current_request.context

    logger.info("Deleting a file metadata.", extra=context)
    user_id = app.current_request.context.get("authorizer", {}).get("principalId")
    remove_file_metadata(file_uuid, user_id)


def parse_multipart_object(headers, content):
    for header in headers.split(";"):
        # Only get the specific dropzone form values we need
        if header == "form-data":
            continue
        elif "filename" in header:
            filename_object = {
                "filename": header.split('"')[1::2][0],
                "content": content,
            }
            return filename_object
        elif 'name="file"' in header:
            continue
        else:
            header_name = header.split('"')[1::2][0]
            metadata_object = {header_name: content}
            return metadata_object


def put_file(app, file_uuid):
    context = app.current_request.context

    request_content_type = app.current_request.headers.get("content-type", "")
    if not request_content_type.startswith("multipart/form-data"):
        logger.debug(f"Request Content-Type: {request_content_type}")
        raise BadRequestError(f"Content-Type header must be 'multipart/form-data'.")

    logger.info("Putting a file.", extra=context)
    user_id = app.current_request.context.get("authorizer", {}).get("principalId")

    decoder = MultipartDecoder(
        app.current_request.raw_body, app.current_request.headers["content-type"]
    )
    # Only parse the first line from "multipart/form-data"
    part = decoder.parts[0]
    content_disposition = part.headers.get(b"Content-Disposition", b"").decode("utf-8")
    filename = (
        content_disposition.split("; ")[2]
        .replace("filename=", "")
        .replace('"', "")
        .strip()
    )
    logger.debug(f"filename: {filename}")
    content_type = part.headers.get(b"Content-Type", b"").decode("utf-8")
    logger.debug(f"content_type: {content_type}")
    file = part.content
    max_file_size = 104857600
    file_size = len(file)
    logger.debug(f"file_size: {file_size}")
    item = read_file_metadata(file_uuid, user_id)
    if not item:
        raise NotFoundError("File metadata not found.")
    logger.debug(f"file_metadata: {item}")

    if item["filename"] != filename:
        raise BadRequestError(
            f"Filename '{filename}' is inconsistent with "
            f"the filename '{item['filename']}' for the metadata."
        )
    elif not 0 < file_size <= max_file_size:
        raise BadRequestError(f"File size must be > 0 and <= {max_file_size} bytes.")


def get_file(app, file_uuid):
    context = app.current_request.context

    logger.info("Getting a file.", extra=context)
    user_id = app.current_request.context.get("authorizer", {}).get("principalId")
