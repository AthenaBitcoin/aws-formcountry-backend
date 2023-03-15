
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


def get_jumio_token(callback_host, locale, tokenLifeTime=86400):
    values: dict[str, Any] = get_parameters_by_name(
        parameters={
            os.environ["JUMIO_TOKEN"]: {},
            os.environ["JUMIO_USER"]: {}
        },
        decrypt=True,
        raise_on_error=True)

    #  https://github.com/Jumio/implementation-guides/blob/master/netverify/netverify-web-v4.md
    auth_str = ':'.join([
                      values[os.environ["JUMIO_USER"]],
                      values[os.environ["JUMIO_TOKEN"]]])
    headers = {
        "Accept": 'application/json',
        "Content-Type": 'application/json',
        "Authorization": ' '.join([
            'Basic',
            base64.b64encode(auth_str.encode()).decode()]),
        "User-Agent": 'AthenaBitcoin MexOnboarding/v1.0'
    }
    url = 'https://netverify.com/api/v4/initiate'

    body = {
        "customerInternalReference": 'abc',
        "userReference": 'def',
        "reportingCriteria": None,
        "successUrl": f"https://{callback_host}/callbacks/jumio/success",
        "errorUrl": f"https://{callback_host}/callbacks/jumio/error",
        "callbackUrl": f"https://{callback_host}/callbacks/jumio/callback",
        "workflowId": 100,
        "locale": locale,
        "tokenLifetimeInMinutes": tokenLifeTime
               }
    http = urllib3.PoolManager()

    response = http.request('POST', url,
                        body=json.dumps(body).encode(),
                        headers=headers,
                        retries=False)

    if response.status != HTTPStatus.OK:
        logger.error(f"JUMIO={response.status}!  {response.data.decode('utf-8')}")
        raise RuntimeError("JUMIO!!!!")

    result = json.loads(response.data.decode('utf-8'))
    logger.debug(f"result: {result}")
    return result


#@event_source(data_class=APIGatewayProxyEventV2)
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST,
                              log_event=True)
def handler(event: dict, context: LambdaContext):

    logger.debug(f"Logging: CorrelationId = {logger.get_correlation_id()}")

    request = APIGatewayProxyEventV2(event)

    logger.debug(f"Object: {request}")

    r = get_jumio_token(host=event["headers"].get("Host"),
                        # https://regex101.com/library/sYfs0V?orderBy=LEAST_POINTS&page=442&search=
                        locale="es-MX")# get from accept language)
    # keys = set(['timestamp', 'transactionReference', 'redirectUrl'}

    return {
        "statusCode": HTTPStatus.OK,
        "body": {
            "redirectUrl": r['redirectUrl']
        },
        "headers": {
            #https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html
            #"Access-Control-Allow-Origin": '*',
            #"Access-Control-Allow-Headers": '*',
            #'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }