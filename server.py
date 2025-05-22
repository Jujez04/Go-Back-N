import socket as sk
import time

LIMIT_PACK = 30

# Creazione del socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# Associamo il socket alla porta 12000
server_address = ('localhost', 12000)
print ('\n\r Associazione %s porta %s' % server_address)
sock.bind(server_address)

expected_seq_num = 0

try:
    while expected_seq_num < LIMIT_PACK:
        print('\n\r waiting to receive message...')
        data, address = sock.recvfrom(4096)
        print('received %s bytes from %s' % (len(data), address))
        msg = data.decode('utf8')
        seq_num = int(msg.split()[1])
        if seq_num == expected_seq_num:
            time.sleep(2)
            message = f'ACK {expected_seq_num}'
            sent = sock.sendto(message.encode(), address)
            print ('sent %s bytes back to %s' % (sent, address))
            expected_seq_num += 1
        else:
            ack_to_resend = expected_seq_num - 1 if expected_seq_num > 0 else 0
            message = f'ACK {ack_to_resend}'
            sent = sock.sendto(message.encode(), address)
            print("\nACK failed\n")
            print ('sent %s bytes back to %s' % (sent, address))
finally:
    print('closing socket')
    sock.close()
