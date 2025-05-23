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
last_seq_printed = -1

try:
    while expected_seq_num < LIMIT_PACK:
        if last_seq_printed != expected_seq_num:
            print(f'\nIn attesa del pacchetto {expected_seq_num}...')
            last_seq_printed = expected_seq_num
        # Ricezione del pacchetto
        data, address = sock.recvfrom(4096)
        msg = data.decode('utf8')
        seq_num = int(msg.split()[1])

        if seq_num == expected_seq_num:
            print(f'Pacchetto {seq_num} ricevuto correttamente')
            print(f'Invio ACK per il pacchetto {seq_num}')
            time.sleep(2)
            message = f'ACK {expected_seq_num}'
            sent = sock.sendto(message.encode(), address)
            print(f'Inviato {message} a {address}')
            expected_seq_num += 1
        else:
            ack_to_resend = expected_seq_num - 1
            message = f'ACK {ack_to_resend}'
            sent = sock.sendto(message.encode(), address)
            print("\nACK failed\n")
            print(f'Pacchetto inatteso (seq: {seq_num}), reinviato {message} a {address}')
finally:
    print('closing socket')
    sock.close()
