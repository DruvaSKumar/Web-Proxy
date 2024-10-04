# Simple Proxy Server with Caching

## Description

This project implements a simple proxy server in Python that can handle HTTP requests. It includes a basic caching mechanism to improve performance for repeated requests. The server listens for incoming connections, forwards requests to the destination web server, and caches responses for a configurable period of time.

## Features

- Multi-threaded handling of client connections
- Basic HTTP request parsing and forwarding
- In-memory caching of responses with configurable expiry time
- Support for both HTTP and HTTPS connections
- Simple command-line interface for starting the server

## Requirements

- Python 3.x

## Usage

1. Clone the repository or download the script.

2. Run the script:
   ```
   python proxy_server.py
   ```

3. When prompted, enter the port number on which you want the proxy server to listen.

4. The server will start and display a message indicating it's running.

5. Configure your browser or application to use this proxy server (use localhost or 127.0.0.1 as the proxy address, and the port number you specified).

## Configuration

You can modify the following variables in the script to adjust the server's behavior:

- `max_conn`: Maximum number of simultaneous connections (default: 10000)
- `buffer_size`: Size of the buffer for receiving data (default: 10000 bytes)
- `cache_expiry_time`: Time in seconds for which cached responses remain valid (default: 60 seconds)

## How It Works

1. The server listens for incoming connections on the specified port.
2. When a connection is received, it parses the HTTP request to extract the destination server and port.
3. It checks if a cached response is available for the request.
4. If a valid cached response exists, it sends the cached response back to the client.
5. If no cache is available, it forwards the request to the destination server, caches the response, and sends it back to the client.
6. The server uses threading to handle multiple connections simultaneously.

## Limitations

- This is a basic implementation and may not handle all edge cases or complex HTTP scenarios.
- The caching mechanism is simple and does not account for cache control headers from the origin server.
- There's no support for HTTPS connections to destination servers (only HTTP is supported).

## Security Considerations

- This proxy does not implement any authentication or access control.
- It does not encrypt traffic between the client and the proxy.
- Use in production environments is not recommended without further security enhancements.

