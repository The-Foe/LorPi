**LoRpi Project: Remote Command Execution via Meshtastic LoRa Network**

---

## Overview
The LoRpi Project enables remote command execution on a Raspberry Pi using a pair of MakerHawk ESP32 LoRa V3 development boards running Meshtastic firmware. One ESP32 board is connected to a Raspberry Pi via USB ("LorpiNode"), while the other is controlled from a smartphone via the Meshtastic app ("LorpiPhone"). Commands prefixed with `!cmd` sent from the phone are executed on the Raspberry Pi, and the results are returned over the LoRa mesh network.

---

## Hardware Requirements
- 2x ESP32 LoRa V3 development boards
- 1x Raspberry Pi (Tested with Raspberry Pi 4 Model B running Raspberry Pi OS 64bit Bookworm port)
- USB cables appropriate for your devices
- Smartphone with BLE (Can use a serial cable instead)

---

## Software Requirements
- Meshtastic firmware installed on both ESP32 boards
- Meshtastic app (iOS/Android)
- Python 3.7+ on Raspberry Pi
- `meshtastic` Python package (`pip install meshtastic`) on Raspberry Pi

---

## Setup Instructions

### 1. Flash Meshtastic Firmware
- Use the official Meshtastic flasher tool or esptool to flash both ESP32 LoRa V3 boards with the latest Meshtastic firmware.

### 2. Configure the Mesh Network
- Open the Meshtastic app on your phone and pair it with one ESP32 via BLE.
- Set a channel name (e.g., `Lorpimesh`) and generate a PSK.
- Apply this same channel and PSK to both ESP32 nodes.
- Rename the nodes:
  - Smartphone-side ESP32: (e.g., `LorpiPhone`)
  - Raspberry Pi-side ESP32: (e.g., `LorpiNode`)

### 3. Connect LorpiNode to Raspberry Pi
- Plug `LorpiNode` into the Raspberry Pi using a USB cable.
- Verify it shows up as `/dev/ttyUSB0` or similar using `dmesg | grep tty`

### 4. Install Python Dependencies
```bash
sudo apt update
sudo apt install python3-pip
pip3 install meshtastic
```

### 5. Deploy the Receiver Script
- Save the working Python script as `lorpi_receiver.py`
- Make it executable:
```bash
chmod +x lorpi_receiver.py
```
- Run the script:
```bash
python3 lorpi_receiver.py
```

### 6. Send Commands from Phone
- Open the Meshtastic app and send a text message like:
```
!cmd whoami
```
- The Raspberry Pi will execute the command and send the response back to the Meshtastic network.

---

## Notes
- Commands must start with `!cmd ` to be recognized.
- Output will be truncated if it exceeds the LoRa packet size limit (~250 bytes).
- It is advisable to implement command filtering and logging for security.

---

## Future Improvements
- Add command whitelisting
- Split large command outputs across multiple packets
- Log command execution history to file
- Convert the Python script into a systemd service to start on boot

