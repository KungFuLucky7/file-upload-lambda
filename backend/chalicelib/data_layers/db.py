import logging

from .. import aws_session, dynamodb_table_name, dynamodb_table_name_gsi
from ..constants import APP_NAME

logger = logging.getLogger(APP_NAME)

table = aws_session.resource("dynamodb").Table(dynamodb_table_name)


def query_file_metadata(user_id: str) -> list:
    response = table.query(
        IndexName=dynamodb_table_name_gsi,
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": user_id},
    )

    return response["Items"]


def create_file_metadata(file_metadata: dict) -> dict:
    logger.info(f"Creating file metadata: {file_metadata}")
    table.put_item(Item=file_metadata)

    return file_metadata


def read_file_metadata(file_uuid: str, user_id: str) -> dict:
    response = table.get_item(Key={"file_uuid": file_uuid, "user_id": user_id})

    return response.get("Item")


def update_file_metadata(
    file_uuid: str,
    user_id: str,
    file_metadata: dict,
) -> dict:
    update_expression = "set filename=:filename"
    expression_attribute_values = {":filename": file_metadata["filename"]}
    if "file_size" in file_metadata:
        update_expression += ", file_size=:file_size"
        expression_attribute_values[":file_size"] = file_metadata["file_size"]
    if "description" in file_metadata:
        update_expression += ", description=:description"
        expression_attribute_values[":description"] = file_metadata["description"]
    if "content_type" in file_metadata:
        update_expression += ", content_type=:content_type"
        expression_attribute_values[":content_type"] = file_metadata["content_type"]
    if "media_uploaded" in file_metadata:
        update_expression += ", media_uploaded=:media_uploaded"
        expression_attribute_values[":media_uploaded"] = file_metadata["media_uploaded"]
    if "record_updated" in file_metadata:
        update_expression += ", record_updated=:record_updated"
        expression_attribute_values[":record_updated"] = file_metadata["record_updated"]
    response = table.update_item(
        Key={"file_uuid": file_uuid, "user_id": user_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW",
    )

    return response.get("Attributes")


def remove_file_metadata(file_uuid: str = None, user_id: str = None) -> None:
    response = table.delete_item(Key={"file_uuid": file_uuid, "user_id": user_id})
    logger.debug(f"DynamoDB delete_item() response: {response}")
