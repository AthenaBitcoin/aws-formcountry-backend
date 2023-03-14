
from aws_lambda_powertools.utilities.parser import event_parser, BaseModel, envelopes
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventV2Model
from typing import List, Optional


from aws_lambda_powertools.utilities.data_classes import event_source, APIGatewayProxyEventV2

from http import HTTPStatus

class UserIdentityLookup(BaseModel):
    user: str

class UserIdentityLookupGWModel(APIGatewayProxyEventV2Model):
    detail: UserIdentityLookup


# , envelope=envelopes.ApiGatewayV2Envelope
#@event_parser(model=UserIdentityLookupGWModel)
#def handler(event: UserIdentityLookup, context: LambdaContext):
#   print(f"printing {event}")

@event_source(data_class=APIGatewayProxyEventV2)
def handler(event: APIGatewayProxyEventV2, context):
    print(f"printing {event}")
    return {
        "status_code": HTTPStatus.OK,
        "body": {}
    }