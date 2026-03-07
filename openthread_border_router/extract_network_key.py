#!/usr/bin/env python3
"""
Thread Dataset TLV Parser and Network Key Extractor
Extract Thread network credentials from Active Dataset TLVs
"""


def parse_tlv_dataset(dataset_hex):
    """Parse Thread dataset TLVs and extract network key"""

    # Remove any whitespace
    dataset_hex = dataset_hex.replace(" ", "").replace("\n", "")

    print("Thread Dataset TLV Parser")
    print("=" * 60)
    print()
    print("Parsing TLVs...")
    print()

    pos = 0
    network_key = None
    network_name = None
    channel = None
    pan_id = None
    extended_pan_id = None

    while pos < len(dataset_hex):
        # Read Type (1 byte = 2 hex chars)
        tlv_type = dataset_hex[pos : pos + 2]
        pos += 2

        # Read Length (1 byte = 2 hex chars)
        length_hex = dataset_hex[pos : pos + 2]
        pos += 2

        # Convert length to decimal
        length = int(length_hex, 16)
        value_chars = length * 2  # Each byte = 2 hex chars

        # Read Value
        value = dataset_hex[pos : pos + value_chars]
        pos += value_chars

        # Decode specific TLV types
        if tlv_type == "05":  # Network Key
            network_key = value
            print(f"✓ Network Key (Master Key): {network_key}")

        elif tlv_type == "03":  # Network Name (+ possibly channel/PAN ID)
            # Network name is printable ASCII at the start
            name_bytes = bytes.fromhex(value[: min(32, len(value))])
            name = ""
            for byte in name_bytes:
                if 32 <= byte <= 126:  # Printable ASCII
                    name += chr(byte)
                else:
                    break
            if name:
                network_name = name
                print(f"✓ Network Name: {network_name}")

        elif tlv_type == "00":  # Channel
            if length == 3:
                channel = int(value[4:6], 16)  # Last byte is channel
                print(f"✓ Channel: {channel}")

        elif tlv_type == "01":  # PAN ID
            pan_id = value
            print(f"✓ PAN ID: 0x{pan_id}")

        elif tlv_type == "02":  # Extended PAN ID
            extended_pan_id = value
            print(f"✓ Extended PAN ID: {extended_pan_id}")

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if network_key:
        print(f"Network Key: {network_key}")
        print()
        print("Use this in OTBR Web UI to manually join the network.")
    else:
        print("⚠ Network Key (Type 0x05) not found in dataset!")

    if network_name:
        print(f"Network Name: {network_name}")
    if channel:
        print(f"Channel: {channel}")
    if pan_id:
        print(f"PAN ID: 0x{pan_id}")
    if extended_pan_id:
        print(f"Extended PAN ID: {extended_pan_id}")


def main():
    print()
    print("Thread Dataset Network Key Extractor")
    print("=" * 60)
    print()
    print("Paste your Active dataset TLVs from Home Assistant:")
    print("(Get from: Settings > Devices & Services > Thread > [Network])")
    print()

    dataset = input("Dataset TLVs: ").strip()

    if not dataset:
        print("No dataset provided.")
        return

    print()
    parse_tlv_dataset(dataset)
    print()


if __name__ == "__main__":
    main()
