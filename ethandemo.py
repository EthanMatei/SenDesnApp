import asyncio
import json
from bleak import BleakClient, BleakScanner
import boto3
from datetime import datetime, timezone
from decimal import Decimal

# --- AWS DynamoDB Setup ---
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('SensorData')

# --- BLE UUIDs ---
ESP_NAME = "ESP32_BLE_Front"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHAR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

# --- Global state ---
latest_reed = "unknown"

def send_to_aws():
    try:
        item = {
            'sensor_id': 'home_node_1',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'temp': Decimal("72.5"),
            'reed_front': latest_reed,
            'reed_back': "closed",
            'reed_garage': "closed",
            'reed_window': "closed"
        }

        table.put_item(Item=item)
        print("✅ Sent to AWS:", item)

    except Exception as e:
        print("❌ Error sending to DynamoDB:", e)

# --- BLE Notification Handler ---
def notification_handler(sender, data):
    global latest_reed
    try:
        decoded = data.decode()
        print("📨 Notification:", decoded)
        payload = json.loads(decoded)
        if 'reed_front' in payload:
            latest_reed = payload['reed_front']
            send_to_aws()
    except Exception as e:
        print("❌ Failed to parse notification:", e)

# --- Main BLE Loop ---
async def main():
    print("🔍 Scanning for ESP32...")
    devices = await BleakScanner.discover()
    address = None

    for d in devices:
        if d.name == ESP_NAME:
            address = d.address
            print(f"✅ Found {ESP_NAME} at {address}")
            break

    if not address:
        print("❌ ESP32 not found.")
        return

    async with BleakClient(address) as client:
        print("✅ Connected to ESP32. Listening for notifications...")
        await client.start_notify(CHAR_UUID, notification_handler)

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("👋 Exiting...")
            await client.stop_notify(CHAR_UUID)

if __name__ == "__main__":
    asyncio.run(main())
