import logging
import sys
from collections import OrderedDict
from copy import deepcopy
from re import match
from time import gmtime, strftime

from backend.chalicelib import environment
from backend.chalicelib.constants import APP_NAME
from backend.chalicelib.enums import EnvironmentEnum


class LogFormatter(logging.Formatter):
    """
    Log Formatter
    """

    def __init__(
        self,
        name_size=5,
        levelname_size=5,
        filename_size=30,
        lineno_size=5,
        funcname_size=0,
        pid_size=0,
        *args,
        **kwargs,
    ):
        self._name_size = name_size
        self._levelname_size = levelname_size
        self._filename_size = filename_size
        self._lineno_size = lineno_size
        self._funcname_size = funcname_size
        self._pid_size = pid_size

        if environment == EnvironmentEnum.local.value:
            self._format_string = "%(asctime)s"
        else:
            # Timestamp is handled by lambda itself so the
            # default FORMAT_STRING doesn't need to include it in AWS environment.
            self._format_string = ""

        if self._name_size > 0:
            self._format_string += LogFormatter.create_log_attribute_format_string(
                "name", self._name_size
            )
        else:
            self._format_string += " %(name)s"

        if self._levelname_size > 0:
            self._format_string += LogFormatter.create_log_attribute_format_string(
                "levelname", self._levelname_size
            )
        else:
            self._format_string += " %(levelname)s"

        if self._filename_size > 0:
            self._format_string += LogFormatter.create_log_attribute_format_string(
                "filename", self._filename_size
            )
        else:
            self._format_string += " %(filename)s"

        if self._lineno_size > 0:
            self._format_string += LogFormatter.create_log_attribute_format_string(
                "lineno", self._lineno_size
            )

        if self._funcname_size > 0:
            self._format_string += LogFormatter.create_log_attribute_format_string(
                "funcName", self._funcname_size
            )

        if self._pid_size > 0:
            self._format_string += LogFormatter.create_log_attribute_format_string(
                "process", self._pid_size
            )

        self._format_string += " %(message)s "

        super().__init__(self._format_string, *args, **kwargs)

    @staticmethod
    def _dq_esc(s):
        """
        Replace all double quotes in a string with single quotes
        """

        return s.replace('"', "'")

    @staticmethod
    def create_log_attribute_format_string(attribute_name, attribute_size):
        return (
            f" %({attribute_name}"
            + (
                f")-{attribute_size}.{attribute_size}"
                if attribute_name != "lineno"
                else f")-{attribute_size}.0"
            )
            + ("s" if attribute_name != "lineno" else "d")
        )

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = strftime(datefmt, ct)
        else:
            t = strftime("%Y-%m-%d %H:%M:%S", ct)
            s = "%s.%03d" % (t, record.msecs)
        return s

    def _get_formatted_key_value_pair(self, key, value):
        easy_types = (str, bool, dict, float, int, list, type(None))

        if isinstance(value, easy_types):
            value = value
        else:
            value = repr(value)

        if key == "stack_info" and value is None:
            result = ""
        elif match(r"^-?(\d*\.\d+|\d+)$", str(value)):
            result = f"{key}={value}"
        else:
            result = f'{key}="{self._dq_esc(str(value))}"'

        return result

    def _get_extra_log_string(self, record):
        res = " "
        # The list contains all the attributes listed in
        # http://docs.python.org/library/logging.html#logrecord-attributes
        skip_list = (
            "args",
            "asctime",
            "created",
            "exc_info",
            "exc_text",
            "filename",
            "funcName",
            "id",
            "levelname",
            "levelno",
            "lineno",
            "module",
            "msecs",
            "msecs",
            "message",
            "msg",
            "name",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "thread",
            "threadName",
            "extra",
        )

        try:
            for key, value in OrderedDict(list(record.__dict__.items())).items():
                if key not in skip_list:
                    res += self._get_formatted_key_value_pair(key, value)
                    res += " "

        except Exception as e:
            res += f"  Exception: {e}"

        return res

    def format(self, record):
        if not record.exc_info:
            log_record = deepcopy(record)
        else:
            log_record = record

        res = super().format(log_record)
        res += self._get_extra_log_string(log_record)

        return res


def initialize_logging(
    debug=False,
    name_size=5,
    levelname_size=5,
    filename_size=30,
    lineno_size=5,
    funcname_size=0,
    pid_size=0,
):
    level = logging.DEBUG if debug is True else logging.INFO

    # Get a reference to the Chalice Logger
    log = logging.getLogger(APP_NAME)
    log.propagate = False
    log.setLevel(level)

    # Add log handler with custom formatter
    handler = logging.StreamHandler(sys.stdout)
    formatter = LogFormatter(
        name_size=name_size,
        levelname_size=levelname_size,
        filename_size=filename_size,
        lineno_size=lineno_size,
        funcname_size=funcname_size,
        pid_size=pid_size,
    )
    formatter.converter = gmtime
    handler.setFormatter(formatter)
    log.addHandler(handler)

    # Set default log level for AWS SDK for Python (Boto3)
    logging.getLogger("boto3").setLevel(logging.INFO)
    logging.getLogger("botocore").setLevel(logging.INFO)
    logging.getLogger("s3transfer").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.INFO)
