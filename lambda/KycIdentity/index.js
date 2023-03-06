
const aws = require('aws-sdk');
const https = require('https');

/**
 * @type {import('@types/aws-lambda').APIGatewayProxyHandler}
 */

function postRequest(jumio_user, jumio_token,body) {
  const options = {
    hostname: 'netverify.com',
    path: '/api/v4/initiate',
    method: 'POST',
    port: 443,
    headers: {
      "Accept": 'application/json',
      "Content-Type": 'application/json',
      "Authorization": 'Basic ' + new Buffer(jumio_user + ':' + jumio_token).toString('base64'),
      "User-Agent": 'AthenaMexOnboarding',
      "Access-Control-Allow-Origin": '*'
    },
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, res => {
      let rawData = '';

      res.on('data', chunk => {
        rawData += chunk;
      });

      res.on('end', () => {
        try {
          resolve(JSON.parse(rawData));
        } catch (err) {
          reject(new Error(err));
        }
      });
    });

    req.on('error', err => {
      reject(new Error(err));
    });

    req.write(JSON.stringify(body));
    req.end();
  });
}



exports.handler = async (event) => {

  const userPhone = event['queryStringParameters']['user']

  let body = {
    "customerInternalReference": userPhone,
    "userReference": userPhone,
    "reportingCriteria": null,
    "successUrl": "https://onboarding.athenabitcoin.net/callbacks/jumio/success",
    "errorUrl": "https://onboarding.athenabitcoin.net/callbacks/jumio/error",
    "callbackUrl": "https://onboarding.athenabitcoin.net/callbacks/jumio/callback",
    "workflowId": 100,
    "locale": "es-MX",
    "tokenLifetimeInMinutes": 90
  }

  const { Parameters } = await (new aws.SSM())
  .getParameters({
    Names: ["JUMIO_TOKEN","JUMIO_USER"].map(secretName => process.env[secretName]),
    WithDecryption: true,
  })
  .promise();


  console.log(Parameters.toString())

  const JUMIO_TOKEN = Parameters.pop().Value;
  const JUMIO_USER = Parameters.pop().Value;



  try {
    const result = await postRequest(JUMIO_TOKEN, JUMIO_USER, body);
    console.log(result);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Headers' : 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': "OPTIONS,POST,GET"
      },
      body: JSON.stringify(result),
    };
  } catch (error) {
    console.log(error);
    return {
      statusCode: 400,
      body: error.message,
    };
  }
/*
      const response = {
        statusCode: 200,
        body: `JUMIO_TOKEN: ${JUMIO_TOKEN}, JUMIO_USER: ${JUMIO_USER}`
      };
      return response;
      */

};
