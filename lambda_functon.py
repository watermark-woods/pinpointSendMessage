import json
import logging
import os
import boto3
from botocore.exceptions import ClientError

env_var = os.environ

origination_number = env_var["source_number"]
app_id = env_var["pinpoint_appid"]
pinpoint = boto3.client('pinpoint')

logger = logging.getLogger(__name__)

def send_sms_message(destination_number, message, message_type):
    """
    Sends an SMS message with Amazon Pinpoint.

    :param pinpoint_client: A Boto3 Pinpoint client.
    :param app_id: The Amazon Pinpoint project/application ID to use when you send
                   this message. The SMS channel must be enabled for the project or
                   application.
    :param destination_number: The recipient's phone number in E.164 format.
    :param origination_number: The phone number to send the message from. This phone
                               number must be associated with your Amazon Pinpoint
                               account and be in E.164 format.
    :param message: The content of the SMS message.
    :param message_type: The type of SMS message that you want to send. If you send
                         time-sensitive content, specify TRANSACTIONAL. If you send
                         marketing-related content, specify PROMOTIONAL.
    :return: The ID of the message.
    """
    try:
        response = pinpoint.send_messages(
            ApplicationId=app_id,
            MessageRequest={
                'Addresses': {destination_number: {'ChannelType': 'SMS'}},
                'MessageConfiguration': {
                    'SMSMessage': {
                        'Body': message,
                        'MessageType': message_type,
                        'OriginationNumber': origination_number}}})
    except ClientError:
        logger.exception("Couldn't send message.")
        raise
    else:
        return response['MessageResponse']['Result'][destination_number]['MessageId']


def lambda_handler(event, context):
    message_data = event.get("Details").get("Parameters")
    if message_data:
        logger.info(json.dumps(message_data))
        
        destination_number = message_data.get("destinationNumber")
        message = message_data.get("messageContent")
        if message and destination_number:
            message_type = "TRANSACTIONAL"
        
            logger.info("Sending SMS message.")
            message_id = send_sms_message(
                destination_number,
                message, 
                message_type
            )
            logger.info(f"Message sent! Message ID: {message_id}.")
    
            return 200
        else:
            logger.error("expected data not found")
            return 400
    else:
        logger.error("invalid data sent")
        return 400
