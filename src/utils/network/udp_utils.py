import socket
from typing import Tuple


class UDPListener:
    def __init__(self, host: str, port: int, buffer_size: int = 1024) -> None:
        """
        Initialize a UDP listener.

        :param host: The host IP address to listen on.
        :param port: The port number to listen on.
        :param buffer_size: The size of the buffer for receiving data.
        """
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def listen(self) -> Tuple[str, Tuple[str, int]]:
        """
        Listen for incoming UDP packets.

        :return: A tuple containing the received message and the address of the sender.
        """
        print(f"Listening for UDP packets on {self.host}:{self.port}")
        data, addr = self.sock.recvfrom(self.buffer_size)
        message = data.decode("utf-8")
        print(f"Received message from {addr}: {message}")
        return message, addr

    def close(self) -> None:
        """
        Close the UDP socket.
        """
        self.sock.close()


class UDPSender:
    def __init__(self, target_host: str, target_port: int) -> None:
        """
        Initialize a UDP sender.

        :param target_host: The target host IP address to send data to.
        :param target_port: The target port number to send data to.
        """
        self.target_host = target_host
        self.target_port = target_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message: str) -> None:
        """
        Send a UDP message to the target host and port.

        :param message: The message to send.
        """
        print(f"Sending message to {self.target_host}:{self.target_port}: {message}")
        self.sock.sendto(message.encode("utf-8"), (self.target_host, self.target_port))

    def close(self) -> None:
        """
        Close the UDP socket.
        """
        self.sock.close()


# Example usage
# if __name__ == "__main__":
#     # Example of running a UDP listener
#     listener = UDPListener(host="127.0.0.1", port=5005)
#     try:
#         message, addr = listener.listen()
#     finally:
#         listener.close()
#
#     # Example of running a UDP sender
#     sender = UDPSender(target_host="127.0.0.1", target_port=5005)
#     try:
#         sender.send("Hello, UDP!")
#     finally:
#         sender.close()
