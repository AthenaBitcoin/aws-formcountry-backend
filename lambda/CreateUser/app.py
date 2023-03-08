import json
import  boto3
import os
from botocore.exceptions import ClientError

# client representing Amazon Cognito Identity Provider
client = boto3.client('cognito-idp')



def get_jumio_token(user_id):
    return "temp_jumio_token"

def lambda_handler(event, context):
    response_dict = {}
    print(json.dumps(event))

    try:
        event_body=json.loads(event['body'])
        phone_number=event_body['phone_number']
        email=event_body['email']
        address=event_body['address']
    except Exception as e:
        print(e)
        return {"statusCode": 400, "body": json.dumps({
                "message": "Invalid Input"
            }) }



    ######If given phone number is exist in the congnito user pool,get user id and kyc details
    try:
        print("Getting the exist cognito user")
        get_user_find_response = client.admin_get_user(
            UserPoolId=os.environ['USER_POOL_ID'],
            Username= phone_number
        )
        response_dict["user_id"] = get_user_find_response['Username']
        for i in get_user_find_response['UserAttributes']:

            if 'custom:kyc' == i['Name']:
                # print("exist")
                response_dict['kyc'] = i['Value']

                if i['Value']=='false':
                    response_dict['kyc_token'] = get_jumio_token(response_dict["user_id"])


    #####If given phone number is not exist in the congnito user pool,Creates a new user in the specified user pool.
    except Exception as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            print("Creating the cognito user")
            create_user_response = client.admin_create_user(
                UserPoolId=os.environ['USER_POOL_ID'],
                Username= phone_number,
                UserAttributes=[
                    {
                        'Name': 'custom:kyc',
                        'Value': 'false'
                    },
                    {
                        'Name': 'email',
                        'Value': email
                    },
                    {
                        'Name': 'address',
                        'Value': address
                    }
                ])
            response_dict['user_id'] = create_user_response['User']['Username']

            response_dict['kyc_token'] = get_jumio_token(response_dict["user_id"])


            for i in create_user_response['User']['Attributes']:
                if 'custom:kyc' == i['Name']:
                    response_dict['kyc'] = i['Value']

    return {
        "statusCode": 200,
        "body": json.dumps(response_dict)
    }




