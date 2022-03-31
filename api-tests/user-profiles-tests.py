#!/usr/bin/python3
import requests
import time
import unittest

from apiunittestcore import HttpResponseValidator
from apiunittestcore import JsonDataValidator
import common.utils
from common.utils import ApiHelperUtil

MODULE_NAME = "user-profiles-tests"
_TEST_START_TIMESTAMP = time.time()

_api_helper_util = None


class UserProfilesFunctionalTests(unittest.TestCase):
    def setUp(self):
        log_message = "Performing Test ::{}".format(self._testMethodName)
        common.utils.log_info(MODULE_NAME, log_message)

    def test_list_sub_accounts(self):
        # Create the API Request URL
        api_request_url = _api_helper_util.get_api_endpoint("UserProfile")
        bearer_access_token = _api_helper_util.create_new_bearer_access_token()
        http_headers = _api_helper_util.http_authentication_header(bearer_access_token)

        http_response = requests.get(api_request_url, headers=http_headers)

        # Begin assertions and validations

        # 1.0 Assert that a successful response was returned.
        self.assertTrue(HttpResponseValidator.is_successful_response(http_response))

        # 2.0 Assert that the expected response was returned as defined by the documentation:
        # https://yourlacework.lacework.net/api/v2/docs#tag/UserProfile
        # 200 A list of sub-accounts is returned.
        self.assertTrue(
            HttpResponseValidator.is_successful_200_ok_response(http_response)
        )

        # 3.0 Assert that the expected reponse schema is present.
        # At least one account should be returned in the application/json schema
        # Top level org data json names
        DATA_JSON_NAME = "data"
        USERNAME_JSON_NAME = "username"
        ORG_ACCOUNT_JSON_NAME = "orgAccount"
        URL_JSON_NAME = "url"
        ORG_ADMIN_JSON_NAME = "orgAdmin"
        ORG_USER_JSON_NAME = "orgUser"
        ACCOUNTS_JSON_NAME = "accounts"
        DATA_ORGANIZATION_JSON_DATA_NAMES_LIST = [
            USERNAME_JSON_NAME,
            ORG_ACCOUNT_JSON_NAME,
            URL_JSON_NAME,
            ORG_ADMIN_JSON_NAME,
            ORG_USER_JSON_NAME,
            ACCOUNTS_JSON_NAME,
        ]
        # Account based json names
        ADMIN_JSON_NAME = "admin"
        ACCOUNT_NAME_JSON_NAME = "accountName"
        CUST_GUID_JSON_NAME = "custGuid"
        USER_GUID_JSON_NAME = "userGuid"
        USER_ENABLED_JSON_NAME = "userEnabled"
        ACCOUNTS_JSON_DATA_NAMES_LIST = [
            ADMIN_JSON_NAME,
            ACCOUNT_NAME_JSON_NAME,
            CUST_GUID_JSON_NAME,
            USER_GUID_JSON_NAME,
            USER_ENABLED_JSON_NAME,
        ]

        # Extract the json response.
        # If a known account setup is provided, a JSON with explict key-value
        # pairs should be provided to establish a complete validation.
        http_response_json_map = http_response.json()
        organization_data_list = http_response_json_map.get(DATA_JSON_NAME)
        self.assertTrue(isinstance(organization_data_list, list))

        for organization_data_map in organization_data_list:
            # Validate each JSON object found in the list.
            self.assertTrue(isinstance(organization_data_map, dict))
            self.assertTrue(
                JsonDataValidator.validate_json_data_names(
                    organization_data_map,
                    DATA_ORGANIZATION_JSON_DATA_NAMES_LIST,
                    match_set_explicitly=True,
                )
            )
            accounts_list = organization_data_map.get(ACCOUNTS_JSON_NAME)
            self.assertTrue(isinstance(accounts_list, list))
            for account_data_map in accounts_list:
                self.assertTrue(isinstance(account_data_map, dict))
                self.assertTrue(
                    JsonDataValidator.validate_json_data_names(
                        account_data_map,
                        ACCOUNTS_JSON_DATA_NAMES_LIST,
                        match_set_explicitly=True,
                    )
                )
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
