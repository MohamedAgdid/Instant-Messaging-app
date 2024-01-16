import socket
import threading
import sqlite3
import time
import json


# Create a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Adresse IP du serveur et numéro de port

IP = '127.0.0.1'  #localhost

PORT = 8489

#setblocking : en cas de problème lors de l'envoi ou de la réception de messages, le serveur ne doit pas bloquer
server.setblocking(1)
# Lier le socket à l'adresse IP et au numéro de port
server.bind((IP, PORT))

# Commencer à écouter les connexions entrantes.
server.listen()

# Créer des table pour les données utilisateur, les messages dans le salon, en privé et en des groupes.
def create_table():
    conn = sqlite3.connect('DATABASE.db')
    c = conn.cursor()
   
    
    c.execute('''CREATE TABLE IF NOT EXISTS message 
                      (message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(20),
                        message TEXT,
                        temps TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS user
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(20) NOT NULL,
                        password VARCHAR(20) NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS private 
                      (message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(20),
                        message TEXT,
                        temps TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS groupe 
                      (message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(20),
                        message TEXT,
                        temps TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()
    
    
# Fonction d'insertion dans l'historique du salon
def insertmsg(username, message):
    conn = sqlite3.connect('DATABASE.db')
    c = conn.cursor()
    c.execute("INSERT INTO message (username, message) VALUES (?, ?)", (username, message))
    conn.commit()
    conn.close()
    
# Fonction d'insertion dans l'historique du prive
def insertmsg_prv(username, message):
    conn = sqlite3.connect('DATABASE.db')
    c = conn.cursor()
    c.execute("INSERT INTO private (username, message) VALUES (?, ?)", (username, message))
    conn.commit()
    conn.close()

# Fonction d'insertion dans l'historique du groupe.
def insertmsg_grp(username, message):
    conn = sqlite3.connect('DATABASE.db')
    c = conn.cursor()
    c.execute("INSERT INTO groupe (username, message) VALUES (?, ?)", (username, message))
    conn.commit()
    conn.close()
    
#Fonction d'insertion dans table user
def insertuser(username, password):
    conn = sqlite3.connect('DATABASE.db')
    c = conn.cursor()
    c.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

#Fonction de selection dans l'historique du salon.
def selectmsg(client, username):
    conn = sqlite3.connect('DATABASE.db')
    c = conn.cursor()
    c.execute('SELECT username, message, temps FROM message WHERE username= ? ORDER BY temps DESC', (username,))
    rows = c.fetchall()
    client.send(f'Votre Historique : '.encode("utf-8"))
    for row in rows:

        client.send(f'> {row[1]} : {row[2]}\n'.encode("utf-8"))
    conn.close()

#Fonction de selection dans l'historique du prive.
def selectmsg_prv(client, username):
    conn = sqlite3.connect('DATABASE.db')
    c = conn.cursor()
    c.execute('SELECT username, message, temps FROM private WHERE username= ? ORDER BY temps DESC', (username,))
    rows = c.fetchall()
    client.send(f'Votre Historique Privé : '.encode("utf-8"))
    for row in rows:
        client.send(f'>> {row[1]} : {row[2]}\n'.encode("utf-8"))
    conn.close()

#Fonction de selection dans l'historique du groupe.
def selectmsg_grp(client, username):
    conn = sqlite3.connect('DATABASE.db')
    c = conn.cursor()
    c.execute('SELECT username, message, temps FROM groupe WHERE username= ? ORDER BY temps DESC', (username,))
    rows = c.fetchall()
    block_history = '\n'.join([f':>> {row[1]} : {row[2]}' for row in rows])
    client.send(f'Votre Historique Groupe : \n {block_history}'.encode("utf-8"))
    conn.close()

#Fonction de selection de password in table user.
def selectuser(username):
    conn = sqlite3.connect('DATABASE.db')
    c = conn.cursor()
    c.execute('SELECT password FROM user WHERE username= ?', (username,))
    rows = c.fetchall()
    passw = None #set none if no username 
    if rows:
        passw = rows[0][0]
    conn.close()
    return passw

#Fonction de selection de username in table user.
def selectusername(username):
    conn = sqlite3.connect('DATABASE.db')
    c = conn.cursor()
    c.execute('SELECT username FROM user WHERE username= ?', (username,))
    rows = c.fetchall()
    user = None
    if rows:
        user = rows[0][0]
    conn.close()
    return user

#Fonction de mise à jour de username
def Update_username(new_username,username):
                conn = sqlite3.connect('DATABASE.db')
                c = conn.cursor()
        
                
                c.execute('''UPDATE message
                                SET username = ?
                                WHERE username = ?;''', (new_username, username))
                
                c.execute('''UPDATE user
                                SET username = ?
                                WHERE username = ?;''', (new_username, username))
                
                c.execute('''UPDATE groupe
                                SET username = ?
                                WHERE username = ?;''', (new_username, username))
                
                c.execute('''UPDATE private
                                SET username = ?
                                WHERE username = ?;''', (new_username, username))
                conn.commit()
                conn.close()
                

# Liste des utilisateurs.
usernames = []
#Liste des clients.
clients = []
#Dictionnaire pour le groupe et admin de groupe.
groupes = {}
Admin = {}

# Fonction de contrôle des clients, suppression en cas de déconnexion, et diffusion de tous les messages
def diffusion_msg(client, username):
    exitOk = False
    while exitOk==False : #Vous ne pressez pas 'Exit'
        try:
            message = (client.recv(1024)).decode("utf-8")
            
            if not message:
                #Client déconnecté
                raise ConnectionError("Client disconnected")
            
            elif message == "online client":
                
                client.send(f"ONLINE= {usernames}".encode("utf-8"))
        
            elif message == 'H_PRIVATE':
                selectmsg_prv(client, username) 
                 
            elif message == "H_SALON":
                selectmsg(client, username)
                
            elif message == "H_GROUPE":
                selectmsg_grp(client,username)
            
            elif message == "NEWUSERNAME":
                new_username = client.recv(1024).decode("utf-8")
                Update_username(new_username,username)
                for i in clients:
                    if i != client:
                        i.send(f"{username} a changé son nom d'utilisateur en {new_username}".encode("utf-8"))
                client.send(f"Tu changes ton nom d'utilisateur en {new_username}".encode("utf-8"))
                
                 # Changer le nom d'utilisateur dans la liste
                username = new_username
                pos = clients.index(client)  
                usernames[pos] = username  # Changer son nom dans la liste

                Diffusion(f"ONLINE= {usernames}".encode("utf-8"))  #Liste pour la mise à jour du nom d'utilisateur.
                
                   
            elif message.startswith('/private'):
                
                message_parts = message.split(" ")
                # Extraire le destinataire et le message des parties séparées
                destinateur = message_parts[1]
                messag = " ".join(message_parts[3:])
                
                dest_socket = None 
                for client_socket, client_username in zip(clients, usernames):
                    if client_username == destinateur:
                        dest_socket = client_socket
                        break
                
                if dest_socket:
                    dest_socket.send(f"/private {username} : {messag}".encode('utf-8'))
                    
                    insertmsg_prv(username,f'To {destinateur} : {messag}')
                    insertmsg_prv(destinateur,f'From {username} : {messag}') 
                else:
                    client.send("User not online or doesn't exist".encode('utf-8'))
                    
            elif message == "/exit":
                exitOk = True
                gestion_deconnexion(client, username)
                
            elif message.startswith("/create_groupe"):
              mesg = message.split(" ")
              groupe_name=mesg[1]
              if groupe_name not in groupes:
                groupes[groupe_name]= [username] #Ajouter le groupe à GROUPES.
                time.sleep(0.1) 
                #Ajouter l'administrateur.
                Admin[groupe_name] = username
                clients[usernames.index(username)].send(":> Le groupe a été créé, vous êtes l'administrateur.".encode("utf-8"))
                Diffusion(f"GROUPES= {groupes}".encode("utf-8"))
              else:
                 client.send(":> Le nom de groupe existe déjà.".encode("utf-8"))
                
            
            elif message.startswith("/grp_mbr"): #Ajouter des membres au groupe.
             try : 
                mesgr = message.split("+")
                groupe_nam=mesgr[1]
                membre_char=mesgr[2]
                # Convertir la chaîne JSON en une liste Python.
                membre = json.loads(membre_char) 
                if groupe_nam in groupes:
                    
                    for i in membre:
                        if i not in groupes[groupe_nam] and i in usernames:
                           groupes[groupe_nam].append(i)
                            
                    for i in membre :
                       if i in usernames :
                         clients[usernames.index(i)].send(f":> Tu es membre de groupe {groupe_nam}".encode("utf-8"))
                    
                else:
                    client.send(f":> Créez d'abord un groupe, puis ajoutez-y vos amis.")
                    
                
                #Envoi de la liste des groupes créés.
                Diffusion(f"GROUPES= {groupes}".encode("utf-8"))
                
             except Exception as e:
                   print(f"Exception dans /grp_mbr: {e}")        
                   
            elif message.startswith('/msgroup'):
                  message_parts = message.split(",")
                  groupe_name = message_parts[1]
                  messag = message_parts[2]
                  Message = f":> ({groupe_name}) {username} : {messag}"
                  Mes = f"({groupe_name}) From {username} : {messag}"
                  
                  dest_socket = None  
                  if groupe_name in groupes:
                    if username in groupes.get(groupe_name, []):
                        membre_of_group = groupes[groupe_name]
                        insertmsg_grp(username, Mes) #the sender of message to base de donnes
                        for member in membre_of_group:
                          if member != username:
                            ind = usernames.index(member)
                            dest_socket = clients[ind]
                            if dest_socket :
                               dest_socket.send(Message.encode('utf-8'))
                               insertmsg_grp(member, Mes)
            
                    else:
                              client.send(f":> Vous n'êtes pas membre du groupe {groupe_name}.\n Demandez à l'un des membres de vous ajouter.".encode('utf-8'))
                  else:
                           client.send(f":> Le groupe {groupe_name} n'existe pas. Créez-le.".encode('utf-8'))

                    
            elif message.startswith("/remove:"):
                    message_par = message.split(":")
                    membre_remov=message_par[1]
                    grou_name=message_par[2]
                    if Admin[grou_name] == username :
                       groupes[grou_name].remove(membre_remov)
                       clients[usernames.index(membre_remov)].send(f":> Vous n'êtes pas membre de {grou_name} actuellement.".encode('utf-8'))
                       Diffusion(f"GROUPES= {groupes}".encode("utf-8"))
                    else :
                        client.send(":> Vous ne pouvez pas supprimer de membre ;\n vous n'êtes pas l'admistrateur.".encode('utf-8'))

                    
            # Normal message
            else:
                
                    # Diffuser un message.
                    for i in clients:
                        if i != client:  # Diffuser le message uniquement aux autres clients, pas au client expéditeur.
                            i.send((f"{username} : {message}").encode("utf-8"))
                    insertmsg(username, message)
                    for i in usernames:
                        if i != username :
                            insertmsg(i,f'From {username} : {message}') #Ajouter le message reçu à la base de données des données du salon.
        
        except ConnectionResetError:#Erreur,si un client quitte et que le serveur est toujours dans la boucle d'acceptation ou de réception.
            # Gérer la déconnexion de manière élégante
            gestion_deconnexion(client, username)
            break
        except Exception as e:
            if exitOk== True :
                print(f"Exception: {e}")
                break

def gestion_deconnexion(client, username):
    try:
        
        Diffusion(f"\n{username} a quitté la discussion.".encode("utf-8"))
        usernam = usernames[clients.index(client)] #Trouver le nom d'utilisateur correspondant au client déconnecté
        clients.remove(client)
        client.close()
        usernames.remove(usernam)
        print(f'{usernam} est déconnecté')
        Diffusion(f"ONLINE= {usernames}".encode("utf-8"))  #Liste si quelqu'un est déconnecté
    except ValueError:
        print("Gestion des erreurs de déconnexion : Client non trouvé dans la liste.")


#Fonction pour diffuser des messages à tous les clients
def Diffusion(message):
        for i in clients:
            i.send(message)

#Fonction principale pour recevoir des messages des clients.
def accept_clients():
    while True:
        try:
            client, address = server.accept()
            print(f"Connecté avec {str(address)}")
            clients.append(client)
            
            #La fonction de gestion des clients devrait être lancée dans un thread distinct pour chaque client
            t = threading.Thread(target=gestion_client, args=(client,)) 
            t.start()

        except Exception as e:
            print(f"Exception dans la fonction accept_clients :{e}")

def gestion_client(client):
    YES=0
    account = True
    command = (client.recv(1024)).decode("utf-8")
    
    if command == "/login":
     try: 
        k=0
        ok=0
        attempts = 3    #Permettre trois tentatives pour le mot de passe.
        client.settimeout(120) #Vous avez 2 minutes pour vous connecter.
        while  attempts > 0:
            
            username = (client.recv(1024)).decode("utf-8")
            password = (client.recv(1024)).decode("utf-8")

            if not username or not password:
                print("Client déconnecté sans envoyer de nom d'utilisateur ou de mot de passe")
                break
            else :
               
               passwd = selectuser(username)
            
            if password == passwd:
                attempts = 3  # Réinitialiser le compteur de tentatives.
                YES=1
                usernames.append(username)
                client.send("CONNECTED DONE".encode("utf-8"))
                print(f"{username} is connected")
                time.sleep(0.2)
                Diffusion(f"ONLINE= {usernames}".encode("utf-8")) #Lister si quelqu'un est connecté
                
                break
                
            elif password == '/exit':
                print("Le client a demandé à quitter.")
                clients.remove(client)
                client.close()
                print("Le client a quitté sans se connecter.")
                break
                
            elif passwd is None :
                client.send("No_account".encode('utf-8'))
                account = False
                break
            
            elif passwd != password:
                attempts -= 1
                if attempts != 0:
                    client.send(f"Mot de passe incorrect. Il reste {attempts} tentatives.".encode("utf-8"))
                elif attempts == 0:
                    client.send(f"votre tentatives fini.".encode("utf-8"))
                    account = False
                    break
                
        if attempts == 0 :
            account = False # Pour aller à l'inscription.
            
     except socket.timeout:
        print("Expiration du délai et le client n'a pas envoyé ses informations.")
        client.send("Timeout".encode('utf-8'))
        YES = 0
        clients.remove(client)
        client.close()

     except Exception as e:
        print(f"Exception dans la gestion du client :{e}")
        clients.remove(client)
        client.close()
   
    if command=='/signup' or account == False:
        
            try:
                      # Recevoir le nom d'utilisateur et le mot de passe du client
                       name= None
                       username = client.recv(1024).decode("utf-8")
                       password = client.recv(1024).decode("utf-8")
                       name= selectusername(username)
                       
                       if password == "/exit" or username == "/exit":
                           clients.remove(client)
                           client.close()
                           
                           print("Le client quitte lors de l'inscription.")
                         
                       elif name == username :
                        
                            client.send("/user_exit deja".encode("utf-8"))
                            username = client.recv(1024).decode("utf-8")
                            password = client.recv(1024).decode("utf-8")
                            if username != name :
                               client.send("Compte cree".encode("utf-8"))
                               YES=1
                               usernames.append(username)
                               insertuser(username, password)
                               Diffusion(f"ONLINE= {usernames}".encode("utf-8"))
                               
            
                                
                            
                       else:
                            YES=1
                            usernames.append(username)
                            insertuser(username, password)
                            client.send("Compte cree".encode("utf-8"))
                            print(f"Requête d'inscription reçue de {username}")
                            Diffusion(f"ONLINE= {usernames}".encode("utf-8")) 
                            
                            
                       
            except Exception as e:
                       print(f"Exception dans la fonction create_account: {e}")
                       print("Le client a rencontré une erreur lors de l'inscription.")
                       clients.remove(client)
                       client.close()
            
    elif command=='/exit': #Exit avant l'inscription ou la connexion.
        
        clients.remove(client)
        client.close()
        print("Le client a quitté.")
        
    if command == "/signup" or command == "/login":
        if YES == 1:
            diffusion_msg(client, username)
    
    
def main():
    create_table()
    print("En attente de connexions entrantes...")
    accept_clients()

main()
