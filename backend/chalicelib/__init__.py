import os

from boto3.session import Session

from .constants import APP_NAME, AWS_REGION_NAME

debug = os.getenv("DEBUG", "false").lower() == "true"
environment = os.getenv("ENV", "development").lower()
secret_name = os.getenv("SECRET_NAME", f"{APP_NAME}-secrets")
auth0_domain = os.getenv("AUTH0_DOMAIN")
dynamodb_table_name = os.getenv("DYNAMODB_TABLE_NAME", f"{APP_NAME}-dynamodb-table")
dynamodb_table_name_gsi = os.getenv(
    "DYNAMODB_TABLE_GSI", f"{APP_NAME}-dynamodb-table-gsi"
)

# Create an AWS session that stores configuration state
# and allows you to create service clients and resources
aws_session = Session(region_name=AWS_REGION_NAME)
