import json
import boto3
import asyncio
from bleak import BleakClient, BleakScanner
from datetime import datetime, timezone
from decimal import Decimal

# --- BLE Setup ---
ESP_NAME = "ESP32_BLE_Cam"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
DATA_CHAR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

# --- AWS Setup ---
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('SensorData')

sqs = boto3.client('sqs', region_name='us-east-2')
queue_url = "https://sqs.us-east-2.amazonaws.com/829293890820/garage-door-control"

# --- State ---
latest_data = {
    'temp': 0.0,
    'reed_front': 'closed',
    'reed_back': 'closed',
    'reed_window': 'closed',
    'reed_garage': 'closed',
    'ir_sensor': 'NoObject'
}
last_sent_data = {}

# --- BLE Notification Handler ---
def notification_handler(sender, data):
    decoded = data.decode()
    print(f"📡 Notification received: {decoded}")
    try:
        parsed = json.loads(decoded)
        if "tempC" in parsed:
            latest_data['temp'] = float(parsed['tempC'])
        if "irSensor" in parsed:
            latest_data['ir_sensor'] = parsed['irSensor']
    except Exception as e:
        print(f"❌ Failed to parse notification: {e}")

# --- Send to DynamoDB if changed ---
def send_to_aws():
    global last_sent_data
    if latest_data != last_sent_data:
        try:
            payload = {
                'sensor_id': 'home_node_1',
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'temp': Decimal(str(latest_data['temp'])),
                'reed_front': latest_data['reed_front'],
                'reed_back': latest_data['reed_back'],
                'reed_garage': latest_data['reed_garage'],
                'reed_window': latest_data['reed_window'],
                'ir_sensor': latest_data['ir_sensor']
            }
            table.put_item(Item=payload)
            last_sent_data = latest_data.copy()
            print("✅ Sent data to AWS:", payload)
        except Exception as e:
            print("❌ DynamoDB Error:", e)
    else:
        print("🔁 No data change.")

# --- BLE + SQS Main ---
async def main():
    print("🔍 Scanning for ESP32 BLE device...")
    esp_address = None

    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == ESP_NAME:
            esp_address = d.address
            print(f"✅ Found {ESP_NAME} at {esp_address}")
            break

    if not esp_address:
        print("❌ ESP32 not found.")
        return

    async with BleakClient(esp_address) as client:
        print("✅ Connected to ESP32 BLE device.")
        await client.get_services()
        await client.start_notify(DATA_CHAR_UUID, notification_handler)

        while True:
            send_to_aws()

            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=5
            )

            messages = response.get('Messages', [])
            if messages:
                for msg in messages:
                    print("📨 Received SQS Message:", msg['Body'])
                    try:
                        body = json.loads(msg['Body'])
                        command = body.get('command', '').strip().lower()
                        if command == 'unlock':
                            print("🔓 Sending 'OPEN' BLE command to ESP32...")
                            await client.write_gatt_char(DATA_CHAR_UUID, b"OPEN")
                        else:
                            print(f"⚠️ Unknown command: {command}")
                        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg['ReceiptHandle'])
                        print("🗑️ Deleted message from queue.")
                    except Exception as e:
                        print(f"❌ Failed to process message: {e}")

            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
