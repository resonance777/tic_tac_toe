# Name: Ruslan Sabitov
# Matriculation Number: 99774243
# Project Title: Visualizing Data Flow Through the OSI Model
# Subject: IT Platform
# Task: Mini Project


import random
import hashlib
import base64

#  APPLICATION LAYER 
def application_layer():
    print("\n--- Application Layer ---")
    message = input("Enter your message: ")

    print("\n[Application Protocol: HTTP]")
    print("POST /send-message HTTP/1.1")
    print("Host: chat.example.com")
    print("Content-Type: text/plain")
    print(f"Content-Length: {len(message)}")
    print("Message Body:", message)

    return message

#  PRESENTATION LAYER
def presentation_layer(message):
    print("\n--- Presentation Layer ---")

    encrypted = base64.b64encode(message.encode()).decode()
    encoded = encrypted.encode("utf-8")

    print("Encrypted (Base64):", encrypted)
    print("Encoded (UTF-8):", encoded)

    return encoded

#SESSION LAYER 
def session_layer(data):
    print("\n--- Session Layer ---")

    session_id = f"SESSION-{random.randint(1000,9999)}"
    combined = session_id + "::" + data.decode()

    print("Session ID:", session_id)
    print("Session Data:", combined)

    return combined

# TRANSPORT LAYER
def transport_layer(data):
    print("\n--- Transport Layer ---")

    segments = []
    port = random.randint(1024, 65535)

    for i in range(0, len(data), 10):
        segment_data = data[i:i+10]
        checksum = hashlib.md5(segment_data.encode()).hexdigest()[:6]

        segment = {
            "segment_no": i // 10,
            "port": port,
            "data": segment_data,
            "checksum": checksum
        }

        segments.append(segment)
        print(segment)

    return segments

#NETWORK LAYER
def network_layer(segments):
    print("\n--- Network Layer ---")

    source_ip = "192.168.1.2"
    dest_ip = "192.168.1.10"

    packets = []

    for seg in segments:
        packet = {
            "src_ip": source_ip,
            "dest_ip": dest_ip,
            "segment": seg
        }
        packets.append(packet)
        print(packet)

    return packets

#DATA LINK LAYER
def data_link_layer(packets):
    print("\n--- Data Link Layer ---")

    source_mac = "AA:BB:CC:DD:EE:01"
    dest_mac = "FF:GG:HH:II:JJ:02"

    frames = []

    for pkt in packets:
        frame = {
            "src_mac": source_mac,
            "dest_mac": dest_mac,
            "packet": pkt
        }
        frames.append(frame)
        print(frame)

    return frames

# PHYSICAL LAYER
def physical_layer(frames):
    print("\n--- Physical Layer ---")
    print("[Binary Transmission]")

    for frame in frames:
        binary = " ".join(format(ord(c), "08b") for c in str(frame))
        print(binary)


#  PHYSICAL LAYER (BACKWARD) 
def physical_layer_backward(frames):
    print("\n--- Physical Layer (Backward) ---")
    print("Binary received → Frame data restored")
    return frames


#  DATA LINK LAYER (BACKWARD) 
def data_link_layer_backward(frames):
    print("\n--- Data Link Layer (Backward) ---")
    packets = []
    for frame in frames:
        packets.append(frame["packet"])
    print("MAC addresses removed")
    return packets


#  NETWORK LAYER (BACKWARD) 
def network_layer_backward(packets):
    print("\n--- Network Layer (Backward) ---")
    segments = []
    for packet in packets:
        segments.append(packet["segment"])
    print("IP addresses removed")
    return segments


#  TRANSPORT LAYER (BACKWARD) 
def transport_layer_backward(segments):
    print("\n--- Transport Layer (Backward) ---")

    segments_sorted = sorted(segments, key=lambda x: x["segment_no"])
    data = ""

    for seg in segments_sorted:
        checksum = hashlib.md5(seg["data"].encode()).hexdigest()[:6]
        if checksum == seg["checksum"]:
            print(f"Segment {seg['segment_no']} checksum OK")
            data += seg["data"]
        else:
            print(f"Segment {seg['segment_no']} checksum ERROR")

    return data


#  SESSION LAYER (BACKWARD) 
def session_layer_backward(data):
    print("\n--- Session Layer (Backward) ---")
    session_id, message = data.split("::", 1)
    print("Session closed:", session_id)
    return message


#  PRESENTATION LAYER (BACKWARD) 
def presentation_layer_backward(data):
    print("\n--- Presentation Layer (Backward) ---")
    decoded = base64.b64decode(data).decode("utf-8")
    print("Decoded & decrypted")
    return decoded


# APPLICATION LAYER (BACKWARD) 
def application_layer_backward(message):
    print("\n--- Application Layer (Backward) ---")
    print("Final Delivered Message:")
    print(message)

def main():
    # FORWARD
    msg = application_layer()
    pres = presentation_layer(msg)
    sess = session_layer(pres)
    trans = transport_layer(sess)
    net = network_layer(trans)
    link = data_link_layer(net)
    physical_layer(link)

    # BACKWARD
    frames = physical_layer_backward(link)
    packets = data_link_layer_backward(frames)
    segments = network_layer_backward(packets)
    data = transport_layer_backward(segments)
    session_data = session_layer_backward(data)
    final_message = presentation_layer_backward(session_data)
    application_layer_backward(final_message)


if __name__ == "__main__":
    main()



