import logging
from typing import Optional

import paramiko

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class SSHClient:
    def __init__(
        self,
        hostname: str,
        username: str,
        password: Optional[str] = None,
        key_filepath: Optional[str] = None,
    ) -> None:
        """
        Initialize SSHClient with hostname, username, and authentication method.

        :param hostname: SSH server hostname
        :param username: SSH username
        :param password: Password for SSH authentication
        :param key_filepath: Filepath to the private key for SSH key-based authentication
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filepath = key_filepath
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self) -> None:
        """
        Establish an SSH connection to the remote host.

        :raises Exception: If connection fails
        """
        try:
            if self.key_filepath:
                logger.info(f"Connecting to {self.hostname} using key authentication.")
                private_key = paramiko.RSAKey.from_private_key_file(self.key_filepath)
                self.client.connect(
                    hostname=self.hostname,
                    username=self.username,
                    pkey=private_key,
                )
            elif self.password:
                logger.info(
                    f"Connecting to {self.hostname} using password authentication."
                )
                self.client.connect(
                    hostname=self.hostname,
                    username=self.username,
                    password=self.password,
                )
            else:
                raise ValueError(
                    "Password or key_filepath must be provided for authentication."
                )

            logger.info(f"Successfully connected to {self.hostname}.")
        except Exception as e:
            logger.error(f"Failed to connect to {self.hostname}: {e}")
            raise

    def execute_command(self, command: str) -> str:
        """
        Execute a command on the remote host.

        :param command: Command to execute on the remote host
        :return: Standard output from command execution
        :raises Exception: If command execution fails
        """
        try:
            if not self.client.get_transport().is_active():
                raise ConnectionError("SSH connection is not active.")

            logger.info(f"Executing command on {self.hostname}: {command}")
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                logger.error(f"Command execution failed: {error}")
                raise RuntimeError(f"Command execution failed with error: {error}")

            logger.info(f"Command executed successfully with output: {output}")
            return output
        except Exception as e:
            logger.error(
                f"Failed to execute command '{command}' on {self.hostname}: {e}"
            )
            raise

    def close(self) -> None:
        """
        Close the SSH connection.
        """
        if self.client:
            self.client.close()
            logger.info(f"SSH connection to {self.hostname} closed.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Example Usage:
# if __name__ == "__main__":
#     # Connect using key-based authentication
#     ssh_client = SSHClient(hostname="your-hostname", username="your-username", key_filepath="/path/to/private_key")
#
#     # Connect using password authentication
#     # ssh_client = SSHClient(hostname="your-hostname", username="your-username", password="your-password")
#
#     try:
#         ssh_client.connect()
#         output = ssh_client.execute_command("ls -l")
#         print(output)
#     finally:
#         ssh_client.close()
