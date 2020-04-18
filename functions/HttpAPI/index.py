# -*- coding: utf-8 -*-

import logging
import json
from urllib.parse import urlparse, parse_qs

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkfnf.request.v20190315.StartExecutionRequest import StartExecutionRequest
from aliyunsdkfnf.request.v20190315.DescribeExecutionRequest import DescribeExecutionRequest

fnf_client = None

def handler(environ, start_response):
    global fnf_client
    RESP_BODY = b'{}'
    context = environ['fc.context']
    request_uri = environ['fc.request_uri']
    path = environ['PATH_INFO']
    creds = context.credentials

    query_params = parse_qs(urlparse(request_uri).query)

    if fnf_client == None:
        sts_creds = StsTokenCredential(creds.access_key_id, creds.access_key_secret, creds.security_token)
        fnf_client = AcsClient(credential=sts_creds, region_id=context.region)

    status = '200 OK'
    request_method = environ['REQUEST_METHOD']
    print(request_method)
    print(path)

    if request_method == 'POST' and path == '/start':
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        print(request_body)
        resp_s = start_execution(fnf_client, query_params['flowName'][0], request_body, context.region)
        resp = json.loads(resp_s)
        resp_body_str = '{"executionName":"%s"}'%resp['Name']
        RESP_BODY = resp_body_str.encode('utf-8')
    elif request_method == 'GET' and path == '/describe':
        resp = describe_execution(fnf_client, query_params['flowName'][0], query_params['executionName'][0], context.region)
        RESP_BODY = resp
    else:
        status = '404 Not Found'

    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [RESP_BODY]

def describe_execution(fnf_client, flow_name, execution_name, region):
    request = DescribeExecutionRequest()
    request.set_FlowName(flow_name)
    request.set_ExecutionName(execution_name)
    request.set_endpoint("{}-internal.fnf.aliyuncs.com".format(region))
    return fnf_client.do_action_with_exception(request)

def start_execution(fnf_client, flow_name, input, region):
    request = StartExecutionRequest()
    request.set_FlowName(flow_name)
    request.set_Input(input)
    request.set_endpoint("{}-internal.fnf.aliyuncs.com".format(region))
    return fnf_client.do_action_with_exception(request)