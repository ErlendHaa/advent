from collections import deque

from intcode import computer

def parse(path):
    with open(path, mode='r') as f:
        return [int(x) for x in f.readline().split(',')]

def sendpackage(com, computers, nat):
    if len(com.out) == 0: return computers, nat

    for i in range(0, len(com.out),3):
        address = com.out[i]
        x, y    = com.out[i + 1], com.out[i + 2]

        if address == 255:
            nat.append([x, y])
        else:
            computers[address].update([x,y])

    # Clear sendt packages
    com.outputs = []
    return computers, nat

def sending_status(computers):
    a = [x for x in computers if len(x.out) > 0]
    return True if len(a) > 0 else False

def receiving_status(computers):
    a = [x for x in computers if len(x.inputs) > 0]
    return True if len(a) > 0 else False

if __name__ == '__main__':
    tape = parse('inputs/day23.txt')
    computers = [computer('NIC', tape, [i]) for i in range(50)]

    nat = []
    last_restart = [None, None]
    sending, receiving = True, True

    while True:
        _ = [com() for com in computers]

        sending = sending_status(computers)

        # Send packages between computers
        for com in computers:
            computers, nat = sendpackage(com, computers, nat)

        # Check if network is idle and restart if nessesary
        if not sending and not receiving:
            restart = nat[-1]
            if restart[1] == last_restart[1]: break

            computers[0].update(restart)
            last_restart = restart
            continue

        receiving = receiving_status(computers)

        # Update computers that have not recieved any new packages
        for com in computers:
            if len(com.inputs) > 0: continue
            com.update([-1])

    print('Part 1: {}'.format(nat[0][1]))
    print('Part 2: {}'.format(restart[1]))
