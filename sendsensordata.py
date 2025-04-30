import boto3
from datetime import datetime, timezone
from decimal import Decimal
import time

# --- AWS SETUP ---
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('SensorData')

# --- Dummy payload to test full app display ---
dummy_payload = {
    'sensor_id': 'home_node_1',
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'temp': Decimal("72.5"),
    'reed_front': 'closed',
    'reed_back': 'open',
    'reed_garage': 'closed',
    'reed_window': 'open',
    'ir_sensor': 'NoObject'
}

def send_dummy():
    try:
        response = table.put_item(Item=dummy_payload)
        print("✅ Sent dummy data to DynamoDB.")
    except Exception as e:
        print("❌ Error sending dummy data:", e)

if __name__ == "__main__":
    while True:
        send_dummy()
        time.sleep(5)  # Send every 5 seconds
