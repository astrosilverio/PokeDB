import signal
import socket

from pokedb import access, locks, logs, storage, transactions


def start_socket():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.close()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('localhost', 1188))
    s.listen(2)
    return s


def start_pokedb():
    storage.start()
    locks.start()
    transactions.start()
    access.start()
    return start_socket()


def terminate_pokedb(socket):
    storage.stop()
    socket.close()


def process_request(data):
    if data.startswith('wyd'):
        return transactions._transaction_manager.transaction_statuses
    elif data.startswith('BEGIN TRANSACTION'):
        return transactions.begin_transaction()
    elif data.startswith('COMMIT'):
        txn_id = int(data.split()[1])
        return transactions.commit(txn_id)
    elif data.startswith('ROLLBACK'):
        txn_id = int(data.split()[1])
        return transactions.rollback(txn_id)
    elif data.startswith('TRANSACTION'):
        words = data.split()
        txn_id = int(words[1])
        if not txn_id in transactions._transaction_manager.transactions:
            return "txn %s does not exist yet" % txn_id
        operation = words[2]
        row_id = int(words[3])

        if operation == 'READ':
            return access.read(txn_id, row_id)
        elif operation == 'WRITE':
            value = words[4]
            return access.write(txn_id, row_id, value)


class Killer(object):
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


if __name__ == '__main__':
    killer = Killer()
    s = start_pokedb()

    while True:
        if killer.kill_now:
            terminate_pokedb()
            break

        conn, addr = s.accept()
        data = conn.recv(1024)

        try:
            response = str(process_request(data))
        except ValueError as e:
            response = e.message

        conn.sendall(response)
        conn.close()
