from functools import reduce


hex2bin = {
    '0' : '0000',
    '1' : '0001',
    '2' : '0010',
    '3' : '0011',
    '4' : '0100',
    '5' : '0101',
    '6' : '0110',
    '7' : '0111',
    '8' : '1000',
    '9' : '1001',
    'A' : '1010',
    'B' : '1011',
    'C' : '1100',
    'D' : '1101',
    'E' : '1110',
    'F' : '1111',
}

def convert2bin(hexrep):
    return ''.join([hex2bin[char] for char in hexrep])

def parse(inputfile):
    hexrep = open(inputfile).read().strip('\n')
    binrep = convert2bin(hexrep)
    return MessageIO(binrep)

class MessageIO:
    def __init__(self, buffer):
        self.buffer = buffer
        self.offset = 0
        self.size   = len(buffer)

    def read(self, nbytes):
        end = self.offset + nbytes

        if end >= self.size:
            raise OverflowError('Buffer out of range')

        chunk = self.buffer[self.offset:end]
        self.offset = end
        return chunk

class Packet:
    def __init__(self, typeid, version, literal = None, packets = []):
        self.typeid  = typeid
        self.version = version
        self.literal = literal
        self.packets = packets

    def isliteral(self):
        return self.typeid == 4

    def evaluate(self):
        if self.isliteral(): return self.literal

        values = [packet.evaluate() for packet in self.packets]
        typeid = self.typeid
        if   typeid == 0: return reduce(lambda x, y: x + y, values)
        elif typeid == 1: return reduce(lambda x, y: x * y, values)
        elif typeid == 2: return reduce(lambda x, y: x if x <  y else y, values)
        elif typeid == 3: return reduce(lambda x, y: x if x >  y else y, values)
        elif typeid == 5: return reduce(lambda x, y: 1 if x >  y else 0, values)
        elif typeid == 6: return reduce(lambda x, y: 1 if x <  y else 0, values)
        elif typeid == 7: return reduce(lambda x, y: 1 if x == y else 0, values)
        else:
            raise ValueError(f'invalid typeid: {typeid}')

def todecimal(binary):
    return int(binary, 2)

def parse_packet_header(message):
    """Parse packet header """
    version = message.read(3)
    typeid  = message.read(3)
    return todecimal(version), todecimal(typeid)

def parse_packet_length(message):
    """Parse packet length for operator packets """
    chunk = message.read(1)
    ltype = todecimal(chunk)
    nbits = 15 if ltype == 0 else 11
    chunk = message.read(nbits)
    return ltype, todecimal(chunk)

def parse_literal(message):
    """Parse literal from literal packet """
    chunks = []
    while True:
        continuation = message.read(1)
        chunks.append(message.read(4))
        if continuation == '0': break

    return todecimal(''.join(chunks))

def parse_message(message):
    version, typeid = parse_packet_header(message)

    if typeid == 4:
        return Packet(typeid, version, literal = parse_literal(message))

    ltype, val = parse_packet_length(message)

    packets = []
    offset  = message.offset
    npacket = 0
    while True:
        if ltype == 0 and message.offset >= offset + val: break
        if ltype == 1 and npacket        >= val:          break

        subpackets = parse_message(message)
        packets.append(subpackets)
        npacket += 1

    return Packet(typeid, version, packets = packets)

def versions(packet):
    vs = [packet.version]
    for pack in packet.packets:
        vs.extend( versions(pack) )
    return vs

def day16_part1(inputfile):
    message = parse(inputfile)
    packet = parse_message(message)
    return sum(versions(packet))

def day16_part2(inputfile):
    message = parse(inputfile)
    packet = parse_message(message)
    return packet.evaluate()
