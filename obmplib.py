def read4bint(f, o):
    ret = f[o+3]
    ret *= 256
    ret += f[o+2]
    ret *= 256
    ret += f[o+1]
    ret *= 256
    ret += f[o]
    return ret

def read2bint(f, o):
    ret = f[o+1]
    ret *= 256
    ret += f[o]
    return ret

def loadBMP(filename):
    f = open(filename, 'b+r')
    bts = f.read()
    f.close()

    if (bts[0:2] != b'BM'):
        return "Not a supported bitmap file"

    bitmapfilesize = read4bint(bts, 0x2)

    pixelarrayoffset = read4bint(bts, 0xa)

    dibheadersize = read4bint(bts, 0xe)

    bitmapwidth = read4bint(bts, 0x12)

    bitmapheight = read4bint(bts, 0x16)

    bitsperpixel = read2bint(bts, 0x1c)

    rawdatasize = read4bint(bts, 0x22)

    rowsize = ((bitsperpixel * bitmapwidth + 31) // 32) * 4

    ret = []
    for j in range(bitmapheight):
        row = []
        for i in range(bitmapwidth):
            x = pixelarrayoffset + i * 3 + j * rowsize
            row.append((bts[x + 2], bts[x + 1], bts[x]))
        ret.append(row)
    return bitmapwidth, bitmapheight, ret[::-1]

def intTo4byte(a):
    ret = b''
    ret += bytes([a % 256])
    a //= 256
    ret += bytes([a % 256])
    a //= 256
    ret += bytes([a % 256])
    a //= 256
    ret += bytes([a % 256])
    return ret

def saveBMP(filename, w, h, pixels):
    rowsize = ((24 * w + 31) // 32) * 4
    
    bts = b'BM'
    dibheader = b'\x28' + b'\x00' * 3
    dibheader += intTo4byte(w)
    dibheader += intTo4byte(h)
    dibheader += b'\x01\x00\x18' + b'\x00' * 5
    dibheader += intTo4byte(h * rowsize)
    dibheader += intTo4byte(2835)
    dibheader += intTo4byte(2835)
    dibheader += intTo4byte(0)
    dibheader += intTo4byte(0)
    padding = rowsize - 3 * w
    pixelarray = []
    for a in range(h):
        for b in pixels[h - a - 1]:
            pixelarray.extend(b)
        pixelarray.extend( [0 for i in range(padding)])
    
    pixelarray = bytes(pixelarray)
    bmpsize = len(pixelarray) + len(dibheader) + 14
    bts += intTo4byte(bmpsize)
    bts += intTo4byte(0)
    bts += intTo4byte(54)

    f = open(filename, 'b+w')
    f.write(bts + dibheader + pixelarray)
    f.close()
