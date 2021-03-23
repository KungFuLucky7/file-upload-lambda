import logging

from authlib.jose import JsonWebToken
from chalice import (
    AuthResponse,
    BadRequestError,
    Chalice,
    ChaliceUnhandledError,
    Response,
)

from chalicelib import debug, environment
from chalicelib.business_logics.file_oprations import (
    delete_file_metadata,
    get_file_metadata,
    get_file_url,
    list_file_metadata,
    post_file_metadata,
    post_file_url,
    put_file_metadata,
)
from chalicelib.constants import APP_NAME
from chalicelib.utils.logger import initialize_logging
from chalicelib.utils.secrets import secrets

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
    return Response(body={"File Upload API": "Front page"}, status_code=200)


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
    except BadRequestError as bre:
        logger.exception(bre)
        return Response(body={"message": str(bre)}, status_code=400)
    except ChaliceUnhandledError as cue:
        return Response(body={"message": str(cue)}, status_code=500)

    return response


@app.authorizer()
def jwt_token_auth(auth_request):
    token = auth_request.token
    user_id = "N/A"
    context = {}
    is_token_valid = False

    if token.startswith("Bearer "):
        token = token.split(" ")[1].strip()
        try:
            jwt = JsonWebToken(["HS256", "RS256"])
            key = secrets["AUTH0_CLIENT_SECRET"]
            logger.debug(f"Token key: {key}")
            claims = jwt.decode(token, key)
            logger.debug(f"Token claims: {claims}")
            user_id = claims["sub"]
            logger.info(f"user_id: {user_id}")
            is_token_valid = True
        except Exception as e:
            logger.exception(e)

    if is_token_valid is True:
        return AuthResponse(routes=["*"], principal_id=user_id, context=context)
    else:
        return AuthResponse(routes=[], principal_id=user_id, context=context)


@app.route("/ping", methods=["GET"])
def ping():
    context = app.current_request.context
    logger.info("Pong for ping successfully retrieved.", extra=context)

    return Response(body={"pong": "From File Upload API"}, status_code=200)


@app.route("/files/metadata", methods=["GET"], authorizer=jwt_token_auth, cors=True)
def files_list_file_metadata():
    items = list_file_metadata(app)

    return Response(body=items, status_code=200)


@app.route("/files/metadata", methods=["POST"], authorizer=jwt_token_auth, cors=True)
def files_post_file_metadata():
    item = post_file_metadata(app)

    return Response(body=item, status_code=201)


@app.route(
    "/files/metadata/{file_uuid}", methods=["GET"], authorizer=jwt_token_auth, cors=True
)
def files_get_file_metadata(file_uuid):
    item = get_file_metadata(app, file_uuid)

    return Response(body=item, status_code=200)


@app.route(
    "/files/metadata/{file_uuid}", methods=["PUT"], authorizer=jwt_token_auth, cors=True
)
def files_put_file_metadata(file_uuid):
    item = put_file_metadata(app, file_uuid)

    return Response(body=item, status_code=200)


@app.route(
    "/files/metadata/{file_uuid}",
    methods=["DELETE"],
    authorizer=jwt_token_auth,
    cors=True,
)
def files_delete_file_metadata(file_uuid):
    delete_file_metadata(app, file_uuid)

    return Response(body={}, status_code=204)


@app.route("/files/{file_uuid}", methods=["POST"], authorizer=jwt_token_auth, cors=True)
def files_post_file(file_uuid):
    upload_url = post_file_url(app, file_uuid)

    return Response(body={"upload_url": upload_url}, status_code=202)


@app.route("/files/{file_uuid}", methods=["GET"], authorizer=jwt_token_auth, cors=True)
def files_get_file(file_uuid):
    download_url = get_file_url(app, file_uuid)

    return Response(
        body=download_url, headers={"Location": download_url}, status_code=302
    )
