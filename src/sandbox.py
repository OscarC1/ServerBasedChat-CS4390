import socket
import net
import byteutil
import crypto
from Codes import Code

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = net.getOwnIP()
src_address = (host, 129,)
sock.bind(src_address)

# Send UDP HELLO to server
dest_address = (host, 128)
message = byteutil.message2bytes([
    Code.CHALLENGE,
    b"101"
])
print(crypto.a3(b"101", 137))
net.sendUDP(sock, message, dest_address)
