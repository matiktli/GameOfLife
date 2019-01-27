
class Logger():
    def __init__(self, name="LOG"):
        self.name = name

    def log(self, tag, message):
        print("[{0}]: {1}".format(tag, message))