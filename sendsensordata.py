import boto3
from datetime import datetime, timezone
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('SensorData')

def send_data(temp, front, back, garage, window):
    response = table.put_item(
        Item={
            'sensor_id': 'home_node_1',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'temp': Decimal(str(temp)),
            'reed_front': front,
            'reed_back': back,
            'reed_garage': garage,
            'reed_window': window
        }
    )
    print("Data sent:", response)

# Simulated reading
send_data(61.5, 'open', 'closed', 'open', 'closed')





