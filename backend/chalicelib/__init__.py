import os

from boto3.session import Session

from backend.chalicelib.constants import AWS_REGION_NAME

debug = os.getenv("DEBUG", "false").lower() == "true"
environment = os.getenv("ENV", "development").lower()

# Create an AWS session that stores configuration state
# and allows you to create service clients and resources
aws_session = Session(region_name=AWS_REGION_NAME)
