import boto3
import json
import uuid
import datetime
import random

sqs_client = boto3.client('sqs')
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/590184043718/AirbnbBookingQueue'


def generate_random_string(length):
    """Generates a random string of alphanumeric characters."""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(chars) for i in range(length))


def generate_booking_data():
    """Generates a dictionary of mock booking data."""
    # Generate start date first
    while True:
        potential_start_date = (datetime.date.today() + datetime.timedelta(days=random.randint(-30, 30)))
        try:
            datetime.datetime.strptime(potential_start_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
            break  # Valid date found, break the loop
        except ValueError:
            pass  # Try again if invalid date format

    return {
        "bookingId": str(uuid.uuid4()),  # Generate a unique UUID
        "userId": generate_random_string(10),  # Random user ID
        "propertyId": f"PID-{random.randint(10000, 99999)}",  # Random property ID
        "location": f"{generate_random_string(8)}, {generate_random_string(7)}",  # Random city and country
        "startDate": potential_start_date.strftime("%Y-%m-%d"),
        "endDate": (datetime.datetime.strptime(potential_start_date.strftime("%Y-%m-%d"),
                                               "%Y-%m-%d") + datetime.timedelta(days=random.randint(1, 15))).strftime(
            "%Y-%m-%d"),  # Random end date 1-15 days after start date
        "price": random.randint(10, 5000),  # Random price between $10 and $5000
    }


def lambda_handler(event, context):
    # TODO implement
    # Example usage:
    i = 0
    while (i < 5):
        booking_data = generate_booking_data()
        print(booking_data)
        sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(booking_data)
        )
        i += 1

    return {
        'statusCode': 200,
        'body': json.dumps('Airbnb data published to SQS!')
    }
