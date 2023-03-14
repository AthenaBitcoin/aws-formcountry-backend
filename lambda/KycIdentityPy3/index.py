
from aws_lambda_powertools.utilities.parser import event_parser, BaseModel, envelopes
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventV2Model
from typing import List, Optional

from aws_lambda_powertools import Logger

from aws_lambda_powertools.utilities.data_classes import event_source, APIGatewayProxyEventV2
import base64
import os
from http import HTTPStatus
from typing import Any
from aws_lambda_powertools.utilities.parameters.ssm import get_parameters_by_name
from aws_lambda_powertools.logging import correlation_paths

class UserIdentityLookup(BaseModel):
    user: str

class UserIdentityLookupGWModel(APIGatewayProxyEventV2Model):
    detail: UserIdentityLookup


# , envelope=envelopes.ApiGatewayV2Envelope
#@event_parser(model=UserIdentityLookupGWModel)
#def handler(event: UserIdentityLookup, context: LambdaContext):
#   print(f"printing {event}")


#import requests
logger = Logger()
import urllib3
import json
def get_jumio_token():
    values: dict[str, Any] = get_parameters_by_name(parameters={
        os.environ["JUMIO_TOKEN"]: {},
        os.environ["JUMIO_USER"]: {}
    }, raise_on_error=False)
    errors: list[str] = values.get("_errors", [])

    if len(errors):
        print(errors)
        raise RuntimeError()
    logger.info(f"Values: {values}")
    headers = {
        "Accept": 'application/json',
        "Content-Type": 'application/json',
        "Authorization": 'Basic ' + base64.b64encode(
            values[os.environ["JUMIO_USER"]] + ':' +
            values[os.environ["JUMIO_TOKEN"]]).encode(),
        "User - Agent": 'AthenaMexOnboarding',
        "Access-Control-Allow-Origin": '*'
    }
    url = 'https://netverify.com/api/v4/initiate'
    #response = requests.post(url, headers=headers)

    http = urllib3.PoolManager()

    response = http.request('POST',
                        url,
                        body = {},# json.dumps(some_data_structure),
                        headers = headers,
                        retries = False)

    print(response.text)


#@event_source(data_class=APIGatewayProxyEventV2)
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
def handler(event: dict, context : LambdaContext):
    print(f"printing {event}")

    logger.debug(f"Logging: CorrelationId = {logger.get_correlation_id()}")
    get_jumio_token()
    #

    request = APIGatewayProxyEventV2(event)

    return {
        "status_code": HTTPStatus.OK,
        "body": {},
        "headers": {
            #https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Headers": '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }