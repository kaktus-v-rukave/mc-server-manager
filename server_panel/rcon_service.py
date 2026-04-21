from mcrcon import MCRcon
from dotenv import load_dotenv

load_dotenv()


class RconService:
    def __init__(self, host, password):
        self.host = host
        self.password = password

    def send_command(self, command):
        with MCRcon(self.host, self.password) as mcr:
            mcr.command(command)

    def stop_server(self):
        self.send_command("stop")