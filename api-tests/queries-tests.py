#!/usr/bin/python3
import json
import requests
import time
import unittest

from apiunittestcore import HttpResponseValidator
from apiunittestcore import JsonDataValidator
import common.utils
from common.utils import ApiHelperUtil

MODULE_NAME = "queries-tests"
_TEST_START_TIMESTAMP = time.time()

_api_helper_util = None

class _UtilFunctions():
    @staticmethod
    def make_queries_request():
        api_request_url = _api_helper_util.get_api_endpoint("Queries")
        bearer_access_token = _api_helper_util.create_new_bearer_access_token()
        http_headers = _api_helper_util.http_authentication_header(bearer_access_token)

        return requests.get(api_request_url, headers=http_headers)
    
    def make_query_text_validation_request(query_text):
        http_response = None
        if isinstance(query_text, str):
            # Create the API Request URL
            api_request_url = _api_helper_util.get_api_endpoint("Queries/validate")
            bearer_access_token = _api_helper_util.create_new_bearer_access_token()
            http_headers = _api_helper_util.http_authentication_header(bearer_access_token)
            http_headers.update(_api_helper_util.http_content_type_header("application/json"))
            post_data_map = {
                "queryText": query_text,
            }
            http_response = requests.post(api_request_url, headers=http_headers, json=post_data_map)
        return http_response
   
    def make_detailed_query_info_request(query_id):
        http_response = None
        if isinstance(query_id, str):
            query_endpoint = "Queries/{}".format(query_id)
            # Create the API Request URL
            api_request_url = _api_helper_util.get_api_endpoint(query_endpoint)
            bearer_access_token = _api_helper_util.create_new_bearer_access_token()
            http_headers = _api_helper_util.http_authentication_header(bearer_access_token)
            http_response = requests.get(api_request_url, headers=http_headers)

        return http_response

class QueriesFunctionalTests(unittest.TestCase):
    def setUp(self):
        log_message = "Performing Test ::{}".format(self._testMethodName)
        common.utils.log_info(MODULE_NAME, log_message)
         
    def test_list_all_queries(self):
        http_response = _UtilFunctions.make_queries_request()  
        # Begin assertions and validations

        # 1.0 Assert that a successful response was returned.
        self.assertTrue(HttpResponseValidator.is_successful_response(http_response))

        # 2.0 Assert that the expected response was returned as defined by the documentation:
        # https://yourlacework.lacework.net/api/v2/docs#tag/Queries
        # 200 A list of all registered LQL queries in the Lacework instance is returned.
        self.assertTrue(HttpResponseValidator.is_successful_200_ok_response(http_response))
        return None
        
    def test_validate_all_account_queries(self):
        # Get a list of all available QueryIds
        http_response = _UtilFunctions.make_queries_request()
        available_queries = None
        self.assertTrue(HttpResponseValidator.is_successful_response(http_response))
        if HttpResponseValidator.is_successful_response(http_response):
            available_queries = http_response.json()['data']
            
        for query in available_queries:
            query_id = query['queryId']
            # Request the detailed query info
            http_response = _UtilFunctions.make_detailed_query_info_request(query_id)
            self.assertTrue(HttpResponseValidator.is_successful_response(http_response))
            query_text = None
            if HttpResponseValidator.is_successful_response(http_response):
                query_text = http_response.json()['data']['queryText']
            # Validate the query text
            # Make the validation request
            http_response = _UtilFunctions.make_query_text_validation_request(query_text)
            # Begin assertions and validations
           
            # 1.0 Assert that a successful response was returned.
            self.assertTrue(HttpResponseValidator.is_successful_response(http_response))

            # 2.0 Assert that the expected response was returned as defined by the documentation:
            # https://yourlacework.lacework.net/api/v2/docs#tag/Queries
            # 200 A list of all registered LQL queries in the Lacework instance is returned.
            self.assertTrue(HttpResponseValidator.is_successful_200_ok_response(http_response))
        return None
        
    def test_query_details(self):
        # The test query of choice is one related to CloudTrail. CloudTrail queries are expected to
        # contain all expected response schema fields.
        TEST_QUERY_ID = "LaceworkLabs_AWS_CTA_CloudTrailCSVMaliciousFormula"
        http_response = _UtilFunctions.make_detailed_query_info_request(TEST_QUERY_ID)
        
        # Begin assertions and validations

        # 1.0 Assert that a successful response was returned.
        self.assertTrue(HttpResponseValidator.is_successful_response(http_response))

        # 2.0 Assert that the expected response was returned as defined by the documentation:
        # https://yourlacework.lacework.net/api/v2/docs#tag/Queries
        # 200 A list of all registered LQL queries in the Lacework instance is returned.
        self.assertTrue(HttpResponseValidator.is_successful_200_ok_response(http_response))
        
        # 3.0 Assert that the expected reponse schema is present.
        # *Note*: Only Lacework global CloudTrail queries require an evaluatorId. At present,
        #         no other query is expected to contain an evaluatorId in the JSON response.
        DATA_JSON_NAME = "data"
        EVALUATOR_ID_JSON_DATA_NAME = "evaluatorId"
        QUERY_ID_JSON_DATA_NAME = "queryId"
        QUERY_TEXT_JSON_DATA_NAME = "queryText"
        OWNER_JSON_DATA_NAME = "owner"
        LAST_UPDATE_TIME_JSON_DATA_NAME = "lastUpdateTime"
        LAST_UPDATE_USER_JSON_DATA_NAME = "lastUpdateUser"
        RESULTS_SCHEMA_JSON_DATA_NAME = "resultSchema"
        EXPECTED_RESPONSE_JSON_DATA_NAMES = [
            EVALUATOR_ID_JSON_DATA_NAME,
            QUERY_ID_JSON_DATA_NAME,
            QUERY_TEXT_JSON_DATA_NAME,
            OWNER_JSON_DATA_NAME,
            LAST_UPDATE_TIME_JSON_DATA_NAME,
            LAST_UPDATE_USER_JSON_DATA_NAME,
            RESULTS_SCHEMA_JSON_DATA_NAME
        ]
        
        http_response_json_map = http_response.json()
        query_detail_map = http_response_json_map.get(DATA_JSON_NAME)
        
        self.assertTrue(isinstance(query_detail_map, dict))
        self.assertTrue(
            JsonDataValidator.validate_json_data_names(
                query_detail_map,
                EXPECTED_RESPONSE_JSON_DATA_NAMES,
                match_set_explicitly=True,
            )
        )
        return None
        
    def test_validate_query_without_evaluator_id(self):
        # Create a test query to submit for validation.
        expected_valid_query_str = str(
            "LW_CUSTOM_DISTINCT_DNS {\n\
                source {\n\
                    LW_HA_DNS_REQUESTS\n\
                }\n\
                return distinct {HOSTNAME}\n\
            }")
        expected_valid_query_str = expected_valid_query_str.replace("   ", " ")
        print(expected_valid_query_str)
        
        # Make the validation request
        http_response = _UtilFunctions.make_query_text_validation_request(expected_valid_query_str)
              
        # Begin assertions and validations

        # 1.0 Assert that a successful response was returned.
        self.assertTrue(HttpResponseValidator.is_successful_response(http_response))

        # 2.0 Assert that the expected response was returned as defined by the documentation:
        # https://yourlacework.lacework.net/api/v2/docs#tag/Queries
        # 200 A list of all registered LQL queries in the Lacework instance is returned.
        self.assertTrue(HttpResponseValidator.is_successful_200_ok_response(http_response))
 
        # 3.0 Assert that the expected reponse schema is present.
        # *Note*: Only Lacework global CloudTrail queries require an evaluatorId. At present,
        #         no other query is expected to contain an evaluatorId in the JSON response.
        #         Hence, in this unit test, no evaluatorId data name is presented validating
        #         the JSON response.
        DATA_JSON_NAME = "data"
        QUERY_ID_JSON_DATA_NAME = "queryId"
        QUERY_TEXT_JSON_DATA_NAME = "queryText"
        OWNER_JSON_DATA_NAME = "owner"
        LAST_UPDATE_TIME_JSON_DATA_NAME = "lastUpdateTime"
        LAST_UPDATE_USER_JSON_DATA_NAME = "lastUpdateUser"
        RESULTS_SCHEMA_JSON_DATA_NAME = "resultSchema"
        EXPECTED_RESPONSE_JSON_DATA_NAMES = [
            QUERY_ID_JSON_DATA_NAME,
            QUERY_TEXT_JSON_DATA_NAME,
            OWNER_JSON_DATA_NAME,
            LAST_UPDATE_TIME_JSON_DATA_NAME,
            LAST_UPDATE_USER_JSON_DATA_NAME,
            RESULTS_SCHEMA_JSON_DATA_NAME
        ]
        
        http_response_json_map = http_response.json()
        query_detail_map = http_response_json_map.get(DATA_JSON_NAME)
        
        self.assertTrue(isinstance(query_detail_map, dict))
        self.assertTrue(
            JsonDataValidator.validate_json_data_names(
                query_detail_map,
                EXPECTED_RESPONSE_JSON_DATA_NAMES,
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
