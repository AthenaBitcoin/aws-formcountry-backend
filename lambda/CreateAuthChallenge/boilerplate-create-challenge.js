/**
 * @type {import('@types/aws-lambda').CreateAuthChallengeTriggerHandler}
 */
/* tslint:disable */
/* eslint-disable */
const AWS = require('aws-sdk');

exports.handler = (event, context, callback) => {
  //Create a random number for otp
  const challengeAnswer = Math.random().toString(10).substr(2, 6);
  const phoneNumber = event.request.userAttributes.phone_number;

  //For Debugging
  console.log(event, context);

  //sns sms
  const sns = new AWS.SNS({ region: 'us-east-1' });

  let parameters = {
    Message: 'Athena Bitcoin - código es: ' + challengeAnswer,
      PhoneNumber: phoneNumber,
      MessageStructure: 'string',
      MessageAttributes: {
        'AWS.SNS.SMS.SenderID': {
          DataType: 'String',
          StringValue: 'AMPLIFY',
        },
        'AWS.SNS.SMS.SMSType': {
          DataType: 'String',
          StringValue: 'Transactional',
        },
      },
    };

  sns.publish(parameters, function (err, data) {
      if (err) {
        console.log(err.stack);
        console.log(data);
        return;
      }
      console.log(`SMS sent to ${phoneNumber} and otp = ${challengeAnswer}`);
      console.log(data)
      return data;
    });

  //set return params
  event.response.privateChallengeParameters = {};
  event.response.privateChallengeParameters.answer = challengeAnswer;
  event.response.challengeMetadata = 'CUSTOM_CHALLENGE';

  callback(null, event);
};
