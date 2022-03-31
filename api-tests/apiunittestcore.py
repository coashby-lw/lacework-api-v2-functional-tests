#!/usr/bin/python3

MODULE_NAME = "apiunittestcore"


class HttpResponseCode:
    SUCCESSFUL_RESPONSE_200_OK = 200
    SUCCESSFUL_RESPONSE_201_CREATED = 201
    SUCCESSFUL_RESPONSE_204_NO_CONTENT = 204

    CLIENT_ERROR_RESPONSE_400_BAD_REQUEST = 400
    CLIENT_ERROR_RESPONSE_401_UNATHORIZED = 401
    CLIENT_ERROR_RESPONSE_403_FORBIDDEN = 403
    CLIENT_ERROR_RESPONSE_404_NOT_FOUND = 404
    CLIENT_ERROR_RESPONSE_405_METHOD_NOT_ALLOWED = 405
    CLIENT_ERROR_RESPONSE_409_CONFLICT = 409
    CLIENT_ERROR_RESPONSE_429_TOO_MANY_REQUESTS = 429

    SERVER_ERROR_RESPONSE_500_INTERNAL_SERVER_ERROR = 500
    SERVER_ERROR_RESPONSE_503_SERVICE_UNAVAILABLE = 503

class JsonDataValidator:
    @staticmethod
    def validate_json_data_names(
        json_map, expected_json_data_names, match_set_explicitly=False
    ):
        expected_names_found = False
        if isinstance(json_map, dict) and isinstance(expected_json_data_names, list):
            expected_names_found = True
            input_json_data_names = list(json_map.keys())
            if match_set_explicitly and len(input_json_data_names) != len(
                expected_json_data_names
            ):
                return False

            for key in expected_json_data_names:
                if key not in input_json_data_names:
                    expected_names_found = False
                    break
        return expected_names_found

    @staticmethod
    def validate_json_data(
        json_map, expected_json_data_map, match_data_explicitly=False
    ):
        expected_data_found = True
        input_json_data_names = list(json_map.keys())
        if match_data_explicitly and len(input_json_data_names) != len(
            match_data_explicitly
        ):
            return False
        for key, value in expected_json_data_map.items():
            if key not in json_map:
                expected_data_found = False
                break
            elif json_map[key] != value:
                expected_data_found = False
                break

        return expected_data_found

class HttpResponseValidator:
    @staticmethod
    def validate_response_json(
        http_response,
        expected_response_json_data_names=None,
        expected_response_json_map=None,
    ):
        expected_response = True
        http_response_json_map = http_response.json()
        if not isinstance(http_response_json_map, dict):
            expected_response = False
        else:
            if isinstance(expected_response_json_map, dict):
                expected_response = JsonDataValidator.validate_json_data(
                    http_response_json_map, expected_response_json_map
                )
            elif isinstance(expected_response_json_data_names, list):
                expected_response = JsonDataValidator.validate_json_data_names(
                    http_response_json_map, expected_response_json_data_names
                )
        return expected_response

    @staticmethod
    def is_informational_response(http_response):
        return http_response.status_code >= 100 and http_response.status_code < 200

    @staticmethod
    def is_successful_response(http_response):
        return http_response.status_code >= 200 and http_response.status_code < 300

    @staticmethod
    def is_successful_200_ok_response(http_response):
        return HttpResponseCode.SUCCESSFUL_RESPONSE_200_OK == http_response.status_code

    @staticmethod
    def is_successful_201_created_response(http_response):
        return (
            HttpResponseCode.SUCCESSFUL_RESPONSE_201_CREATED
            == http_response.status_code
        )

    @staticmethod
    def is_successful_204_no_content_response(http_response):
        return (
            HttpResponseCode.SUCCESSFUL_RESPONSE_204_NO_CONTENT
            == http_response.status_code
        )

    @staticmethod
    def is_redirection_message(http_response):
        return http_response.status_code >= 300 and http_response.status_code < 400

    @staticmethod
    def is_client_error_response(http_response):
        return http_response.status_code >= 400 and http_response.status_code < 500

    @staticmethod
    def is_client_error_400_bad_request_response(http_response):
        return (
            HttpResponseCode.CLIENT_ERROR_RESPONSE_400_BAD_REQUEST
            == http_response.status_code
        )

    @staticmethod
    def is_client_error_401_unathorized_response(http_response):
        return (
            HttpResponseCode.CLIENT_ERROR_RESPONSE_401_UNATHORIZED
            == http_response.status_code
        )

    @staticmethod
    def is_client_error_403_forbidden_response(http_response):
        return (
            HttpResponseCode.CLIENT_ERROR_RESPONSE_403_FORBIDDEN
            == http_response.status_code
        )

    @staticmethod
    def is_client_error_404_not_found_response(http_response):
        return (
            HttpResponseCode.CLIENT_ERROR_RESPONSE_404_NOT_FOUND
            == http_response.status_code
        )

    @staticmethod
    def is_client_error_405_method_not_allowed_response(http_response):
        return (
            HttpResponseCode.CLIENT_ERROR_RESPONSE_405_METHOD_NOT_ALLOWED
            == http_response.status_code
        )

    @staticmethod
    def is_client_error_409_conflict_response(http_response):
        return (
            HttpResponseCode.CLIENT_ERROR_RESPONSE_409_CONFLICT
            == http_response.status_code
        )

    @staticmethod
    def is_client_error_429_too_many_requests_response(http_response):
        return (
            HttpResponseCode.CLIENT_ERROR_RESPONSE_429_TOO_MANY_REQUESTS
            == http_response.status_code
        )

    @staticmethod
    def is_server_error_response(http_response):
        return http_response.status_code >= 500 and http_response.status_code < 600

    @staticmethod
    def is_server_error_500_internal_server_error_response(http_response):
        return (
            HttpResponseCode.SERVER_ERROR_RESPONSE_500_INTERNAL_SERVER_ERROR
            == http_response.status_code
        )

    @staticmethod
    def is_server_error_503_service_unavailable_response(http_response):
        return (
            HttpResponseCode.SERVER_ERROR_RESPONSE_503_SERVICE_UNAVAILABLE
            == http_response.status_code
        )
