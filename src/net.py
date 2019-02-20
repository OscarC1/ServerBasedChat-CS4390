from Codes import Code
import byteutil
import traceback


def sendUDP(sock, message, dest_address):
    if isinstance(message, Code):
        message = message.value

    if not isinstance(message, bytes):
        message = bytes(message)

    print("┌ Sending UDP message to server")
    print("│ Server: {}:{}".format(*dest_address))
    print("│ ┌Message (bytes): '{}'".format(message))
    print("└ └Message (print): {}".format(byteutil.formatBytesMessage(message)))

    try:
        sock.sendto(message, dest_address)
    except Exception as e:
        if e.errno == 10051:  # Winerror 10051: unreachable network
            traceback.print_exc(limit=0)
        else:
            raise
