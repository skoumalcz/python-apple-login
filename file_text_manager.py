from os import path


class FileTextManager(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def save(self, text):
        file = open(self.file_name, "w")
        file.write(text)
        file.close()

    def load(self):
        if not path.exists(self.file_name):
            return None
        file = open(self.file_name, "r")
        text = file.read()
        file.close()
        return text
