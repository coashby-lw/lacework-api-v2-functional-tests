#!/usr/bin/python3
from datetime import datetime
import math
import requests
import time
import unittest

from apiunittestcore import HttpResponseValidator
import common.utils
from common.utils import ApiHelperUtil

MODULE_NAME = "access-tokens-tests"
_TEST_START_TIMESTAMP = time.time()

_api_helper_util = None


class AccessTokensFunctionalTests(unittest.TestCase):
    def setUp(self):
        log_message = "Performing Test ::{}".format(self._testMethodName)
        common.utils.log_info(MODULE_NAME, log_message)

    def test_generate_access_token(self):
        # Create the API Request URL
        api_request_url = _api_helper_util.get_api_endpoint("access/tokens")

        http_headers = {
            "Content-Type": "application/json",
            "X-LW-UAKS": _api_helper_util.secret_key(),
        }

        post_data_map = {
            "keyId": _api_helper_util.api_access_key_id(),
            "expiryTime": _api_helper_util.api_access_key_expiry_time_seconds(),
        }

        http_response = requests.post(
            api_request_url, headers=http_headers, json=post_data_map
        )
        # Let's measure time after the reponse has been generated. This will ignore
        # wait times due to transmission and processing in both directions.
        http_api_request_utc_date_time = datetime.utcnow()

        # Begin assertions and validations

        # 1.0 Assert that a successful response was returned.
        self.assertTrue(HttpResponseValidator.is_successful_response(http_response))

        # 2.0 Assert that the expected response was returned as defined by the documentation:
        # https://yourlacework.lacework.net/api/v2/docs#tag/ACCESS_TOKENS
        # 201 A temporary access (bearer) token is returned.
        self.assertTrue(
            HttpResponseValidator.is_successful_201_created_response(http_response)
        )

        # 3.0 Assert that the expected reponse schema is present.
        # The access token should be returned in an application/json schema
        EXPIRES_AT_JSON_DATA_NAME = "expiresAt"
        TOKEN_JSON_DATA_NAME = "token"
        EXPECTED_RESPONSE_JSON_DATA_NAMES = [
            EXPIRES_AT_JSON_DATA_NAME,
            TOKEN_JSON_DATA_NAME,
        ]
        self.assertTrue(
            HttpResponseValidator.validate_response_json(
                http_response=http_response,
                expected_response_json_data_names=EXPECTED_RESPONSE_JSON_DATA_NAMES,
            )
        )

        # 4.0 Validate the expiration time. The returned time is an ISO 8601
        # formatted UTC date time string: "yyyy-MM-ddTHH:mm:ss.SSSZ"
        http_response_json_map = http_response.json()
        returned_expires_at_utc_time_str = http_response_json_map[
            EXPIRES_AT_JSON_DATA_NAME
        ]
        returned_expires_at_utc_time_str = returned_expires_at_utc_time_str.replace(
            "Z", ""
        )
        expires_at_date_time = datetime.fromisoformat(returned_expires_at_utc_time_str)
        returned_expiry_time_seconds = (
            expires_at_date_time - http_api_request_utc_date_time
        ).total_seconds()
        self.assertLessEqual(
            math.floor(returned_expiry_time_seconds),
            _api_helper_util.api_access_key_expiry_time_seconds(),
        )
        expected_expiry_time_delta_seconds = math.ceil(
            (
                _api_helper_util.api_access_key_expiry_time_seconds()
                - returned_expiry_time_seconds
            )
        )
        # Log a warning message if the returned time is more than 5 seconds less than expected.
        # This may be an indication of a network or processing delay.
        MAX_EXPECTED_EXPIRY_TIME_DELTA_SECONDS = 5
        if expected_expiry_time_delta_seconds > MAX_EXPECTED_EXPIRY_TIME_DELTA_SECONDS:
            log_message = "While processing ::{}, the remaining expiry time returned was more than {}s".format(
                self._testMethodName, MAX_EXPECTED_EXPIRY_TIME_DELTA_SECONDS
            )
            log_message += " less than expected. This may be an indication of greater than expected"
            log_message += (
                " delays in either the network or processing of the API request."
            )
            common.utils.log_warning(MODULE_NAME, log_message)

        # 5.0 Assert that a token string was returned.
        # Are there any rules about token strings we should test?
        token_string = http_response_json_map[TOKEN_JSON_DATA_NAME]
        self.assertIsInstance(token_string, str)

        return None


if __name__ == "__main__":
    try:
        # Configure the unit test
        api_config_parameters = common.utils.configure_test_environment()
        _api_helper_util = ApiHelperUtil(api_config_parameters)
        # Run the module's unit test.
        unittest.main()

    except SystemExit as error:
        if error.args[0] == True:
            raise
