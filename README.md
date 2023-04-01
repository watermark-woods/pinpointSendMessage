# pinpointSendMessage
A simple python lambda function to send a text via lambda for use with amazon connect

# Environment
## Runtime Settings
Python 3.9 with no layers any architecure works fine (arm64 is recommended for the lower cost)
## Permissions
In IAM create a inline policy for the auto created role for your new function 
this inline policy should have the following json set be sure to fill in your AWS Account ID
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "mobiletargeting:SendMessages",
            "Resource": "arn:aws:mobiletargeting:*:[AWS-ACCOUNT-ID]:apps/*"
        }
    ]
}
```

## Environment variables
| name | value |
| -- | -- |
| source_number | your pinpoint sms number |
| pinpoint_appid | your pinpoit app id |
