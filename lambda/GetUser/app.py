import json
import  boto3
import os 
from botocore.exceptions import ClientError


# client representing Amazon Cognito Identity Provider
client = boto3.client('cognito-idp')


def get_jumio_token(user_id):
    return "temp_jumio_token"


def lambda_handler(event, context):


    result_dict = {}
    print(json.dumps(event))
    
    try:
        # TODO: How to pass phone number with + in query string
        number=int(event['queryStringParameters']['phone_number'])
        phone_number = f'{number:+}'
    except Exception as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({
                "message": "Invalid Input"
            }) }

    ######Gets the specified user by user name in a cognito user pool


    try:

        get_user_find_response = client.admin_get_user(
            UserPoolId= os.environ['USER_POOL_ID'],
            Username= phone_number
        )
        result_dict["user_id"] = get_user_find_response['Username']
        for i in get_user_find_response['UserAttributes']:

            if 'custom:kyc' == i['Name']:
                result_dict['kyc'] = i['Value']

                if i['Value']=='false':
                    result_dict['kyc_token'] = get_jumio_token(result_dict["user_id"])

        return {
            "statusCode": 200,
            "body": json.dumps(result_dict)
        }
    except Exception as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            return {"statusCode": 404}
        return {"statusCode": 500, "body": json.dumps({
                "message": "unable to fetch the user details"
            }) }




