import logging

import boto3

from .. import dynamodb_table_name
from ..constants import APP_NAME

logger = logging.getLogger(APP_NAME)


class DynamoDB:
    def __init__(self, table_name):
        self._table = table_name

    def query_file_metadata(self, user_id: str) -> list:
        # response = self._table.query({"user_id": user_id})

        # return response["Items"]
        return [{"mock": "data"}]

    def create_file_metadata(self, file_metadata: dict) -> dict:
        self._table.put_item(Item=file_metadata)

        return file_metadata

    def get_file_metadata(self, file_uuid: str, user_id: str) -> dict:
        response = self._table.get_item(
            Key={"file_uuid": file_uuid, "user_id": user_id}
        )
        logger.info(response)

        return response.get("Item")

    def update_file_metadata(
        self,
        file_uuid: str,
        user_id: str,
        file_metadata: dict,
    ) -> dict:
        response = self._table.update_item(
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

    def remove_file_metadata(self, file_uuid: str = None, user_id: str = None) -> None:
        self._table.delete_item(Key={"file_uuid": file_uuid, "user_id": user_id})


db = DynamoDB(boto3.resource("dynamodb").Table(dynamodb_table_name))
