from subprocess import Popen, PIPE
from os import path


class Run:

    @staticmethod
    def start(command: str):
        with open("log", "w") as file:

            file.write("\n\n============ New Logs ==========\n")

            res = Popen(command, shell=True, stderr=file, stdout=file, start_new_session=True)
            return res
