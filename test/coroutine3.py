
def getSize(length):
    b = bytearray(length.to_bytes(4, byteorder='big'))
    i = 0
    while True:
        if b[i] == 0:
            b.pop(0)
        else:
            break
    return b
    
def getChunkGenerator():
    yield getSize(len(b'hello')) + b'\r\n' + b'hello' + b'\r\n'
    yield getSize(len(b'world')) + b'\r\n' + b'world' + b'\r\n'
    return b'0\r\n'

def getChunk():
    try:
        b = next(getChunkGenerator())
        print("sending chunk:", str(b))
        return b
    except Exception as e:
        chunkFinish = True
    return b""
    
print(getChunk())
print(getChunk())
print(getChunk())
print(getChunk())