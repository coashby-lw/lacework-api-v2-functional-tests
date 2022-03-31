# Lacework API v2 Functional Tests
A collection of python tests that align to the Lacework v2 API in the effort of providing clear and concise usage along with programmatic validation of expected results.

<WIP>

## To Do
1. Complete README.md documentation
1. Add a python formatter
1. Complete test coverage
1. Create a batch testing script
1. Collate test results into a report file

## Requirements
<WIP>

## Usage
1. Make sure the configureation file `.api-test-config.json` is present in directory where the api tests will be run.
The contents of the file *MUST* be a JSON with the following data entries:
```JSON
{
    "api_access_key_id": <STRING>,
    "api_access_key_expiry_time_seconds": <INTEGER>,
    "customer_account_name": <STRING>,
    "secret_key": <STRING>
}
``` 
2. Run a collection of tests within an API by executing a particular self-named test script.
```shell
> python3 <API_TEST_SCRIPT_NAME>
```
Run an individual API function within an API test script by using the form
```shell
 > python3 <API_TEST_SCRIPT_NAME> -k=<FUNCTION_NAME>
 ```

 ### Examples
 *Run Access Token Tests*
 ```shell
 > python3 access-tokens-tests.py
 ```

