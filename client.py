import socket as sk # Per la creazione del socket UDP
import time # Per creare il timer
import threading # Per creare il thread che gestisce il timer
import random

SERVER_ADDRESS = ('localhost', 12000)
WINDOW_SIZE = 3
LOSS_PROBABILITY = 0.7 # Probabilità di perdita del pacchetto

# Creazione del socket UDP
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# Definisco il timer del sender, così come le sue funzioni per lavorare sulla ritrasmissione dei pacchetti
TIMEOUT = 2

class Timer:
    def __init__(self, timeout_interval):
        self.timeout_interval = timeout_interval
        self.start_time = None

    def start_timer(self):
        self.start_time = time.perf_counter() # Utilizziamo perf_counter per ottenere un tempo più preciso

    def has_reached_timeout(self):
        if self.start_time is None:
            return False
        if time.perf_counter() - self.start_time >= self.timeout_interval:
            self.start_time = None
            return True
        return False

    def stop_timer(self):
        self.start_time = None

stats = {
    'inviati': 0,
    'persi': 0,
    'ritrasmessi': 0,
    'ack_ricevuti': 0
}

# Definisco i metodi per inviare pacchetti, ricevere ACK e gestire il timeout
def send_pack(pack_num):
    global timer
    message = f'Pacchetto {pack_num}'
    # Simulazione perdita del pacchetto
    if random.random() < LOSS_PROBABILITY:
        stats['persi'] += 1
        print(f"[SIMULAZIONE PERDITA] Pacchetto {pack_num} perso")
    else:
        stats['inviati'] += 1
        print(f"Invio {message}")
        sock.sendto(message.encode(), SERVER_ADDRESS)
    if pack_num == base:
        timer.start_timer()


def receive_ack():
    global timer, base
    while base < PACK_TO_SEND:
        time.sleep(1)
        try:
            data, server = sock.recvfrom(4096)
            msg = data.decode('utf8')
            ack_message, ack_num = msg.split()
            ack_num = int(ack_num)
            if ack_message == 'ACK':
                stats['ack_ricevuti'] += 1
                print(f"Ricevuto {ack_num}")
                with lock:
                    if ack_num >= base:
                        base = ack_num + 1
                        if base == next_id_pack:
                            timer.stop_timer()
                        else:
                            timer.start_timer()
        except Exception as e:
            print("Errore nella ricezione ACK:", e)

def handle_timeout():
    global base, next_id_pack, timer
    while base < PACK_TO_SEND:
        time.sleep(0.1)
        with lock:
            if timer.has_reached_timeout():
                print("Timeout raggiunto! Ritrasmetto da", base, "a", next_id_pack - 1)
                for i in range(base, next_id_pack):
                    stats['ritrasmessi'] += 1
                    send_pack(i)
                timer.start_timer()


# Definisco i pacchetti da spedire al receiver
PACK_TO_SEND = 30
base = 0
next_id_pack = 0
timer = Timer(TIMEOUT)
lock = threading.Lock()

# Avvia i thread
threading.Thread(target=receive_ack, daemon=True).start()
threading.Thread(target=handle_timeout, daemon=True).start()
try:
    while base < PACK_TO_SEND:
        with lock:
            if next_id_pack < base + WINDOW_SIZE and next_id_pack < PACK_TO_SEND:
                send_pack(next_id_pack)
                next_id_pack += 1
        time.sleep(0.5)
finally:
    time.sleep(1)
    print('Chiusura del socket')
    sock.close()
    print("\nStatistiche finali:")
    for k, v in stats.items():
        print(f"{k}: {v}")