from subprocess import Popen, PIPE


class Run:

    @staticmethod
    def start(command: str):
        res = Popen(command,shell=True)
        return res
