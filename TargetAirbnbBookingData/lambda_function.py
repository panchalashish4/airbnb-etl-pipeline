import boto3
import json

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    # TODO implement
    print(event)
    body = event[0]["body"]
    print(body)

    # Create a temporary filename
    output_file = f"/tmp/filtered_data_{body["bookingId"]}"

    # Write filtered data to temporary file
    with open(output_file, 'w') as f:
        json.dump([body], f, indent=4)

    # Upload filtered data to the target S3 bucket
    target_bucket_name = "doordash-target-zn-assign3"  # Replace with your target bucket name
    s3_client.upload_file(output_file, target_bucket_name,
                          f"filtered_airbnb/filtered_{body["bookingId"]}")  # Upload to a subfolder "filtered"

    print(
        f"Filtered data written to {output_file} and uploaded to S3 bucket: {target_bucket_name}/filtered_airbnb/{body["bookingId"]}")

    return {
        'statusCode': 200,
        'body': json.dumps(f'File uploaded to S3 bucket: {target_bucket_name}/filtered_airbnb/{body["bookingId"]}')
    }
