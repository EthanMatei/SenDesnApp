import boto3
from datetime import datetime
from decimal import Decimal

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')  # Change region if needed
table = dynamodb.Table('SensorData')

# Simulate sensor data
def send_data(sensor_id, value):
    response = table.put_item(
        Item={
            'sensor_id': sensor_id,
            'timestamp': datetime.now().isoformat(),
            'value': Decimal(str(value))  # ✅ Wrap float in Decimal
        }
    )
    print("Data sent:", response)

# Example usage
send_data('temp_sensor_1', 23.7)
