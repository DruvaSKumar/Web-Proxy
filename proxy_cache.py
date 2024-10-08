import socket
import sys
import _thread
import traceback

cache = {}

def main():
    global listen_port, buffer_size, max_conn
    try:
        listen_port = int(input("Enter a listening port: "))
    except KeyboardInterrupt:
        sys.exit(0)

    max_conn = 10000
    buffer_size = 10000
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", listen_port))
        s.listen(max_conn)
        print("[*] Initializing socket. Done.")
        print("[*] Socket binded successfully...")
        print(f"[*] Server started successfully [{listen_port}]\n")
    except Exception as e:
        print(e)
        sys.exit(2)

    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            _thread.start_new_thread(conn_string, (conn, data, addr))
        except KeyboardInterrupt:
            s.close()
            print("\n[*] Shutting down...\n")
            sys.exit(1)
    s.close()

def conn_string(conn, data, addr):
    try:
        print(addr)
        first_line = data.decode('latin-1').split("\n")[0]
        print(first_line)
        url = first_line.split(" ")[1]

        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]

        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int(temp[(port_pos + 1):][:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        print(webserver)
        proxy_server(webserver, port, conn, data, addr)
    except Exception as e:
        print(e)
        traceback.print_exc()

def proxy_server(webserver, port, conn, data, addr):
    print(f"{webserver} {port} {conn} {addr}\n")
    try:
        if webserver in cache:
            cached_response = cache[webserver]
            print(f"[*] Serving from cache: {webserver}\n")
            conn.sendall(cached_response)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webserver, port))
            s.send(data)

            server_response = b""
            while 1:
                reply = s.recv(buffer_size)

                if len(reply) > 0:
                    conn.sendall(reply)
                    server_response += reply
                    print(f"[*] Request sent: {addr[0]} > {webserver}\n")
                else:
                    break

            s.close()
            conn.close()

            cache[webserver] = server_response

    except Exception as e:
        print(e)
        traceback.print_exc()
        if 's' in locals() and s:
            s.close()
        conn.close()
        sys.exit(1)

if __name__ == "__main__":
    main()

