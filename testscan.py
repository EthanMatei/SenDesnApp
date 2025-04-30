import asyncio
from bleak import BleakScanner

async def scan():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover(timeout=5.0)
    if devices:
        for d in devices:
            print(f"{d.name} - {d.address}")
    else:
        print("No devices found.")

asyncio.run(scan())
