import os

from boto3.session import Session

from .constants import APP_NAME, AWS_REGION_NAME

debug = os.getenv("DEBUG", "false").lower() == "true"
environment = os.getenv("ENV", "development").lower()
secret_name = os.getenv("SECRET_NAME", f"{APP_NAME}-secret")

# Create an AWS session that stores configuration state
# and allows you to create service clients and resources
aws_session = Session(region_name=AWS_REGION_NAME)
