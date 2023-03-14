
from aws_lambda_powertools.utilities.parser import event_parser, BaseModel, envelopes
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventV2Model
from typing import List, Optional


from aws_lambda_powertools.utilities.data_classes import event_source, APIGatewayProxyEventV2
import base64
import os
from http import HTTPStatus
from typing import Any
from aws_lambda_powertools.utilities.parameters.ssm import get_parameters_by_name


class UserIdentityLookup(BaseModel):
    user: str

class UserIdentityLookupGWModel(APIGatewayProxyEventV2Model):
    detail: UserIdentityLookup


# , envelope=envelopes.ApiGatewayV2Envelope
#@event_parser(model=UserIdentityLookupGWModel)
#def handler(event: UserIdentityLookup, context: LambdaContext):
#   print(f"printing {event}")


#import requests

import urllib3
import json
def get_jumio_token():
    values: dict[str, Any] = get_parameters_by_name(parameters={
        os.environ["JUMIO_TOKEN"]: {"transform": 'str'},
        os.environ["JUMIO_USER"]: {"transform": 'str'}
    }, raise_on_error=False)
    errors: list[str] = values.get("_errors", [])

    if len(errors):
        print(errors)
        raise RuntimeError()

    headers = {
        "Accept": 'application/json',
        "Content-Type": 'application/json',
        "Authorization": 'Basic ' + base64.b64encode(values['JUMIO_USER'] + ':' + values['JUMIO_TOKEN']).encode(),
        "User - Agent": 'AthenaMexOnboarding',
        "Access - Control - Allow - Origin": '*'
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


@event_source(data_class=APIGatewayProxyEventV2)
def handler(event: APIGatewayProxyEventV2, context):
    print(f"printing {event}")
    get_jumio_token()
    #

    return {
        "status_code": HTTPStatus.OK,
        "body": {}
    }