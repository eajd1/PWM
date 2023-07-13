# Created: 17/01/2023
# Last Updated: 19/01/2023
# By Ethan Denis

import hashlib, binascii, time

def round_up(num : float) -> int:
    integerPart = int(num)
    remaining = num - integerPart
    if (remaining > 0):
        return integerPart + 1
    else:
        return integerPart

def even_hex(num : int) -> str:
    str = hex(num)
    if (len(str) % 2 != 0):
        str = "0x0" + str[2:]
    return str


class SMsg:

    cypherText = ''

    def __init__(self, blockSize : int):
        self.blockSize = blockSize
        if (self.blockSize > 64):
            self.blockSize = 64

    def make_hash(self, msg : str, salt : str):
        hash = hashlib.pbkdf2_hmac('sha512', str.encode(msg), str.encode(salt), 10000)
        hash = int(binascii.hexlify(hash), 16)
        return hash

    def make_blocks(self, msg : str):
        blocks = []
        for i in range(0, round_up(len(msg) / self.blockSize)):
            blocks.append(self.hexify(msg[i*self.blockSize:(i+1)*self.blockSize]))
        return blocks

    def add_padding(self, plainTextBlocks):
        length = len(plainTextBlocks[len(plainTextBlocks) - 1])
        length = length - 2 # don't include 0x
        length = int(length / 2) # how many bytes (2 hex digits)
        if (length != self.blockSize):
            difference = self.blockSize - length
            for i in range(0, difference):
                plainTextBlocks[len(plainTextBlocks) - 1] += even_hex(difference)[2:]
        return plainTextBlocks

    def hexify(self, msg : str):
        # Converts the msg into a hex number
        hexNums = ''
        for i in range(0, len(msg)):
            num = ord(msg[i])
            hexNums += even_hex(num)[2:] # remove 0x
        return '0x' + hexNums
    
    def encrypt_block(self, block : str, lastBlock : str, password : str):
        newmsg = hex(int(block, 16) ^ self.make_hash(password, lastBlock))
        return newmsg

    def encrypt(self, msg : str, password : str):
        if (not msg):
            return
        
        print("Encrypting...")
        startTime = time.time()
        # blocks of hex unpadded
        plainTextBlocks = self.make_blocks(msg)
        
        # Add Padding
        plainTextBlocks = self.add_padding(plainTextBlocks)

        # Encrypting
        chainValue = "0x00"
        cypherTextBlocks = []
        for i in range(0, len(plainTextBlocks)):
            cypherTextBlocks.append(self.encrypt_block(plainTextBlocks[i], chainValue, password))
            chainValue = cypherTextBlocks[i]
            print(f" {i} out of {len(plainTextBlocks)}", end = '\r')
        self.cypherText = cypherTextBlocks

        endTime = time.time()
        print("Encrypted in " + str(endTime - startTime) + 's')

    def dehexify(self, msg : str):
        # Converts hex number back to text
        msg = msg[2:] # remove 0x
        text = ''
        for i in range(0, len(msg), 2):
            num = int("0x" + msg[i:i+2], 16) # convert each byte to int
            text += chr(num)
        return text

    def decrypt_block(self, block : str, lastBlock : str, password : str):
        newmsg = hex(int(block, 16) ^ self.make_hash(password, lastBlock))
        return newmsg

    def remove_padding(self, plainTextBlocks):
        index = len(plainTextBlocks) - 1
        lastCharacter = plainTextBlocks[index][-2:] # last 2 characters
        num = int(("0x" + lastCharacter), 16) * 2 # convert to int num of characters
        paddingPos = len(plainTextBlocks[index]) - num
        if (num / 2 < self.blockSize):
            byte = plainTextBlocks[index][paddingPos : paddingPos + 2]
            firstPad = int(("0x" + byte), 16)
            if (num == firstPad * 2):
                plainTextBlocks[index] = plainTextBlocks[index][:paddingPos]
        return plainTextBlocks

    def decrypt(self, password : str):
        print("Decrypting...")
        startTime = time.time()
        chainValue = "0x00"
        plainTextBlocks = []
        for i in range(0, len(self.cypherText)):
            plainTextBlocks.append(self.decrypt_block(self.cypherText[i], chainValue, password))
            chainValue = self.cypherText[i]
            print(f" {i} out of {len(self.cypherText)}", end = '\r')

        # Remove Padding
        plainTextBlocks = self.remove_padding(plainTextBlocks)

        # Convert to text
        for i in range(0, len(plainTextBlocks)):
            plainTextBlocks[i] = self.dehexify(plainTextBlocks[i])
        
        endTime = time.time()
        print("Decrypted in " + str(endTime - startTime) + 's')
        return ''.join(plainTextBlocks)

    def get_formatted_cypher_text(self):
        # To convert the array to a string concatonate the elements and replace "0x" with a new line
        text = ''
        for i in range(0, len(self.cypherText)):
            text += self.cypherText[i]
        text = text.replace("0x", "\n")
        return text[1:] # remove new line at start

    def load_text(self, cypherText : str):
        # reads in a string in to form created by GetFormattedCypherText() and converts to the array form
        array = cypherText.splitlines()
        for i in range(0, len(array)):
            array[i] = "0x" + array[i]
        self.cypherText = array

# pwm = None
# msg = input("msg: ")
# while (msg):
#     password = input("password: ")
#     chunkSize = input("Block Size: ")
#     pwm = SMsg(int(chunkSize))
#     pwm.Encrypt(msg, password)

#     if (input("Decrypt?: ")):
#         password = input("password: ")
#         pwm.Decrypt(password)
    
#     msg = input("msg: ")