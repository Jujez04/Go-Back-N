import socket as sk
import time
import logging

LIMIT_PACK = 30

logging.basicConfig(
    filename='server.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Creazione del socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# Associamo il socket alla porta 12000
server_address = ('localhost', 12000)
logging.info('Associazione %s porta %s' % server_address)
sock.bind(server_address)

expected_seq_num = 0
last_seq_printed = -1

try:
    while expected_seq_num < LIMIT_PACK:
        if last_seq_printed != expected_seq_num:
            logging.info(f'In attesa del pacchetto {expected_seq_num}...')
            last_seq_printed = expected_seq_num
        # Ricezione del pacchetto
        data, address = sock.recvfrom(4096)
        msg = data.decode('utf8')
        seq_num = int(msg.split()[1])

        if seq_num == expected_seq_num:
            logging.info(f'Pacchetto {seq_num} ricevuto correttamente')
            logging.info(f'Invio ACK per il pacchetto {seq_num}')
            time.sleep(2)
            message = f'ACK {expected_seq_num}'
            sent = sock.sendto(message.encode(), address)
            logging.info(f'Inviato {message} a {address}')
            expected_seq_num += 1
        else:
            ack_to_resend = expected_seq_num - 1
            message = f'ACK {ack_to_resend}'
            sent = sock.sendto(message.encode(), address)
            logging.warning(f'Pacchetto inatteso (seq: {seq_num}), reinviato {message} a {address}')
finally:
    logging.info('Chiusura del socket')
    sock.close()
