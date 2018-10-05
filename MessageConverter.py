class MessageConverter:
    @staticmethod
    def string_to_byte_array(string):
        return [int(hex(ord(c)), 16) for c in string]

    @staticmethod
    def byte_array_to_string(bytes):
        return ''.join(map(chr, bytes))

    @staticmethod
    def format_hex_array(hex_array):
        return [int('0x' + b + c, 16) for (b, c) in zip(hex_array[0::2], hex_array[1::2])]