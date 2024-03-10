import os
import json
import socket
from datetime import datetime

CONTENT_DICT_FILE = "content_dictionary.txt"


def load_content_dictionary():
    content_dict = {}
    with open(CONTENT_DICT_FILE, 'r') as dict_file:
        lines = dict_file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                content_name, ip = line.split(':')
                content_dict[content_name] = [chunk.strip() for chunk in ip.split(',')]
    return content_dict


def download_chunk(ip_address, chunk_name):
    BUFFER_SIZE = 2000000000
    try:
        # Create a TCP socket and connect to the peer
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, 5000))

        # Prepare the JSON message with the requested content name
        message = json.dumps({"requested_content": chunk_name}).encode()

        # Send the request to the peer
        client_socket.send(message)

        # Receive the chunk data from the peer
        data = client_socket.recv(BUFFER_SIZE)

        # Check if the chunk was successfully received
        if data:
            # Save the chunk to the appropriate directory
            chunk_path = os.path.join(".", chunk_name)
            with open(chunk_path, 'wb') as chunk_file:
                chunk_file.write(data)
                client_socket.close()
            return True

        else:
            return None

    except Exception as e:
        print(f"An error occurred while downloading chunk {chunk_name}: {e}")
        return None


def merge_chunks(file_name):
    merged_file_path = f"./{file_name}1.png"
    with open(merged_file_path, 'wb') as merged_file:
        for k in range(1, 6):
            chunk_path = f"./{file_name}_{k}"
            with open(chunk_path, 'rb') as chunk:
                merged_file.write(chunk.read())
            os.remove(chunk_path)
    return merged_file_path


def log_download(file_name, ip_address):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: {file_name} downloaded from {ip_address}\n"
    with open("download_log.txt", 'a') as log_file:
        log_file.write(log_entry)


if __name__ == "__main__":
    content_dict = load_content_dictionary()

    content_name = input("Enter the content filename: ")
    filename = content_name + '.png'
    for i in range(1, 6):
        chunk_name = f"{content_name}_{i}"
        ip_addresses = content_dict.get(chunk_name, [])
        downloaded = False

        for ip_address in ip_addresses:
            if download_chunk(ip_address, chunk_name):
                downloaded = True
                log_download(chunk_name, ip_address)
                break

        if not downloaded:
            print(f"CHUNK {chunk_name} CANNOT BE DOWNLOADED FROM ONLINE PEERS.")
            continue

    merge_chunks(content_name)
    print(f"File {content_name} has been successfully downloaded and merged.")
