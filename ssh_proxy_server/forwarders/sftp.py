import logging
import paramiko
from enhancements.modules import Module


class SFTPHandlerBasePlugin(Module):

    def __init__(self, sftp, filename):
        super().__init__()
        self.filename = filename
        self.sftp = sftp

    @classmethod
    def get_interface(cls):
        return None

    def close(self):
        pass

    def handle_data(self, data):
        return data


class SFTPHandlerPlugin(SFTPHandlerBasePlugin):
    pass


class SFTPBaseHandle(paramiko.SFTPHandle):

    def __init__(self, plugin, filename, flags=0):
        super().__init__(flags)
        self.plugin = plugin(self, filename)
        self.writefile = None
        self.readfile = None

    def close(self):
        super().close()
        self.plugin.close()

    def read(self, offset, length):
        logging.info("R_OFFSET: " + str(offset))
        data = self.readfile.read(length)
        return self.plugin.handle_data(data, length)

    def write(self, offset, data):
        logging.info("W_OFFSET: " + str(offset))
        data = self.plugin.handle_data(data)
        self.writefile.write(data)
        return paramiko.SFTP_OK
