import socket
import threading
from tkinter import *
import time
from tkinter import ttk
import json
from time import strftime
from tkinter import messagebox


# Création d'un objet socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT= 8489

#adresse IP locale
#IP server here to connect in different machine
IP = '127.0.0.1'

# Connexion au serveur
client.connect((IP, PORT))

# Classe pour l'écran de connexion ou d'inscription
class login_or_signup:
    def __init__(self, client):
        self.client = client
        self.window = Tk()
        self.window.geometry("450x600+80+40")
        self.window.iconbitmap(default="icon.ico")
        self.window.resizable(height=False,width=False)
        self.window.title("Login or Sign up")
        self.window.protocol("WM_DELETE_WINDOW", self.EXit)
        self.window['bg'] = '#3498db'
        self.login_button = Button(self.window, text="login", fg='black', bg='#FFA500',bd=0, highlightthickness=0, command=self.login)
        self.login_button.place(x='145',y='257')
        self.sign_button = Button(self.window, text="sign up", fg='black', bg='#4CAF50',bd=0, highlightthickness=0, command=self.sign)
        self.sign_button.place(x='195',y='257')
        self.exit_B = Button(self.window, text="EXIT", fg='white', bg='#FF0000',bd=0, highlightthickness=0, command=self.EXit)
        self.exit_B.place(x='255', y='257')
        self.photo = PhotoImage(file="student.png")
        self.label = Label(self.window, image=self.photo,bg="#3498db")
        self.label.place(x='140',y='60')
        

    # Méthode appelée lors de la fermeture de la fenêtre
    def EXit(self):
        client.send("/exit".encode("utf-8"))
        self.window.destroy()
        
    # Méthode pour passer à l'écran d'inscription
    def sign(self):
        self.client.send('/signup'.encode('utf-8'))
        self.window.destroy()
        sign_screen = sign_up(self.client)
        sign_screen.start()
    
    # Méthode pour passer à l'écran de connexion
    def login(self):
        self.client.send('/login'.encode('utf-8'))
        self.window.destroy()
        login_screen = LoginScreen(self.client)
        login_screen.start()
    
    def start(self):
        self.window.mainloop()

# Classe pour l'écran d'inscription
class sign_up :
    def __init__(self, client):
        self.client = client
        self.window = Tk()
        self.window.geometry("450x600+80+40")
        self.window.title("sign up")
        self.window.iconbitmap(default="icon.ico")
        self.window['bg'] = '#3498db'  # Background color
        self.username_label = Label(self.window, text="Username:", foreground="white", background="#333333")
        self.password_label = Label(self.window, text="Password:", foreground="white", background="#333333")
        self.login_button = Button(self.window, text="signup", fg='white', bg='#9932CC',bd=0, highlightthickness=0, command=self.signup)
        self.exit2_button = Button(self.window, text="QUITTE", fg='white', bg='red',bd=0, highlightthickness=0, command=self.Exit)
        self.window.resizable(height=False,width=False)
        self.username_label.place(x='80',y='260')
        self.username_entry = Entry(self.window)
        self.username_entry.focus()         
        self.username_entry.place(x='150',y='260')
        self.password_label.place(x='80',y='290')
        self.password_entry = Entry(self.window)
        self.password_entry.config(show='*')        
        self.password_entry.place(x='150',y='290')
        self.window.protocol("WM_DELETE_WINDOW", self.Exit)
        self.login_button.place(x='150',y='320')
        self.exit2_button.place(x='200',y='320')
        self.photo = PhotoImage(file="student.png")
        self.label = Label(self.window, image=self.photo,bg="#3498db")
        self.label.place(x='140',y='60')
        
          
    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username=="" and password=="":
            messagebox.showerror("AGDiD CHAT", "veuillez entrer le nom d'utilisateur et le mot de passe.", parent=self.window)
        if username=="" or password=="":
            messagebox.showerror("AGDiD", "veuillez entrer toutes les données.", parent=self.window)
        
        else:
            #Envoyer le nom d'utilisateur et le mot de passe au serveur
             self.client.send(username.encode('utf-8'))
             time.sleep(0.1)  #temps entre les deux
             self.client.send(password.encode('utf-8'))
             msg_s=self.client.recv(1024).decode("utf-8")
             if msg_s=='Compte cree':
                messagebox.showinfo("AGDiD CHAT", f"  {username}, votre compte est créé.", parent=self.window)
                self.window.destroy()
                chat_screen = ChatScreen(self.client)
                chat_screen.start()
             elif msg_s.startswith("/user_exit deja"):
                 messagebox.showerror("user existe déjà", "Veuillez choisir un autre nom d'utilisateur ou ajouter un nombre à celui-ci." , parent=self.window)
    
    def Exit(self):
        
        client.send('/exit'.encode('utf-8'))  
        self.window.destroy()
        
        
    def start(self):
        self.window.mainloop()
    
# Classe pour l'écran de connexion
class LoginScreen:
    def __init__(self, client):
        self.client = client
        self.window = Tk()
        self.window.geometry("450x600+80+40") 
        self.window.title("Login")
        self.window.iconbitmap(default="icon.ico")
        self.window['bg'] = '#3498db' 
        self.username_label = Label(self.window, text="Username:", foreground="white", background="#333333")
        self.password_label = Label(self.window, text="Password:", foreground="white", background="#333333")
        self.login_button = Button(self.window, text="Login", fg='white', bg='#9932CC',bd=0, highlightthickness=0, command=self.login)
        self.exit2_button = Button(self.window, text="QUITTE", fg='white', bg='red',bd=0, highlightthickness=0, command=self.Exit)
        self.window.resizable(height=False,width=False)
        self.username_label.place(x='80',y='260')
        self.username_entry = Entry(self.window)
        self.username_entry.focus()         
        self.username_entry.place(x='150',y='260')
        self.window.protocol("WM_DELETE_WINDOW", self.Exit)
        self.password_label.place(x='80',y='290')
        self.password_entry = Entry(self.window)
        self.password_entry.config(show='*')       
        self.password_entry.place(x='150',y='290')
        
        self.login_button.place(x='150',y='320')
        self.exit2_button.place(x='200',y='320')
        self.photo = PhotoImage(file="student.png")
        self.label = Label(self.window, image=self.photo,bg="#3498db")
        self.label.place(x='140',y='60')
        
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username=="" and password=="":
            messagebox.showerror("AGDiD CHAT", "veuillez entrer le nom d'utilisateur et le mot de passe.", parent=self.window)
        if username=="" or password=="":
            messagebox.showerror("AGDiD", "veuillez entrer toutes les données.", parent=self.window)
        #Envoyer le nom d'utilisateur et le mot de passe au serveur
        else:
            self.client.send(username.encode('utf-8'))
            time.sleep(0.1)  
            self.client.send(password.encode('utf-8'))
        
            msg=self.client.recv(1024).decode("utf-8")
            if msg != 'CONNECTED DONE':
                 
                 if msg.startswith("Mot de passe incorrect."):
                     messagebox.showerror("Mot de passe", msg, parent=self.window)
                 elif msg.startswith("votre tentatives fini"):
                     messagebox.showerror("AGDiD CHAT", "Votre tentative a échoué. Essayez à nouveau. Si vous avez besoin de créer un compte, faites-le.", parent=self.window)
                     self.window.destroy()
                     sign_screen = sign_up(self.client)
                     sign_screen.start()
                 elif msg == 'No_account' :
                    messagebox.showerror("AGDiD CHAT", "veuillez créer un compte", parent=self.window)
                    self.window.destroy()
                    sign_screen = sign_up(self.client)
                    sign_screen.start()
                 elif msg == 'Timeout':
                     messagebox.showerror("Time end", "Le temps d’inscription se termine.", parent=self.window)
                     self.window.destroy()
            else:
                   messagebox.showinfo("AGDiD CHAT", f"{username}, bienvenue", parent=self.window)
                   self.window.destroy()
                   chat_screen = ChatScreen(self.client)
                   chat_screen.start()
        
    def Exit(self):
        self.password_entry.delete(0,END)
        self.password_entry.insert(0, '/exit')
        self.window.destroy()
        
        
    def start(self):
        self.window.mainloop()

class ChatScreen:
    def __init__(self, client):
        self.exitOk = False
        self.client = client
        self.window = Tk()
        self.window.title("Instant Messaging")
        self.window.geometry("450x630+80+30")
        self.window['bg'] = '#3498db'  
        self.window.iconbitmap(default="icon.ico")
        self.window.resizable(height=False, width=False)
        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        self.time_label = Label(self.window, font=('calibri', 10, 'bold'), background='white', foreground='black')
        self.time_label.pack(side="top", fill="both")
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=1, fill='both')
        self.salon_frame = Frame(self.notebook, bg='lightblue')
        self.private_frame = Frame(self.notebook, bg='lightgreen')
        self.groupe_frame = Frame(self.notebook, bg='#E6E6FA')
        self.notebook.add(self.salon_frame, text='Salon')
        self.notebook.add(self.private_frame, text='Privé')
        self.notebook.add(self.groupe_frame, text='Groupe')
        self.init_salon_chat()
        self.init_private_chat()
        self.init_groupe_chat()
    
    def update_time(self):
            time_now = strftime('%H:%M:%S %p')
            self.time_label.config(text=time_now)
            self.window.after(1000, self.update_time)  #Mettre à jour toute seconde
    
    
    def init_salon_chat(self):
        self.message_label_salon = Label(self.salon_frame, text="MESSAGE :", fg='black', bg='lightblue')
        self.send_button_salon = Button(self.salon_frame, text="SEND", fg='white', bg='green',bd=0, highlightthickness=0, command=self.send_salon)
        self.exit_button_salon = Button(self.salon_frame, text="EXIT", fg='white', bg='red',bd=0, highlightthickness=0, command=self.exit)
        self.message_label_salon.place(x='80', y='520')
        self.message_entry_salon = Entry(self.salon_frame)
        self.message_entry_salon.place(x='140', y='520')
        self.message_entry_salon.focus()
        self.send_button_salon.place(x='270', y='519')
        self.exit_button_salon.place(x='380', y='519')

        # chat box
        self.chat_box_salon = Text(self.salon_frame,font=('Urban',  10,'bold') ,bg='#E0E0E0', height=29, width=62)
        self.chat_box_salon.place(x='6', y='47')
        self.History_button_salon = Button(self.salon_frame, text="HISTORY", fg='black', bg='#FFC107',bd=0, highlightthickness=0, command=self.sendH_salon)
        self.History_button_salon.place(x='315', y='519')
        
        # Modifier le nom d'utilisateur pour l'onglet Salon
        self.username_Buttonchange_salon = Button(self.salon_frame, text="USERNAME", fg='white', bg='purple',bd=0, highlightthickness=0, command=self.changeUserSalon)
        self.username_Buttonchange_salon.place(x='20', y='550')
        self.usernamechange_entry_salon = Entry(self.salon_frame)
        self.username_Buttonchange_salon = Button(self.salon_frame, text="OK", fg='black', bg='green',bd=0, highlightthickness=0, command=self.sendnewnameSalon)
        self.online_box_salon = Text(self.salon_frame, bg='lightblue', height=2, width=54)
        self.online_box_salon.place(x='5', y='5')
        self.del_button_salon = Button(self.salon_frame, text="DEL BOX", fg='white', bg='red',bd=0, highlightthickness=0, command=self.deletebox)
        self.del_button_salon.place(x='20', y='519')
        
        
        self.chat_box_salon.tag_config("sent", foreground="purple")
        self.chat_box_salon.tag_config("received", foreground="purple") 
        
    def init_private_chat(self):
        self.destinateur_label_private = Label(self.private_frame, text="DESTINATAIRE :", fg='black', bg='lightgreen')
        self.message_label_private = Label(self.private_frame, text="MESSAGE :", fg='black', bg='lightgreen')
        self.send_button_private = Button(self.private_frame, text="SEND", fg='white', bg='green',bd=0, highlightthickness=0, command=self.send_private_destinateur)
        self.exit_button_private = Button(self.private_frame, text="EXIT", fg='white', bg='red',bd=0, highlightthickness=0, command=self.exit)
        self.destinateur_label_private.place(x='50', y='490')
        self.destinateur_entry_private = Entry(self.private_frame)
        self.destinateur_entry_private.place(x='140', y='490')
        self.destinateur_entry_private.focus()
        
        self.message_label_private.place(x='80', y='520')
        self.message_entry_private = Entry(self.private_frame)
        self.message_entry_private.place(x='140', y='520')
    
        self.send_button_private.place(x='270', y='519')
        self.exit_button_private.place(x='380', y='519')

        # chat box
        self.chat_box_private = Text(self.private_frame,font=('Urban',  10,'bold') ,bg='#E0E0E0', height=27, width=62)
        self.chat_box_private.place(x='6', y='47')
        self.History_button_private = Button(self.private_frame, text="HISTORY", fg='black', bg='#FFC107',bd=0, highlightthickness=0, command=self.sendH_private)
        self.History_button_private.place(x='315', y='519')
        
        self.del_button_private = Button(self.private_frame, text="DEL BOX", fg='white', bg='red',bd=0, highlightthickness=0, command=self.deleteboxprivate)
        self.del_button_private.place(x='20', y='518')
        
        
        self.username_Buttonchange_private = Button(self.private_frame, text="USERNAME", fg='white', bg='purple',bd=0, highlightthickness=0, command=self.changeUserPrivate)
        self.username_Buttonchange_private.place(x='20', y='550')
        self.usernamechange_entry_private = Entry(self.private_frame)
        self.username_Buttonchange_private = Button(self.private_frame, text="OK", fg='black', bg='#4CAF50',bd=0, highlightthickness=0, command=self.sendnewnamePrivate)
        self.online_box_private = Text(self.private_frame, bg='lightgreen', height=2, width=54)
        self.online_box_private.place(x='5', y='5')
    
        
       
        self.chat_box_private.tag_config("sent", foreground="purple")
        self.chat_box_private.tag_config("received", foreground="purple") 
    
    def init_groupe_chat(self):
        
        self.message_label_groupe = Label(self.groupe_frame, text="MESSAGE :", fg='black', bg='#E6E6FA')
        self.send_button_groupe = Button(self.groupe_frame, text="Send", fg='white', bg='green',bd=0, highlightthickness=0, command=self.send_groupe)
        self.exit_button_groupe = Button(self.groupe_frame, text="EXIT", fg='white', bg='red',bd=0, highlightthickness=0, command=self.exit)
        self.message_label_groupe.place(x='80', y='550')
        self.message_entry_groupe = Entry(self.groupe_frame)
        self.message_entry_groupe.place(x='140', y='550')
        self.message_entry_groupe.focus()
        self.send_button_groupe.place(x='270', y='549')
        self.exit_button_groupe.place(x='310', y='549')

       
        self.create_group_entry = Entry(self.groupe_frame)
        self.create_group_entry.place(x='140', y='490')

        self.create_group_buton = Button(self.groupe_frame, text="CREATE GROUPE", fg='white', bg='purple',bd=0, highlightthickness=0,command=self.create_comd_affiche)
        self.create_group_buton.place(x='37', y='490')
        self.create_group_button = Button(self.groupe_frame, text="CREATE", fg='white', bg='purple',bd=0, highlightthickness=0,command=self.create_group) 
        # chat box
        self.chat_box_groupe = Text(self.groupe_frame,font=('Urban',  10,'bold') ,bg='#E0E0E0', height=25, width=62)
        self.chat_box_groupe.place(x='6', y='80')
        self.History_button_groupe = Button(self.groupe_frame, text="HISTORY", fg='black', bg='#FFC107',bd=0, highlightthickness=0, command=self.sendH_groupe) # command=self.sendH_groupe
        self.History_button_groupe.place(x='348', y='549')
        
        self.membre_groupe = Label(self.groupe_frame, text="MEMBRE :", fg='black', bg='#E6E6FA')
        self.membre_groupe.place(x='80', y='520')
        
        self.membre_entry = Entry(self.groupe_frame)
        self.button_send_membre = Button(self.groupe_frame, text="SEND MBR", fg='white', bg='#6495ED',bd=0, highlightthickness=0,command=self.send_membre_groupe)
        self.membre_entry.place(x='140', y='519')
        self.button_send_membre.place(x='270', y='519')
        self.online_box_client_groupe = Text(self.groupe_frame, bg='#E6E6FA', height=2, width=54)
        self.online_box_client_groupe.place(x='5', y='0')
        
        self.online_box_groupe = Text(self.groupe_frame, bg='#E6E6FA', height=2, width=54)
        self.online_box_groupe.place(x='6', y='41')
        self.online_box_groupe.insert(END, "créer un groupe et profitez de bons moments ensemble")
      
        self.del_button_groupe = Button(self.groupe_frame, text="DEL BOX", fg='white', bg='red',bd=0, highlightthickness=0, command=self.deleteboxgroupe)
        self.del_button_groupe.place(x='16', y='547')
        self.remove_button_groupe = Button(self.groupe_frame, text="REMOVE", fg='white', bg='#FF4500',bd=0, highlightthickness=0, command=self.remove_membre) # command=self.sendH_groupe
        self.remove_button_groupe.place(x='348', y='520')
        
        self.chat_box_groupe.tag_config("sent", foreground="purple")
        self.chat_box_groupe.tag_config("received", foreground="purple") 
    
    def send_private_destinateur(self):
        destinateur = self.destinateur_entry_private.get()
        if destinateur in self.onlineclientlist:
           message = self.message_entry_private.get()
           self.message_entry_private.delete(0,END)
           self.client.send(f"/private {destinateur} : {message}".encode('utf-8'))
           
           self.chat_box_private.insert(END, f"\nTo {destinateur} : {message}", "sent")
        else:
          self.chat_box_private.insert(END, f"\nL'utilisateur n'est pas en ligne ou n'existe pas.")
    
    def remove_membre(self):
        rm=self.membre_entry.get()
        gr_name=self.create_group_entry.get()
        client.send(f'/remove:{rm}:{gr_name}'.encode("utf-8"))
        
    def create_group(self):
          self.group_name = self.create_group_entry.get()
          if self.group_name :
        
             self.client.send(f"/create_groupe {self.group_name}".encode("utf-8"))
             self.create_group_button.place_forget()
          else:
               pass
           
    def create_comd_affiche(self):
        
        self.create_group_button.place(x='270', y='490')

  
    def exit(self):
        if self.exitOk == False:
            self.client.send("/exit".encode('utf-8'))
            self.window.destroy()
            self.exitOk = True #true pour terminer la boucle dans recvmessage

    def sendH_salon(self):
         self.client.send("H_SALON".encode('utf-8'))

    def sendH_private(self):
         self.client.send("H_PRIVATE".encode('utf-8'))
    
    def sendH_groupe(self):
         self.client.send("H_GROUPE".encode('utf-8'))
    

    def changeUserSalon(self):
      self.usernamechange_entry_salon.place(x='95', y='555')  
      self.username_Buttonchange_salon.place(x='230', y='553')  
      self.usernamechange_entry_salon.focus()

    def sendnewnameSalon(self):
        username = self.usernamechange_entry_salon.get()
        
        self.client.send("NEWUSERNAME".encode("utf-8"))
        time.sleep(0.1)  
        self.client.send(username.encode('utf-8'))
        self.usernamechange_entry_salon.delete(0, END)
        
        self.usernamechange_entry_salon.place_forget()
        self.username_Buttonchange_salon.place_forget()

    def changeUserPrivate(self):
       self.usernamechange_entry_private.place(x='95', y='555')  
       self.username_Buttonchange_private.place(x='230', y='553')  
       self.usernamechange_entry_private.focus()

    def sendnewnamePrivate(self):
        username = self.usernamechange_entry_private.get()
        
        self.client.send("NEWUSERNAME".encode("utf-8"))
        time.sleep(0.1)
        self.client.send(username.encode('utf-8'))
        self.usernamechange_entry_private.delete(0, END)
     
        self.usernamechange_entry_private.place_forget()
        self.username_Buttonchange_private.place_forget()
        
    def send_salon(self):
        message = self.message_entry_salon.get()
        if message:
            self.chat_box_salon.insert(END, "\n" + "You: " + message, "sent") 
        self.client.send(message.encode('utf-8'))
        
        self.message_entry_salon.delete(0, END)
    
    def send_membre_groupe(self):
        
        membr=self.membre_entry.get()
        group=self.create_group_entry.get()
        if group and membr :
          self.membre_entry.delete(0,END)
          membre=membr.split(",")
          # Convertir la liste des membres en une chaîne formatée en JSON 
          # vous ne pouvez pas envoyer une liste
          json_char = json.dumps(membre)
          client.send(f"/grp_mbr+{group}+{json_char}".encode("utf-8"))
         
         
    def send_groupe(self):
        message = self.message_entry_groupe.get()
        groupname=self.create_group_entry.get()
        
        if message :
            
            msgroup=f'/msgroup,{groupname},{message}'
            self.client.send(msgroup.encode('utf-8'))
            self.chat_box_groupe.insert(END, f"({groupname}) YOU : {message}\n", "sent")
            self.message_entry_groupe.delete(0, END)
              
    def recvonline(self, msg):
        if msg.startswith('ONLINE='):
           try: 
            # Supprimer tous les éléments dans la Listbox
               self.online_box_salon.delete("1.0", END)
               self.online_box_private.delete("1.0", END)
               self.online_box_client_groupe.delete("1.0", END)
               
            # Insert each online client into the Listbox
               self.online_box_salon.insert(END, msg)
               self.online_box_private.insert(END, msg)
               self.online_box_client_groupe.insert(END, msg)
            #Sauvegarder la liste des clients en ligne.
               self.onlineclientlist=msg
           except:
               print("except in sending online list")


    def recv_msg(self):
       while self.exitOk == False: #Vous ne pressez pas sur 'Exit'
          try:
            msg = self.client.recv(1024).decode("utf-8")
            if msg.startswith('/private'):
               
                message_parts = msg.split(" ")
                sender = message_parts[1]
                message = " ".join(message_parts[3:])
                self.chat_box_private.insert(END, f"\nFrom {sender} : {message}")
                
            elif msg.startswith('Votre Historique :'):
                self.chat_box_salon.insert(END, "\n" + msg,"received")
                
            elif msg.startswith('Votre Historique Privé : '):
                self.chat_box_private.insert(END, "\n" + msg,"received")
                
            elif msg.startswith('>>'):
                self.chat_box_private.insert(END, "\n" + msg,"received")
            
            elif msg.startswith(">"):
                self.chat_box_salon.insert(END, "\n" + msg,"received")
                
            elif msg.startswith('ONLINE='):
                self.online_box_salon.delete("1.0", END)
                self.online_box_private.delete("1.0", END)
                self.online_box_client_groupe.delete("1.0", END)
                self.online_box_salon.insert(END, msg)
                self.online_box_private.insert(END, msg)
                self.online_box_client_groupe.insert(END, msg)
                self.onlineclientlist=msg
            
            elif msg.startswith("Votre Historique Groupe :"):
                self.chat_box_groupe.insert(END,msg+"\n","received")
                
            elif msg.startswith(":>>"): 
                self.chat_box_groupe.insert(END,msg+"\n","received")
                
            elif msg.startswith("Vous n'êtes pas membre du groupe"):
                self.chat_box_groupe.insert(END,msg+"\n","received")
        
            elif msg.startswith("GROUPES="):
                  self.online_box_groupe.delete('1.0', END)
                  self.online_box_groupe.insert(END, msg)

            elif msg.startswith(":>") :
                self.chat_box_groupe.insert(END,msg+"\n")
           
            else:
                
                self.chat_box_salon.insert(END, "\n" + msg)
                  
          except Exception as e:
                 if self.exitOk == True:
                    print(f"client quitte and loop of threads is end {e}")
                    break

             
    def deleteboxgroupe(self):
            self.chat_box_groupe.delete("1.0", END)
    def deletebox(self):
             self.chat_box_salon.delete("1.0", END)  
    def deleteboxprivate(self):
             self.chat_box_private.delete("1.0", END)  

    def start_threads(self):
        threading.Thread(target=self.recv_msg).start()

    def start(self):
        self.start_threads()
        self.update_time()
        self.window.mainloop()
    
#fonction principale
def main():
    login_sign_screen = login_or_signup(client)
    login_sign_screen.start()
    
# appel de la fonction principale
main()
