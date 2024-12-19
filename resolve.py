import socket

def resolve_msc(mmsc_server_ip, mmsc_server_port):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the MMSC server
    sock.connect((mmsc_server_ip, mmsc_server_port))

    # Send a probe request to the MMSC server
    probe_request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(mmsc_server_ip)
    sock.sendall(probe_request.encode())

    # Receive the response from the MMSC server
    response = sock.recv(1024).decode()

    # Parse the response to extract the MSC IP and port
    msc_ip = None
    msc_port = None
    for line in response.splitlines():
        if "X-Mmsc-Location" in line:
            msc_url = line.split(":")[1].strip()
            msc_ip, msc_port = msc_url.split(":")
            msc_port = int(msc_port)
            break

    # Close the socket
    sock.close()

    return msc_ip, msc_port

# Example usage:
mmsc_server_ip = "192.168.1.100"
mmsc_server_port = 8080
msc_ip, msc_port = resolve_msc(mmsc_server_ip, mmsc_server_port)
print("MSC IP:", msc_ip)
print("MSC Port:", msc_port
