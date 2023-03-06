

To Deploy from local:

1. Install docker and sam cli: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

2. Install AWS SSO Export util: https://github.com/benkehoe/aws-sso-util

3. Verify the below in ~/.aws/config:

[profile athena-ksolves]
sso_start_url = https://athenabitcoin.awsapps.com/start/
sso_region = us-west-2
sso_account_id = 294175892778
sso_role_name = AdministratorAccess
region = us-west-2
output = json

4. run:

aws-sso-util login --profile athena-ksolves
sam build --use-container
sam deploy --config-env dev
