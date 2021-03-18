import logging

import boto3

from .. import dynamodb_table_name, dynamodb_table_name_gsi
from ..constants import APP_NAME

logger = logging.getLogger(APP_NAME)

table = boto3.resource("dynamodb").Table(dynamodb_table_name)


def query_file_metadata(user_id: str) -> list:
    response = table.query(
        IndexName=dynamodb_table_name_gsi,
        KeyConditionExpression="userId = :userId",
        ExpressionAttributeValues={":userId": user_id},
    )

    return response["Items"]


def create_file_metadata(file_metadata: dict) -> dict:
    logger.info("Creating file metadata.")
    table.put_item(Item=file_metadata)

    return file_metadata


def read_file_metadata(file_uuid: str, user_id: str) -> dict:
    response = table.get_item(Key={"file_uuid": file_uuid, "user_id": user_id})
    logger.info(response)

    return response.get("Item")


def update_file_metadata(
    file_uuid: str,
    user_id: str,
    file_metadata: dict,
) -> dict:
    response = table.update_item(
        Key={"file_uuid": file_uuid, "user_id": user_id},
        UpdateExpression="set filename=:filename, "
        "description=:description, "
        "content_type=:content_type",
        ExpressionAttributeValues={
            ":filename": file_metadata["filename"],
            ":description": file_metadata["description"],
            ":content_type": file_metadata["content_type"],
        },
        ReturnValues="UPDATED_NEW",
    )
    logger.info(response)

    return response.get("Item")


def remove_file_metadata(file_uuid: str = None, user_id: str = None) -> None:
    table.delete_item(Key={"file_uuid": file_uuid, "user_id": user_id})
