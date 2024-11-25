from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, \
    QMessageBox , QGridLayout , QCheckBox , QTextEdit
import sys
import socket
import threading

class Server(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Le server de tchat")
        self.setGeometry(200, 200, 300, 400)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        grid = QGridLayout()
        self.label = QLabel("Serveur :")
        grid.addWidget(self.label, 0, 0)
        self.input_server = QLineEdit("0.0.0.0")
        grid.addWidget(self.input_server, 0, 1)
        self.input_port = QLabel("port :")
        grid.addWidget(self.input_port, 1, 0)
        self.input_port = QLineEdit("4200")
        grid.addWidget(self.input_port, 1, 1)
        self.max = QLabel("Max Clients:")
        grid.addWidget(self.max, 2, 0)
        self.max_clients_input = QLineEdit("5")
        grid.addWidget(self.max_clients_input, 2, 1)
        layout.addWidget(self.label)
        self.input_server = QLineEdit()
        layout.addWidget(self.input_server)
        self.label = QLabel("Port :")
        layout.addWidget(self.label)
        self.input_port = QLineEdit()
        layout.addWidget(self.input_port)
        self.start_button = QPushButton("Démarrer le serveur")
        self.start_button.clicked.connect(self.button)
        layout.addWidget(self.start_button)
        central_widget.setLayout(layout)
        self.client = QTextEdit()
        self.client.setReadOnly(True)
        layout.addWidget(self.client)

    def button(self):
        if self.marche:
            self.stop_server()
        else:
            self.start_server()

    # Function to handle receiving messages from a client
    def receive_from_client(conn, addr):
        while True:
            try:
                client_message = conn.recv(1024).decode()
                if not client_message:
                    break
                print(f"Client {addr}: {client_message}")
                if client_message == "bye":
                    print(f"Client {addr} déconnecté.")
                    break
                elif client_message == "arret":
                    print("Arrêt du client et du serveur.")
                    conn.send("Server shutting down...".encode())
                    conn.close()
                    server_socket.close()
                    print("Fermeture du serveur.")
                    return
            except Exception as e:
                print(f"Erreur avec le client {addr}: {e}")
                break
        conn.close()
        print(f"Connexion fermée avec le client {addr}")
            
    def demmarage(self):
        if self.marche:

            try:
                server = self.input_server.text()
                port = int(self.input_port.text())
                max_clients = int(self.max_clients_input.text())

                global server_socket
                server_socket = socket.socket()
                server_socket.bind((server, port))
                server_socket.listen(max_clients)
                print("Serveur en attente de connexions...")
                self.marche = True
                self.start_button.setText("Arrêter le serveur")
                self.client.append("Serveur démarré.")
                self.accept_thread = threading.Thread(target=self.accept_clients)
                self.accept_thread.start()
            except Exception as e:
                self.client.append(f"Erreur lors du démarrage: {e}")
        else:
            self.stop_server()

               
    def stop_server(self):
        try:
            self.is_running = False
            if self.server_socket:
                self.server_socket.close()
            self.client_display.append("Serveur arrêté.")
        except Exception as e:
            self.client_display.append(f"Erreur lors de l'arrêt: {e}")
        finally:
            self.start_button.setText("Démarrer le serveur")  

    def accept(self):
        self.is_running = True
        while self.is_running:
            self.client.append("En attente d'un client")
            conn, addr = self.server_socket.accept()
            self.client_conn = conn
            self.client_addr = addr
            self.client.append(f"Client connecté : {addr}")
            self.__reception()
        

    def receive_from_client(conn, addr):
    while True:
        try:
            client_message = conn.recv(1024).decode()
            if not client_message:
                break
            print(f"Client {addr}: {client_message}")
            if client_message == "bye":
                print(f"Client {addr} déconnecté.")
                break
            elif client_message == "arret":
                print("Arrêt du client et du serveur.")
                conn.send("Server shutting down...".encode())
                conn.close()
                server_socket.close()
                print("Fermeture du serveur.")
                return
        except Exception as e:
            print(f"Erreur avec le client {addr}: {e}")
            break
    conn.close()
    print(f"Connexion fermée avec le client {addr}")
        
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = Server()
        window.show()
        sys.exit(app.exec())
