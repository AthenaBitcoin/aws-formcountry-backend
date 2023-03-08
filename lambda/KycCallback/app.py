import json
import  boto3
import os 
from botocore.exceptions import ClientError


# client representing Amazon Cognito Identity Provider
client = boto3.client('cognito-idp')



def lambda_handler(event, context):


    result_dict = {}
    print(json.dumps(event))
    
    try:
        # TODO: How to pass phone number with + in query string
        user_id=event['queryStringParameters']['user_id']
    except Exception as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({
                "message": "Invalid Input"
            }) }

    ######Gets the specified user by user name in a cognito user pool


    try:

        kyc_update_response = client.admin_update_user_attributes(
            UserPoolId= os.environ['USER_POOL_ID'],
            Username= user_id,
            UserAttributes=[
                {
                    'Name': 'custom:kyc',
                    'Value': 'true'
                }
                ]
        )

        return {
            "statusCode": 201
        }
    except ParamValidationError as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({
                "message": "invalid input"
            }) }
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({
                "message": "unable to update user kyc status"
            }) }




