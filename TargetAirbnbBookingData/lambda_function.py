import json
from datetime import datetime


def lambda_handler(event, context):
    """Lambda function to process event and return message with duration."""

    print("Event: ", event)
    # Get the message body from the event
    body = json.loads(event[0]["body"])

    # Extract start and end dates from the message
    start_date_str = body.get("startDate")
    end_date_str = body.get("endDate")

    # Check if both dates are present
    if not start_date_str or not end_date_str:
        return {
            "statusCode": 400,
            "body": "Missing start or end date in message."
        }

    # Try converting dates to datetime objects
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        return {
            "statusCode": 400,
            "body": "Invalid date format. Use YYYY-MM-DD."
        }

    # Calculate duration in days
    duration = (end_date - start_date).days

    response_data = {**body, "duration": duration}

    # Return message only if duration is greater than 1
    if duration > 1:
        print("Response Data: ", response_data)
        return {
            "statusCode": 200,
            "body": response_data
        }
