import logging

from chalice import (
    AuthResponse,
    BadRequestError,
    Chalice,
    ChaliceUnhandledError,
    Response,
)

from chalicelib import debug, environment
from chalicelib.business_logics.file_oprations import list_file_metadata
from chalicelib.constants import APP_NAME
from chalicelib.utils.logger import initialize_logging

logger = logging.getLogger(APP_NAME)

# Initialize AWS Chalice app
app = Chalice(app_name=APP_NAME, configure_logs=False)
app.debug = debug
initialize_logging(debug=app.debug)
logger.info(f"ENV: {environment}")
logger.info(f"DEBUG: {app.debug}")
logger.info("App creation complete . . .")


@app.route("/")
def index():
    return Response(
        body={"File Upload API": "Hello world!"},
        status_code=200,
    )


@app.middleware("all")
def middleware(event, get_response):
    try:
        logger.debug(event.to_dict())
        response = get_response(event)
        if isinstance(response.body, dict) and all(
            key in response.body for key in ("Code", "Message")
        ):
            response.body.pop("Code")
            response.body["message"] = response.body.pop("Message")
    except BadRequestError as e:
        logger.exception(e)
        return Response(
            body={"message": str(e)},
            status_code=400,
        )
    except ChaliceUnhandledError as e:
        return Response(
            body={"message": str(e)},
            status_code=500,
        )

    return response


@app.authorizer()
def jwt_token_auth(auth_request):
    token = auth_request.token
    context = {}
    is_token_valid = True

    if is_token_valid is True:
        return AuthResponse(routes=["*"], principal_id="N/A", context=context)
    else:
        return AuthResponse(routes=[], principal_id="N/A", context=context)


@app.route("/ping", methods=["GET"])
def ping():
    context = app.current_request.context
    logger.info("Pong for ping successfully retrieved.", extra=context)

    return Response(
        body={"pong": "From File Upload API"},
        status_code=200,
    )


@app.route("/files/metadata", methods=["GET"], authorizer=jwt_token_auth)
def files_list_file_metadata():
    items = list_file_metadata()

    return Response(
        body=items,
        status_code=200,
    )


@app.route("/files/metadata", methods=["POST"], authorizer=jwt_token_auth)
def files_post_file_metadata():
    pass


@app.route("/files/metadata/{file_uuid}", methods=["GET"], authorizer=jwt_token_auth)
def files_get_file_metadata(file_uuid):
    pass


@app.route("/files/{file_uuid}", methods=["PUT"], authorizer=jwt_token_auth)
def files_put_file(file_uuid):
    pass


@app.route("/files/{file_uuid}", methods=["GET"], authorizer=jwt_token_auth)
def files_get_file(file_uuid):
    pass
