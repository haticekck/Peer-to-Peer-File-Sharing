import json
import datetime
import os
import socket

HOST = ''
PORT = 5000

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the host and port
sock.bind((HOST, PORT))
# Listen for incoming connections
sock.listen()

print(f"Chunk_Uploader is listening on port {PORT}")

while True:

    # Accept a connection from a client
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr[0]}")

    # Set a timeout for the TCP connection
    conn.settimeout(60)

    try:
        # Receive the message from the client
        data = conn.recv(1024)
        if not data:
            break

        try:
            message = json.loads(data.decode())
            requested_chunk = message.get("requested_content")
            if requested_chunk:
                new_path = "chunks"
                os.chdir(new_path)

                # Send the requested chunk file to the requester
                filename = requested_chunk
                with open(filename, 'rb') as file:
                    chunk_data = file.read()
                    conn.sendall(chunk_data)
                    print(f"Sent {filename} to {addr[0]}")

                    # Log the file info in the log file
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_entry = f"Chunk: {requested_chunk}, Timestamp: {timestamp}, Destination: {addr[0]}\n"
                    new_path1 = ""
                    os.chdir("..")
                    with open("upload_log.txt", 'a') as log_file:
                        log_file.write(log_entry)
            else:
                print("Invalid JSON message format: missing 'requested_chunk' field")
        except json.JSONDecodeError:
            print("Invalid JSON message")
        except FileNotFoundError:
            print(f"Chunk file '{filename}' not found.")
        except IOError as e:
            print(f"Error opening chunk file '{filename}': {str(e)}")

    except socket.timeout:
        print("TCP connection timed out")

    finally:
        conn.close()

log_file.close()
