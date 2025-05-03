import meshtastic
import meshtastic.serial_interface
import time
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)

def on_receive(packet):
    logging.debug(f"Received packet: {packet}")
    try:
        if 'decoded' in packet:
            text = packet['decoded'].get('text', '')
            logging.debug(f"Decoded text: {text}")

            if text.startswith("!cmd "):
                command = text[5:]  # Strip '!cmd '
                logging.debug(f"Executing command: {command}")

                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                except subprocess.CalledProcessError as e:
                    output = e.output  # Capture errors too

                logging.debug(f"Command output: {output}")
                iface.sendText(output[:230])  # Truncate to fit LoRa message size

            else:
                logging.debug("Received text does not start with '!cmd '")
        else:
            logging.debug("Packet has no 'decoded' field.")
    except Exception as e:
        logging.error(f"Exception in on_receive: {e}")

iface = meshtastic.serial_interface.SerialInterface()
iface.onTextMessage = on_receive

logging.info("LoRpi Receiver is running...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Receiver stopped by user.")
