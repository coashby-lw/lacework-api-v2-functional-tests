#!/usr/bin/python3
import time
import unittest

import common.utils
from common.utils import ApiHelperUtil

MODULE_NAME = "alert-rules-tests"
_TEST_START_TIMESTAMP = time.time()

_api_helper_util = None


class AlertRulesFunctionalTests(unittest.TestCase):
    def setUp(self):
        log_message = "Performing Test ::{}".format(self._testMethodName)
        common.utils.log_info(MODULE_NAME, log_message)


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
