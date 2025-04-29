import json
import boto3
import asyncio
from bleak import BleakClient, BleakScanner

# BLE Setup
ESP_NAME = "ESP32_BLE_Cam"  # Name of the garage ESP32 device
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
DATA_CHAR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

# AWS SQS Setup
sqs = boto3.client('sqs', region_name='us-east-2')
queue_url = "https://sqs.us-east-2.amazonaws.com/829293890820/garage-door-control"

# Message processing loop
async def process_messages():
    print("🔁 Starting control listener loop...")
    esp_address = None

    # Scan for the garage ESP32
    print("🔍 Scanning for ESP32...")
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == ESP_NAME:
            esp_address = d.address
            print(f"✅ Found ESP32 at {esp_address}")
            break

    if not esp_address:
        print("❌ ESP32 not found. Exiting.")
        return

    async with BleakClient(esp_address) as client:
        print("✅ Connected to ESP32 BLE device.")

        # Ensure service discovery is performed
        await client.get_services()

        while True:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10
            )

            messages = response.get('Messages', [])
            if messages:
                for msg in messages:
                    print("📨 Received SQS Message:", msg['Body'])

                    try:
                        body = json.loads(msg['Body'])  # Parse the JSON body
                        command = body.get('command', '').strip().lower()

                        if command == "unlock":
                            print("🔓 Sending 'OPEN' BLE command to ESP32...")
                            await client.write_gatt_char(DATA_CHAR_UUID, b"OPEN")
                        else:
                            print(f"⚠️ Unknown command: {command}")

                        # Delete message after processing
                        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg['ReceiptHandle'])
                        print("🗑️ Deleted message from queue.")

                    except Exception as e:
                        print(f"❌ Failed to process message: {e}")

            await asyncio.sleep(1)

# Entry point
if __name__ == "__main__":
    asyncio.run(process_messages())
