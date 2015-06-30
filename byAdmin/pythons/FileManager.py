import os
import codecs

class FileManager:
    @staticmethod
    def read_file(filename):
        with codecs.open(filename, 'r', encoding='utf8') as f:
            return f.read()

    @staticmethod
    def save_file(filename, contents):
        with open(filename, 'wb') as f:
            f.write(contents)
            f.close()

    @staticmethod
    def write_string_to_file(filename, contents):
        with codecs.open(filename, 'w', encoding='utf8') as f:
            f.write(contents)
            f.close()

    @staticmethod
    def append_string_to_file(filename, contents):
        with codecs.open(filename, 'a', encoding='utf8') as f:
            f.write(contents)
            f.close()

    @staticmethod
    def make_dir(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def touch_file(filePath, times=None):
        if not os.path.exists(filePath):
            with open(filePath, 'a'):
                os.utime(filePath, times)

    @staticmethod
    def parent_path(p):
        return os.path.normpath(os.path.join(p, os.path.pardir))

    @staticmethod
    def remove_file(path):
        if os.path.exists(path):
            os.remove(path)
