#!/usr/bin/env python3

import base64
import json

from botocore.exceptions import ClientError

from backend.chalicelib import aws_session, secret_name
from backend.chalicelib.constants import AWS_REGION_NAME


def get_secrets() -> dict:
    # Create a Secrets Manager client
    client = aws_session.client(
        service_name="secretsmanager",
        region_name=AWS_REGION_NAME,
    )

    # In this sample we only handle the specific exceptions
    # for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com
    # /secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text
            # using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid
            # for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        else:
            raise
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary,
        # one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            secrets = json.loads(get_secret_value_response["SecretString"])
        else:
            secrets = base64.b64decode(get_secret_value_response["SecretBinary"])

    return secrets


# Get secrets from AWS Secrets Manager
secrets = get_secrets()

if __name__ == "__main__":
    app_secrets = get_secrets()
    print(app_secrets)
