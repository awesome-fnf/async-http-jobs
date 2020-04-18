## Introduction

Serverless Workflow is not only ideal for orchestrating multiple Function Compute (FC) functions, it also provides the following benefits to asynchronously function invocations:

1. **Asynchrounous HTTP functions:** FC does not support async invocations for HTTP functions yet. However, the same functionality can be implemented by invoking a HTTP function that starts a workflow execution that runs asynchronously and its status can be queried by invoking the same HTTP function with a different path and queries.
2. **Reliable asynchronous invocations:** custom retry and try/catch support ensure reliable functions invocations.

This application demonstrates combining Serverless Workflow and Function Compute to support asynchronous HTTP functions invocations and the execution status can be queried by making HTTP requests as well.

## Dive deep
In order to make a HTTP triggered function to run in background and can be polled for status update, one can use a HTTP function (named HttpAPI) to start a Serverless Workflow execution (with the /start path and flowName query parameter) which runs asynchronously with durability. The caller is also able to query the execution status with the /describe path, flowName and executionName query parameters.

![intro](https://img.alicdn.com/tfs/TB1VQsrCEY1gK0jSZFCXXcwqXXa-1261-441.png)

## Development, deployments and invocations
The project source code: https://github.com/awesome-fnf/async-http-jobs

1. Install the `fun` command line interface that helps deploying Serverless Workflow and Function Compute related resources following https://github.com/alibaba/funcraft/blob/master/docs/usage/installation-zh.md.
2. Run `fun config` command to configure account ID, AKID and AKSecret.
3. Under the `async-http-jobs` to deploy all the resources
    ```
    fun package; fun deploy --use-ros --stack-name fnf-demo-http-async
    ```
4. Click Deploy and after all the related resources are successfully deployed, use the `curl` command returned from the deployment output
    ```bash
    ## Start an async flow execution, this command will return an executionName that can be used to describe this asynchronous job
    curl -X POST --data '{"key":"value"}' '<replace_fc_http_trigger_url>start?flowName=<replace_flow_name>'
    ```
5. Click the `AsyncWorkflow` resource to async-http-jobs flow，an execution has been started and is running
6. Using the following curl command to query the execution status
    ```bash
    # Describe the execution status
    curl -X GET '<replace_fc_http_trigger_url>describe?flowName=replace_flow_name>&executionName=<replace_execution_name>'
    ```