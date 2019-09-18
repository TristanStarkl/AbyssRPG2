import socket
import select
from threading import Thread
import save
import json
import queue


class Server(Thread):
    def __init__(self, q1, q2):
        Thread.__init__(self)
        self.isServer = False
        self.queue_from_chat = q2
        self.queue_to_chat = q1

    def create_server(self, port, max_joueur):
        try:
            self.connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.port = port

            self.max_joueur = max_joueur
            self.isServer = True
            self.connexion_principale.bind(('', self.port))
            self.connexion_principale.listen(self.max_joueur)
            self.client_name = []
        except Exception as E:
            return ("Erreur: Port déja pris")
        return ("None")

    def stop_server(self):
            print("Fermeture des connexions")
            print("Fermeture des connexions")
            for client in self.clients_connectes:
                    client.close()

            self.connexion_principale.close()

    def traitement_message(self, msg):
        try:
            if (msg.startswith("//")):
                msg = msg[2:]
                print(msg)
                self.client_name.append(msg)
                self.send_msg(msg)
            elif (msg.startswith("..")):
                tab = msg.split('|')
                client_name = tab[0]
                client_name = client_name[2:]
                typeOf = tab[1]
                preset_name = tab[2]
                file = tab[3]
                file = file.rstrip('\\')
                data = json.loads(file, object_hook=save.dict_to_obj)
                data.name = client_name + ' - ' + data.name
                try:
                   save.saveToFile(data, "personnage", multiplayer=True)
                except Exception as E:
                    print(E)
                    print("Erreur dans Save")
            else:
                self.send_msg(msg)
            print(msg)
        except Exception as E:
            print('---------------------------------------------------------------')
            print(E)
            print("ERREUR ICI PTIT FILS DE PUTE")
            print("Message mal formaté")
            print('---------------------------------------------------------------')

    def send_msg(self, msg):
        for client in self.clients_connectes:
            client.send(msg.encode())

    def run(self):
        print("Le serveur écoute à présent sur le port {}".format(self.port))

        self.serveur_lance = True
        self.clients_connectes = []

        while self.serveur_lance:
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexion_principale en lecture
    # On attend maximum 50ms
            self.connexions_demandees, wlist, xlist = select.select([self.connexion_principale],
             [], [], 0.05)
    
            for connexion in self.connexions_demandees:
                connexion_avec_client, infos_connexion = connexion.accept()
            # On ajoute le socket connecté à la liste des clients
                self.clients_connectes.append(connexion_avec_client)
        
            clients_a_lire = []
            try:
                clients_a_lire, wlist, xlist = select.select(self.clients_connectes,
                        [], [], 0.05)
            except select.error:
                pass
            else:
                try:
                    # On parcourt la liste des clients à lire
                    for client in clients_a_lire:
                        # Client est de type socket
                        msg_recu = client.recv(65536)
                        # Peut planter si le message contient des caractères spéciaux
                        msg_recu = msg_recu.decode()
                        self.traitement_message(msg_recu)
                except:
                    pass
            for client in self.clients_connectes:
                try:
                    client.send(b"ping")
                except ConnectionResetError as E:
                    index = self.clients_connectes.index(client)
                    name_deco = self.client_name.pop(index) 
                    self.clients_connectes.remove(client)
                    print("{} déconnecté".format(name_deco))



if __name__ == "__main__":

    server = Server(queue.Queue(), queue.Queue())
    #port = int(input("Port> "))
    port = 1234
    server.create_server(port, 10)
    server.start()
    server.join()