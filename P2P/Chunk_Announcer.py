import os
import json
import time
import math
from socket import *

content_name = 'cherry'
file_name = content_name + '.png'
BROADCAST_IP = '192.168.2.255'
c = os.path.getsize(file_name)
# print(c)
CHUNK_SIZE = math.ceil(math.ceil(c) / 5)


# print(CHUNK_SIZE)


def divide_file_into_chunks(file_name1):
    if not os.path.exists("chunks"):
        # Create the directory
        os.mkdir("chunks")
        print("Directory created successfully.")
    else:
        print("Directory already exists.")

    index = 1
    with open(file_name1, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunk_name = content_name + '_' + str(index)
            # print("chunk name is: " + chunk_name + "\n")
            with open(os.path.join("chunks", chunk_name), 'wb+') as chunk_file:
                chunk_file.write(chunk)
            index += 1
            chunk = infile.read(int(CHUNK_SIZE))


def get_chunk_files(directory):
    # Get the names of files under the specified directory
    file_names = []
    for file_name0 in os.listdir(directory):
        if file_name0.startswith(f"{content_name}_"):
            file_names.append(file_name0)

    return file_names


def announce_chunks():
    # Divide the specified file into chunks
    chunk_directory = "chunks"
    divide_file_into_chunks(file_name)

    print(f"Number of chunks: 5")
    print("Starting to announce chunks...")

    while True:
        # Get the chunk file names in the 'chunks' directory
        chunk_files = get_chunk_files(chunk_directory)

        # Prepare the message in JSON array format
        message = json.dumps({"chunks": chunk_files})

        # Send the broadcast UDP message
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sock.sendto(message.encode(), (BROADCAST_IP, 5001))
        sock.close()

        time.sleep(20)


announce_chunks()
