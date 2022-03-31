#!/usr/bin/python3
from datetime import datetime
import json
import logging
import os
import requests

logging.basicConfig(level=logging.INFO)
_test_logger = logging.getLogger()

MODULE_NAME = "utils"


def _format_log_message(module_name, log_message):
    return log_message


def log_error(module_name, log_message):
    log_message = _format_log_message(module_name=module_name, log_message=log_message)
    _test_logger.error(log_message)


def log_warning(module_name, log_message):
    log_message = _format_log_message(module_name=module_name, log_message=log_message)
    _test_logger.warning(log_message)


def log_info(module_name, log_message):
    log_message = _format_log_message(module_name=module_name, log_message=log_message)
    _test_logger.info(log_message)


def json_file_to_map(json_file_uri):
    map_data = None
    try:
        with open(json_file_uri, "r") as json_file_data:
            map_data = json.load(json_file_data)
    except IOError as error:
        log_message = (
            'An IOError occured whle trying to load the JSON file: "{}"'.format(
                json_file_uri
            )
        )
        log_message += "Please check that the file path is correct.\n"
        log_error(MODULE_NAME, log_message)
    except json.decoder.json.JSONDecodeError as error:
        log_message = (
            'A syntax error was found when loading the JSON file: "{}":\n'.format(
                json_file_uri
            )
        )
        log_message += "json.decoder.json.JSONDecodeError: {} line, {} column {} (char {}).".format(
            error.msg, error.lineno, error.colno, error.pos
        )
        log_error(MODULE_NAME, log_message)
    return map_data


class ApiConfigParameters:
    API_ACCESS_KEY_ID = "api_access_key_id"
    API_ACCESS_KEY_EXPIRY_TIME_SECONDS = "api_access_key_expiry_time_seconds"
    CUSTOMER_ACCOUNT_NAME = "customer_account_name"
    SECRET_KEY = "secret_key"

    def __init__(
        self,
        api_access_key_id=None,
        api_access_key_expiry_time_seconds=None,
        customer_account_name=None,
        secret_key=None,
    ):
        self.api_access_key_id = api_access_key_id
        self.api_access_key_expiry_time_seconds = api_access_key_expiry_time_seconds
        self.customer_account_name = customer_account_name
        self.secret_key = secret_key

    def as_map(self):
        return {
            ApiConfigParameters.API_ACCESS_KEY_ID: self.api_access_key_id,
            ApiConfigParameters.API_ACCESS_KEY_EXPIRY_TIME_SECONDS: self.api_access_key_expiry_time_seconds,
            ApiConfigParameters.CUSTOMER_ACCOUNT_NAME: self.customer_account_name,
            ApiConfigParameters.SECRET_KEY: self.secret_key,
        }

    @staticmethod
    def as_json(self):
        return json.dumps(self.as_map(), indent=2)


class ApiHelperUtil:
    API_ACCESS_KEY_ID = "api_access_key_id"
    API_ACCESS_KEY_EXPIRY_TIME_SECONDS = "api_access_key_expiry_time_seconds"
    CUSTOMER_ACCOUNT_NAME = "customer_account_name"
    SECRET_KEY = "secret_key"

    def __init__(self, api_config_parameters) -> None:
        self._api_access_key_id = api_config_parameters.api_access_key_id
        self._api_access_key_expiry_time_seconds = (
            api_config_parameters.api_access_key_expiry_time_seconds
        )
        self._customer_account_name = api_config_parameters.customer_account_name
        self._secret_key = api_config_parameters.secret_key
        self._access_token = None
        self._access_token_creation_time = None
        self._access_token_expiry_time_seconds = None

    def api_access_key_id(self):
        return self._api_access_key_id

    def api_access_key_expiry_time_seconds(self):
        return self._api_access_key_expiry_time_seconds

    def customer_account_name(self):
        return self._customer_account_name

    def secret_key(self):
        return self._secret_key

    def access_token(self):
        return self._access_token

    def get_api_endpoint(self, api_requst):
        endpoint_url = None
        if isinstance(api_requst, str) and isinstance(self._customer_account_name, str):
            endpoint_url = "https://{}.lacework.net/api/v2/{}".format(
                self._customer_account_name, api_requst
            )
        return endpoint_url

    def create_new_bearer_access_token(self, expiry_time_seconds=3600):
        api_request_url = self.get_api_endpoint("access/tokens")

        http_headers = {
            "Content-Type": "application/json",
            "X-LW-UAKS": self.secret_key(),
        }

        post_data_map = {
            "keyId": self.api_access_key_id(),
            "expiryTime": self.api_access_key_expiry_time_seconds(),
        }

        http_response = requests.post(
            api_request_url, headers=http_headers, json=post_data_map
        )

        http_response_json_map = http_response.json()
        if isinstance(http_response_json_map, dict):
            bearer_access_token = http_response_json_map.get("token")
            if bearer_access_token != None:
                self._access_token = bearer_access_token
                self._access_token_creation_time = datetime.now()
                self._access_token_expiry_time_seconds = expiry_time_seconds
        else:
            log_message = "An error occured while creating a new bearer access token.\n"
            log_message += "    API endpoint: {}\n".format(api_request_url)
            log_error(MODULE_NAME, log_message)

        return bearer_access_token

    def bearer_access_token_valid(self):
        valid_time_remaining_seconds = 0
        if self._access_token_creation_time != None and isinstance(
            self._access_token_expiry_time_seconds, int
        ):
            valid_time_remaining_seconds = (
                datetime.now() - self._access_token_expiry_time_seconds
            )
        return isinstance(self._access_token, str) and valid_time_remaining_seconds > 0

    @staticmethod
    def http_authentication_header(authentication_token):
        return {"Authorization": "Bearer {}".format(authentication_token)}
    
    @staticmethod
    def http_content_type_header(content_type):
        return {"Content-Type": "{}".format(content_type)}


def configure_test_environment(json_config_file_uri=None):
    if None == json_config_file_uri:
        json_config_file_uri = ".api-test-config.json"
    api_config_parameters = None
    if isinstance(json_config_file_uri, str) and os.path.exists(json_config_file_uri):
        validated_config_file_map = ApiConfigParameters().as_map()
        config_file_map = json_file_to_map(json_file_uri=json_config_file_uri)
        # Set the environment configuration map from the configuration JSON file.
        for key, value in config_file_map.items():
            if key in validated_config_file_map:
                validated_config_file_map[key] = value

        api_config_parameters = ApiConfigParameters(**validated_config_file_map)

    return api_config_parameters
