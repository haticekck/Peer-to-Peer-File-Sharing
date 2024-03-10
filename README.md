
# P2P File Sharing System

## Introduction
This P2P (Peer-to-Peer) File Sharing System is designed to facilitate the sharing and downloading of files among multiple peers in a decentralized manner. It consists of four main components: Chunk_Announcer, Chunk_Discovery, Chunk_Downloader, and Chunk_Uploader. Each component serves a specific role in the file-sharing process.

## Components

### Chunk_Announcer
The Chunk_Announcer is responsible for periodically announcing a peer’s availability of chunks (file segments). Chunk_Announcer divides the file into 5 equal chunks. It broadcasts the information to other peers on the network. Peers can use this information to discover available chunks.

### Chunk_Discovery
The Chunk_Discovery component allows a peer to discover the available chunks. It stores the list of files (parsed from the JSON message) and IP addresses in a dictionary called “content_dictionary.txt”. 

### Chunk_Downloader
The Chunk_Downloader is used to download chunks from other peers. It prompts the user to specify the content they want to download and initiates sequential download procedures for each chunk of the content. It looks up the content dictionary to fetch the list of IP addresses having a certain chunk and attempts to download the chunk from the first available IP address. If the download is unsuccessful, it tries other IP addresses until the chunk is successfully downloaded. Chunk_Downloader also dumps all downloaded file information in a download log called “download_log.txt” with the timestamp.

### Chunk_Uploader
The Chunk_Uploader allows a peer to upload chunks to other peers. It starts to listen to in Local Area Network for requested chunks and then sends the file to the requester. Chunk_Uploader logs the file’s information in a text file called “upload_log.txt” with the timestamp.


## Usage
1. Start the Chunk_Announcer component using `python Chunk_Announcer.py`. This will start announcing the availability of chunks to other peers on the network.

2. Start the Chunk_Discovery component using `python Chunk_Discovery.py`. This will allow you to discover the available chunks for specific content.

3. Start the Chunk_Downloader component using `python Chunk_Downloader.py`. This will prompt you to enter the content name you want to download and initiate the download process for the chunks of that content.

4. Start the Chunk_Uploader component using `python Chunk_Uploader.py`. This will allow you to upload chunks to other peers on the network.

## Known Limitations
- For the system to work properly as a file sharer, the user needs to upload a picture with the extension ".png" to where the code documents are.
- In downloader part when the user prompts the wanted filename, the name of the file should be written without any extention.
- The system assumes a local network environment and does not include features for handling NAT traversal or communication over the internet.
- Error handling is minimal in the code provided and may require additional enhancements to handle various edge cases and exceptions.


