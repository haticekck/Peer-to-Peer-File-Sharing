import socket
import json


def content_discovery():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to listen for incoming messages
    sock.bind(('', 5001))

    print("Content Discovery is listening for UDP broadcast messages...")

    # Create the content dictionary to store file information
    content_dict = {}

    while True:
        # Receive the broadcast message and the sender's address
        message, address = sock.recvfrom(1024)

        # Decode the received message from bytes to string
        message = message.decode()

        try:
            # Parse the JSON message
            data = json.loads(message)

            # Extract the chunks information from the parsed data
            chunks = data.get("chunks", [])

            # Update the content dictionary with the file information
            for chunk in chunks:
                if chunk in content_dict:
                    content_dict[chunk].append(address[0])
                else:
                    content_dict[chunk] = [address[0]]

            # Display the detected user and their hosted content on the console
            display_detected_user(address[0], content_dict)

            # Write the content dictionary to the shared text file
            write_content_dict_to_file(content_dict)

        except json.JSONDecodeError:
            print("Invalid JSON message received")
            print("------------------------")


def display_detected_user(ip_address, content_dict):
    hosted_content = [chunk for chunk, addresses in content_dict.items() if ip_address in addresses]
    if hosted_content:
        print(f"Detected User: {ip_address} - Hosted Content: {', '.join(hosted_content)}")
        print("------------------------")


def write_content_dict_to_file(content_dict):
    with open('content_dictionary.txt', 'w') as file:
        for chunk, addresses in content_dict.items():
            file.write(f"{chunk}: {', '.join(addresses)}\n")


content_discovery()
