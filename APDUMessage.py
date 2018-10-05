class APDUMessage:

    def __init__(self, header, body):
        self.header = header
        self.body = body

    def convertToByteArray(self):
        return self.header + [len(self.body)] + self.body + [0x00]