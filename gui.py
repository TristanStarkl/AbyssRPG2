from tkinter import *
from stats import *
import tkinter.ttk as ttk
import server
import random
import queue
import chat
from threading import Thread, RLock
import socket




windows = Tk()
windows.title("Abyss RPG")
windows.geometry("1600x900")
windows.resizable(False, False)

character = personnage(0, 0, 0, 0, 0, 0, 0)

background_image= PhotoImage(file="./ressources/background.png")
background_label = Label(windows, image=background_image)
background_label.pack()

inventaire_box = Text(bd=0, height=24, undo=True, width=100)
inventaire_box.place(x=740,y=460)

name_box = Text(bd=0, height=1, undo=True, width=24)
name_box.place(x=150, y=105)

first_name_box = Text(bd=0, height=1, undo=True, width = 24)
first_name_box.place(x=150, y=140)

age_box = Text(bd=0, height=1, undo=True, width = 3)
age_box.place(x=150, y=175)

notes_box = Text(bd=0, height=15, undo=True, width = 37)
notes_box.place(x=40, y=355)

"""120 255 pré apo
120 285 post apo"""
liste_metiers_1 = []
liste_metiers = save.loadFromFile("professions")
for metier in liste_metiers:
	liste_metiers_1.append(metier.name)

liste_etat_1 = []
liste_etat = save.loadFromFile("etat")
for etat in liste_etat:
	liste_etat_1.append(etat.name)


liste_blessure_1 = []
liste_blessure = save.loadFromFile("blessures")
for bles in liste_blessure:
	liste_blessure_1.append(bles.name)




liste_metier_pre_apo = Text(bd=0, height=1, undo=True, width = 24)
liste_metier_pre_apo.place(x=120, y=250)

liste_etat_box = ttk.Combobox(windows, values=liste_etat_1, width=40, height=45)
liste_etat_box.place(x=390, y=95)

liste_blessure_box = ttk.Combobox(windows, values=liste_blessure_1, width=40, height=45)
liste_blessure_box.place(x=390, y=150)

liste_metier_post_apo = ttk.Combobox(windows, values=liste_metiers_1)
liste_metier_post_apo.place(x=120, y=280)


listes_blessures_chara = []
liste_button_blessure_chara = []	
photo_croix = PhotoImage(file='./ressources/croix.png')
blessure_X = 1160
blessure_Y = 80
nbBlessures = 0

def destroy_blessure(label, name):
	global liste_blessure_chara
	global liste_button_blessure_chara
	i = listes_blessures_chara.index(label)
	a = listes_blessures_chara.pop(i)
	global character
	b = liste_button_blessure_chara.pop(i)
	for bobo in liste_blessure:
		if (bobo.name == name):
			break
	character.removeBlessure(bobo.name)
	a.place_forget()
	b.place_forget()
	global blessure_Y
	global blessure_X
	del a
	del b
	global nbBlessures
	nbBlessures -= 1
	blessure_Y = 80
	for label in listes_blessures_chara:
		label.place(x=blessure_X, y=blessure_Y)
		blessure_Y += 35
	blessure_Y = 80
	for bu in liste_button_blessure_chara:
		bu.place(x=1500, y=blessure_Y)
		blessure_Y += 35
	windows.update()
	updateStat()
	#saveCharacter()
	#loadCharacter()

def ajouter_blessures(name):
	for bobo in liste_blessure:
		if (bobo.name == name):
			break
	global blessure_X
	global blessure_Y
	global nbBlessures
	global character

	if (nbBlessures >= 3):
		return 

	label = Label(windows, text=name, bg="white")
	button = Button(windows, text="", relief=FLAT, image=photo_croix, command=lambda m=label: destroy_blessure(label, name))
	liste_button_blessure_chara.append(button)
	listes_blessures_chara.append(label)
	label.place(x=blessure_X, y=blessure_Y)
	button.place(x=1500,y=blessure_Y)
	blessure_Y += 35
	nbBlessures += 1
	character.addBlessure(bobo)
	#saveCharacter()
	updateStat()

def delete_all_blessure():
	global blessure_X
	global blessure_Y
	global nbBlessures
	global listes_blessures_chara
	global liste_button_blessure_chara
	for l in listes_blessures_chara:
		l.place_forget()
		del l
	for b in liste_button_blessure_chara:
		b.place_forget()
		del b
	listes_blessures_chara = []
	liste_button_blessure_chara = []
	blessure_X = 1160
	blessure_Y = 80
	nbBlessures = 0


def blessures_append():
	blessure_name = liste_blessure_box.get()
	ajouter_blessures(blessure_name)

button_plus = PhotoImage(file="./ressources/plus.png")
button_append_blessure = Button(windows, text="", relief=FLAT, image=button_plus, command=blessures_append)
button_append_blessure.place(x=669, y=148)

force = Text(bd=0, height=1, undo=True, width=2)
force.config(font=("Gabriola", 28))
force.place(x=640, y=240-40)

endurance = Text(bd=0, height=1, undo=True, width=2)
endurance.config(font=("Gabriola", 28))
endurance.place(x=640, y=335-30)

intelligence = Text(bd=0, height=1, undo=True, width=2)
intelligence.config(font=("Gabriola", 28))
intelligence.place(x=640, y=430-30)

perception = Text(bd=0, height=1, undo=True, width=2)
perception.config(font=("Gabriola", 28))
perception.place(x=640, y=525-30)

social = Text(bd=0, height=1, undo=True, width=2)
social.config(font=("Gabriola", 28))
social.place(x=640, y=620-30)

agilite = Text(bd=0, height=1, undo=True, width=2)
agilite.config(font=("Gabriola", 28))
agilite.place(x=640, y=720-30)

chance = Text(bd=0, height=1, undo=True, width=2)
chance.config(font=("Gabriola", 28))
chance.place(x=640, y=815-30)

currentForce = Text(bd=0, height=1, undo=True, width=2)
currentForce.config(font=("Gabriola", 28))
currentForce.place(x=580, y=240-40)

currentEndurance = Text(bd=0, height=1, undo=True, width=2)
currentEndurance.config(font=("Gabriola", 28))
currentEndurance.place(x=580, y=335-30)

currentIntelligence = Text(bd=0, height=1, undo=True, width=2)
currentIntelligence.config(font=("Gabriola", 28))
currentIntelligence.place(x=580, y=430-30)

currentPerception = Text(bd=0, height=1, undo=True, width=2)
currentPerception.config(font=("Gabriola", 28))
currentPerception.place(x=580, y=525-30)

currentSocial = Text(bd=0, height=1, undo=True, width=2)
currentSocial.config(font=("Gabriola", 28))
currentSocial.place(x=580, y=620-30)

currentAgilite = Text(bd=0, height=1, undo=True, width=2)
currentAgilite.config(font=("Gabriola", 28))
currentAgilite.place(x=580, y=720-30)

currentChance = Text(bd=0, height=1, undo=True, width=2)
currentChance.config(font=("Gabriola", 28))
currentChance.place(x=580, y=815-30)

currentMoral = Text(bd=0, height=1, undo=True, width=3)
currentMoral.config(font=("Arial", 14))
currentMoral.place(x=200, y=820)

moral = Text(bd=0, height=1, undo=True, width=3)
moral.config(font=("Arial", 14))
moral.place(x=290, y=820)

currentStam = Text(bd=0, height=1, undo=True, width=3)
currentStam.config(font=("Arial", 14))
currentStam.place(x=200, y=740)

stam = Text(bd=0, height=1, undo=True, width=3)
stam.config(font=("Arial", 14))
stam.place(x=290, y=740)

currentPV = Text(bd=0, height=1, undo=True, width=3)
currentPV.config(font=("Arial", 14))
currentPV.place(x=50, y=740)

pv = Text(bd=0, height=1, undo=True, width=3)
pv.config(font=("Arial", 14))
pv.place(x=120, y=740)

currentPSY = Text(bd=0, height=1, undo=True, width=3)
currentPSY.config(font=("Arial", 14))
currentPSY.place(x=50, y=820)

psy = Text(bd=0, height=1, undo=True, width=3)
psy.config(font=("Arial", 14))
psy.place(x=120, y=820)


liste_chara = []
liste_chara1 = save.loadFromFile("personnage")
for c in liste_chara1:
	liste_chara.append(c.name)
liste_chara_box = ttk.Combobox(windows, values=liste_chara, width=10)
liste_chara_box.place(x=145, y=25)


def get_object(name, defaultValue):
	a = defaultValue
	try:
		a = int(name.get(1.0, END).rstrip('\n'))
	except Exception as E:
		pass
	return a

def saveCharacter():
	global character
	bobo = character.get_list_blessures()
	name = name_box.get(1.0, END).rstrip('\n')
	if (name == ""):
		name = "Sans Nom"
	FORCE = get_object(force, 0)
	ENDURANCE = get_object(endurance, 0)
	INTELLIGENCE = get_object(intelligence, 0)
	PERCEPTION = get_object(perception, 0)
	SOCIAL = get_object(social, 0)
	AGILITE = get_object(agilite, 0)
	CHANCE = get_object(chance, 0)
	CURRENT_FORCE = get_object(currentForce, -1)
	CURRENT_ENDURANCE = get_object(currentEndurance, -1)
	CURRENT_INTELLIGENCE = get_object(currentIntelligence, -1)
	CURRENT_PERCEPTION = get_object(currentPerception, -1)
	CURRENT_SOCIAL = get_object(currentSocial, -1)
	CURRENT_AGILITE = get_object(currentAgilite, -1)
	CURRENT_CHANCE = get_object(currentChance, -1)
	CURRENT_STAM = get_object(currentStam, -1)
	CURRENT_MORAL = get_object(currentMoral, -1)
	CURRENT_PSY = get_object(currentPSY, -1)
	CURRENT_PV = get_object(currentPV, -1)
	NOTES = notes_box.get(1.0, END).rstrip('\n')
	print("NOTES = ", NOTES)
	PV = get_object(pv, 0)
	MORAL = get_object(moral, 0)
	PSY = get_object(psy, 0)
	STAM = get_object(stam, 0)
	perso = personnage(FORCE,
		ENDURANCE,
		INTELLIGENCE,
		PERCEPTION,
		SOCIAL,
		AGILITE,
		CHANCE,
		currentF=CURRENT_FORCE,
		currentE=CURRENT_ENDURANCE,
		currentI=CURRENT_INTELLIGENCE,
		currentP=CURRENT_PERCEPTION,
		currentS=CURRENT_SOCIAL,
		currentA=CURRENT_AGILITE,
		currentC=CURRENT_CHANCE,
		inventaire=inventaire_box.get(1.0, END).rstrip('\n'),
		name=name,
		first_name=first_name_box.get(1.0, END).rstrip('\n'),
		metier_pre_apo=liste_metier_pre_apo.get(1.0, END).rstrip('\n'),
		bobo=bobo, 
		currentStam=CURRENT_STAM,
		currentPv=CURRENT_PV,
		currentMoral=CURRENT_MORAL,
		currentPsy=CURRENT_PSY,
		stam_max=STAM,
		psy=PSY,
		mor=MORAL,
		pv=PV,
		notes=NOTES		)
	save.saveToFile(perso, "personnage")
	global liste_chara
	global liste_chara1
	liste_chara = []
	liste_chara1 = save.loadFromFile("personnage")
	for c in liste_chara1:
		liste_chara.append(c.name)
	global liste_chara_box
	print("Liste_chara = ", liste_chara)
	liste_chara_box["values"] = liste_chara
	global CLIENT
	if (CLIENT.isClient):
		with open("./save/personnage/{}.json".format(name), 'r') as f:
			content = f.read()
		msg = "..{}|{}|{}|{}".format(CLIENT.name, "personnage", name, content)
		CLIENT.send(msg)

def updateStat():

	global character
	for c in liste_chara1:
		if (c.name == character.name):
			character = c
	c.updateSTATS()
	currentForce.delete(1.0, END)
	currentEndurance.delete(1.0, END)
	currentIntelligence.delete(1.0, END)
	currentPerception.delete(1.0, END)
	currentSocial.delete(1.0, END)
	currentAgilite.delete(1.0, END)
	currentChance.delete(1.0, END)
	psy.delete(1.0, END)
	currentPSY.delete(1.0, END)
	pv.delete(1.0, END)
	currentPV.delete(1.0, END)
	stam.delete(1.0, END)
	currentStam.delete(1.0, END)
	moral.delete(1.0, END)
	currentMoral.delete(1.0, END)
	currentForce.insert(INSERT, character.currentF)
	currentEndurance.insert(INSERT, character.currentE)
	currentIntelligence.insert(INSERT, character.currentI)
	currentPerception.insert(INSERT, character.currentP)
	currentSocial.insert(INSERT, character.currentS)
	currentAgilite.insert(INSERT, character.currentA)
	currentChance.insert(INSERT, character.currentC)
	psy.insert(INSERT, character.psy)
	currentPSY.insert(INSERT, character.currentPsy)
	pv.insert(INSERT, character.pv)
	currentPV.insert(INSERT, character.currentPv)
	stam.insert(INSERT, character.stam_max)
	currentStam.insert(INSERT, character.currentStam)
	moral.insert(INSERT, character.mor)
	currentMoral.insert(INSERT, character.currentMoral)

def newCharacter():
	inventaire_box.delete(1.0, END)
	name_box.delete(1.0, END)
	first_name_box.delete(1.0, END)
	age_box.delete(1.0, END)
	notes_box.delete(1.0, END)
	liste_metier_pre_apo.delete(1.0, END)
	force.delete(1.0, END)
	endurance.delete(1.0, END)
	intelligence.delete(1.0, END)
	perception.delete(1.0, END)
	social.delete(1.0, END)
	agilite.delete(1.0, END)
	chance.delete(1.0, END)
	currentForce.delete(1.0, END)
	currentEndurance.delete(1.0, END)
	currentIntelligence.delete(1.0, END)
	currentPerception.delete(1.0, END)
	currentSocial.delete(1.0, END)
	currentAgilite.delete(1.0, END)
	currentChance.delete(1.0, END)
	delete_all_blessure()


	psy.delete(1.0, END)
	currentPSY.delete(1.0, END)
	pv.delete(1.0, END)
	currentPV.delete(1.0, END)
	stam.delete(1.0, END)
	currentStam.delete(1.0, END)
	moral.delete(1.0, END)
	currentMoral.delete(1.0, END)

NAME_CHAT = ""


def loadCharacter():
	saveCharacter()
	chara_name = liste_chara_box.get()
	global character
	for c in liste_chara1:
		if (c.name == chara_name):
			character = c
			break

	c.updateSTATS()
	inventaire_box.delete(1.0, END)
	name_box.delete(1.0, END)
	first_name_box.delete(1.0, END)
	age_box.delete(1.0, END)
	notes_box.delete(1.0, END)
	liste_metier_pre_apo.delete(1.0, END)
	force.delete(1.0, END)
	endurance.delete(1.0, END)
	intelligence.delete(1.0, END)
	perception.delete(1.0, END)
	social.delete(1.0, END)
	agilite.delete(1.0, END)
	chance.delete(1.0, END)
	currentForce.delete(1.0, END)
	currentEndurance.delete(1.0, END)
	currentIntelligence.delete(1.0, END)
	currentPerception.delete(1.0, END)
	currentSocial.delete(1.0, END)
	currentAgilite.delete(1.0, END)
	currentChance.delete(1.0, END)
	delete_all_blessure()


	psy.delete(1.0, END)
	currentPSY.delete(1.0, END)
	pv.delete(1.0, END)
	currentPV.delete(1.0, END)
	stam.delete(1.0, END)
	currentStam.delete(1.0, END)
	moral.delete(1.0, END)
	currentMoral.delete(1.0, END)
	psy.insert(INSERT, character.psy)
	currentPSY.insert(INSERT, character.currentPsy)
	pv.insert(INSERT, character.pv)
	currentPV.insert(INSERT, character.currentPv)
	stam.insert(INSERT, character.stam_max)
	currentStam.insert(INSERT, character.currentStam)
	moral.insert(INSERT, character.mor)
	currentMoral.insert(INSERT, character.currentMoral)

	inventaire_box.insert(INSERT, c.inventaire)
	print("Inventaire de c ({}) = ".format(c.name), c.inventaire)
	name_box.insert(INSERT, c.name)
	first_name_box.insert(INSERT, c.first_name)
	age_box.insert(INSERT, c.age)
	notes_box.insert(INSERT, c.notes)
	liste_metier_pre_apo.insert(INSERT, c.metier_pre_apo)
	for bobo in c.bobo:
		ajouter_blessures(bobo)
	force.insert(INSERT, c.force)
	endurance.insert(INSERT, c.endurance)
	intelligence.insert(INSERT, c.intelligence)
	perception.insert(INSERT, c.perception)
	social.insert(INSERT, c.social)
	agilite.insert(INSERT, c.agilite)
	chance.insert(INSERT, c.chance)
	currentForce.insert(INSERT, c.currentF)
	currentEndurance.insert(INSERT, c.currentE)
	currentIntelligence.insert(INSERT, c.currentI)
	currentPerception.insert(INSERT, c.currentP)
	currentSocial.insert(INSERT, c.currentS)
	currentAgilite.insert(INSERT, c.currentA)
	currentChance.insert(INSERT, c.currentC)


##########################################################"""HEBERGER"""

MUTEX = RLock()
queue1 = queue.Queue()
queue2 = queue.Queue()

SERVER = server.Server(queue1, queue2)
CHAT = chat.Chat(queue2, queue1, MUTEX)

class Client():
	def __init__(self, q, p, mutex):
		#Thread.__init__(self)
		self.isClient = False
		self.queue_v_c = q
		self.queue_f_c = p
		self.mutex = mutex

	def connect(self, ip, port, name):
		try:
			self.ip = ip
			self.port = port
			self.name = name
			self.connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connexion_avec_serveur.connect((self.ip, self.port))
			self.connexion_avec_serveur.setblocking(False)
			self.isClient = True
			msg = "//{} vient de se connecter\n".format(name)
			self.connexion_avec_serveur.send(msg.encode())
		except Exception as e:
			print(e)
			return ("Connexion impossible")
		return ("None")

	def stop(self):
		print("Fermeture")
		self.connexion_avec_serveur.close()

	def send(self, msg):
		self.connexion_avec_serveur.send(msg.encode())


	def run(self):
		msg = ""
		global CHAT
		try:
			print('1')
			msg = self.connexion_avec_serveur.recv(65536)
			print("2")
		except socket.error:
			print("inchallah")
		else:
			if (msg.decode() != "ping"):
				print(" '{}' ".format(msg.decode()))
				try:
					with self.mutex:
						self.queue_v_c.put(msg.decode())
				except queue.Full:
					pass

			try:
				print("Estoy here")
				with self.mutex:
					msg = self.queue_f_c.get()
					print("Je get un message: ", msg)
				self.send(msg)
				CHAT.update()
			except queue.Empty:
				pass

CLIENT = Client(queue1, queue2, MUTEX)


def launch_heberger():
	windows_heberger = Toplevel()
	windows_heberger.title("Héberger")
	windows_heberger.geometry("323x217")
	windows_heberger.resizable(False, False)
	background_image_heberger = PhotoImage(file="./ressources/heberger.png")
	background_label1 = Label(windows_heberger, image=background_image_heberger)
	background_label1.pack()

	heberger_port_var = StringVar()
	heberger_port = Entry(windows_heberger, textvariable=heberger_port_var, width=5)
	heberger_port.place(x=70, y=60)

	nb_max_joueur_var = StringVar()
	nb_max_joueur = Entry(windows_heberger, textvariable=nb_max_joueur_var, width = 2)
	nb_max_joueur.place(x=260, y=102)

	problem_server = Label(windows_heberger, text="", bg="white", width=30)
	problem_server.place(x=25,y=135)

	def launch():
		global SERVER
		a = 0
		try:
			port= int(heberger_port_var.get())
		except Exception as E:
			problem_server["text"] = "Port incorrect"
			return
		try:
			nbMaxJoueur = int(nb_max_joueur_var.get())
		except Exception as E:
			problem_server["text"] = "Nb joueur incorrect"
			return
		problem_server["text"] = SERVER.create_server(port, nbMaxJoueur)
		if (problem_server["text"] == "None"):
			windows_heberger.destroy()
			SERVER.start()
		#d.join()


	launchButtonImage = PhotoImage(file="./ressources/launch.png")
	boutton_launch = Button(windows_heberger, text="", relief=FLAT, image=launchButtonImage, command=launch)
	boutton_launch.place(x=82,y=175)

	windows_heberger.mainloop()

def launch_connexion():
	windows_connexion = Toplevel()
	windows_connexion.title("Héberger")
	windows_connexion.geometry("323x217")
	windows_connexion.resizable(False, False)
	background_image_heberger = PhotoImage(file="./ressources/connection_button.png")
	background_label1 = Label(windows_connexion, image=background_image_heberger)
	background_label1.pack()

	connexion_port_var = StringVar()
	connexion_port = Entry(windows_connexion, textvariable=connexion_port_var, width=5)
	connexion_port.place(x=65, y=100)

	connexion_name_var = StringVar()
	connexion_name = Entry(windows_connexion, textvariable=connexion_name_var, width=12)
	connexion_name.place(x=200, y=100)

	connexion_ip_var = StringVar()
	connexion_ip = Entry(windows_connexion, textvariable=connexion_ip_var, width = 20)
	connexion_ip.place(x=50, y=60)

	problem_server = Label(windows_connexion, text="", bg="white", width=30)
	problem_server.place(x=25,y=135)

	def connect():
		global CLIENT
		global CHAT
		try:
			port= int(connexion_port_var.get())
		except Exception as E:
			problem_server["text"] = "Port incorrect"
			return
		try:
			ip = connexion_ip_var.get().rstrip("\n")
		except Exception as E:
			problem_server["text"] = "Ip incorrecte"
			return
		name = connexion_name_var.get().rstrip("\n")
		if len(name) == 0:
			problem_server["text"] = "Nom incorrect petit fils de putes"
			return

		problem_server["text"] = CLIENT.connect(ip, port, name)
		if (problem_server["text"] == "None"):
			windows_connexion.destroy()
			CHAT.name = name
			CHAT.start_chat()
			CLIENT.run()
		#d.join()


	connectButtonImage = PhotoImage(file="./ressources/connexion.png")
	boutton_launch = Button(windows_connexion, text="", relief=FLAT, image=connectButtonImage, command=connect)
	boutton_launch.place(x=82,y=175)

	windows_connexion.mainloop()

def launch_table_roll():

	def roll():
		return (random.randint(0, 100))

	table_roll = Toplevel()
	table_roll.title("Héberger")
	table_roll.geometry("400x654")
	table_roll.resizable(False, False)
	background_image_roll = PhotoImage(file="./ressources/feuille_roll.png")
	background_image = Label(table_roll, bg="white", image=background_image_roll)
	background_image.pack()
	arme_tranchante_var = IntVar()
	arme_tranchante = Checkbutton(table_roll, bg="white",variable=arme_tranchante_var)
	arme_tranchante.place(x=135,y=80)
	arme_contondante_var = IntVar()
	arme_contondante = Checkbutton(table_roll,bg="white", variable=arme_contondante_var)
	arme_contondante.place(x=320,y=80)
	global character
	def roll_rapide_f():
		contondant = arme_contondante_var.get()
		if (contondant == 1):
			max_resulat["text"] = character.roll_hit_contondante() - 10
		else:
			max_resulat["text"] = character.roll_hit_tranchante() - 10
		resultat_roll["text"] = roll()

	def roll_basique_f():
		contondant = arme_contondante_var.get()
		if (contondant == 1):
			max_resulat["text"] = character.roll_hit_contondante()
		else:
			max_resulat["text"] = character.roll_hit_tranchante()
		resultat_roll["text"] = roll()


	def roll_brutale_f():
		contondant = arme_contondante_var.get()
		if (contondant == 1):
			max_resulat["text"] = character.roll_hit_contondante() - 30
		else:
			max_resulat["text"] = character.roll_hit_tranchante() - 30
		resultat_roll["text"] = roll()


	def roll_cible_tete_f():
		contondant = arme_contondante_var.get()
		if (contondant == 1):
			max_resulat["text"] = character.roll_hit_contondante() + 10 -20
		else:
			max_resulat["text"] = character.roll_hit_tranchante() + 10 - 20
		resultat_roll["text"] = roll()


	def roll_cible_bras_f():
		contondant = arme_contondante_var.get()
		if (contondant == 1):
			max_resulat["text"] = character.roll_hit_contondante()
		else:
			max_resulat["text"] = character.roll_hit_tranchante()
		resultat_roll["text"] = roll()


	def roll_cible_torse_f():
		contondant = arme_contondante_var.get()
		if (contondant == 1):
			max_resulat["text"] = character.roll_hit_contondante() + 10
		else:
			max_resulat["text"] = character.roll_hit_tranchante() + 10
		resultat_roll["text"] = roll()


	def roll_cible_jambes_f():
		contondant = arme_contondante_var.get()
		if (contondant == 1):
			max_resulat["text"] = character.roll_hit_contondante() + 10 - 5
		else:
			max_resulat["text"] = character.roll_hit_tranchante() + 10 - 5
		resultat_roll["text"] = roll()

	def roll_deviation_f():
		max_resulat["text"] = character.roll_deviation()
		resultat_roll["text"] = roll()
	
	def get_object2(name, defaultValue):
		a = defaultValue
		try:
			a = int(name.get().rstrip('\n'))
		except Exception as E:
			pass
		return a

	def roll_moral_f():
		pv_perdu1 = get_object2(pv_perdu_var, 0)
		nb_ennemis1 = get_object2(nb_ennemis_var, 0)
		allies_mort1 = get_object2(allies_mort_var, 0)
		allies_vie1 = get_object2(allies_vie_var, 0)
		a = pv_perdu1 + nb_ennemis1 + (allies_mort1 * 20) - character.currentC - allies_vie1
		resultat_roll["text"] = a


	def special_roll():
		d = get_object2(special_roll_entry_dice_var, 0)
		plus = get_object2(special_roll_entry_plus_var, 0)
		i = random.randint(0, d + plus)
		resultat_roll["text"] = i

	roll_button_img = PhotoImage(file="./ressources/roll_button.png")
	roll_rapide = Button(table_roll, relief=FLAT, bg="white",image=roll_button_img, command=roll_rapide_f)
	roll_rapide.place(x=235, y=132)
	roll_basique = Button(table_roll, relief=FLAT, bg="white", image=roll_button_img, command=roll_basique_f)
	roll_basique.place(x=235, y=166)
	roll_brutale = Button(table_roll, relief=FLAT, bg="white", image=roll_button_img, command=roll_brutale_f)
	roll_brutale.place(x=235, y=195)
	roll_cible_tete = Button(table_roll, relief=FLAT, bg="white", image=roll_button_img, command=roll_cible_tete_f)
	roll_cible_tete.place(x=235, y=224)
	roll_cible_bras = Button(table_roll, relief=FLAT, bg="white", image=roll_button_img, command=roll_cible_bras_f)
	roll_cible_bras.place(x=235, y=253)
	roll_cible_torse = Button(table_roll, relief=FLAT, bg="white", image=roll_button_img, command=roll_cible_torse_f)
	roll_cible_torse.place(x=235, y=289)
	roll_cible_jambes = Button(table_roll, relief=FLAT, bg="white", image=roll_button_img, command=roll_cible_jambes_f)
	roll_cible_jambes.place(x=235, y=321)
	roll_deviation = Button(table_roll, relief=FLAT, bg="white", image=roll_button_img, command=roll_deviation_f)
	roll_deviation.place(x=235, y=369)
	roll_moral = Button(table_roll, relief=FLAT, bg="white", image=roll_button_img, command=roll_moral_f)
	roll_moral.place(x=137, y=458)

	special_roll_entry_dice_var = StringVar()
	special_roll_entry_dice = Entry(table_roll, textvariable=special_roll_entry_dice_var, width=5)
	special_roll_entry_dice.place(x=180,y=505)
	special_roll_entry_plus_var = StringVar()
	special_roll_entry_plus = Entry(table_roll, textvariable=special_roll_entry_plus_var, width=5)
	special_roll_entry_plus.place(x=235,y=505)


	pv_perdu_var = StringVar()
	pv_perdu = Entry(table_roll, textvariable=pv_perdu_var, width=2)
	pv_perdu.place(x=81,y=443)
	nb_ennemis_var = StringVar()
	nb_ennemis = Entry(table_roll, textvariable=nb_ennemis_var, width=3)
	nb_ennemis.place(x=181,y=443)
	allies_mort_var = StringVar()
	allies_mort = Entry(table_roll, textvariable=allies_mort_var, width=2)
	allies_mort.place(x=281,y=443)
	allies_vie_var = StringVar()
	allies_vie = Entry(table_roll, textvariable=allies_vie_var, width=2)
	allies_vie.place(x=365,y=443)

	special_roll  = Button(table_roll, relief=FLAT, bg="white", image=roll_button_img, command=special_roll)
	special_roll.place(x=250,y=500)

	resultat_roll = Label(table_roll, relief=FLAT, bg="white", text="28")
	resultat_roll.config(font=("Gabriola", 28))
	resultat_roll.place(x=75,y=570)

	max_resulat = Label(table_roll, relief=FLAT, bg="white", text="")
	max_resulat.config(font=("Gabriola", 28))
	max_resulat.place(x=250,y=570)
	table_roll.mainloop()


load_img = PhotoImage(file="./ressources/load.png")
boutton_load = Button(windows, text="", relief=FLAT, image=load_img, command=loadCharacter)
boutton_load.place(x=240, y=22)
save_img = PhotoImage(file="./ressources/save.png")
boutton_save = Button(windows, text="", relief=FLAT, image=save_img, command=saveCharacter)
boutton_save.place(x=302,y=22)

new_img = PhotoImage(file="./ressources/new.png")
boutton_new = Button(windows, text="", relief=FLAT, image=new_img, command=newCharacter)
boutton_new.place(x=362,y=20)

heberger_button_img = PhotoImage(file="./ressources/heberger_button.png")
heberger_button = Button(windows, text="", relief=FLAT, image=heberger_button_img, command=launch_heberger)
heberger_button.place(x=10, y=20)

connexion_button_img = PhotoImage(file="./ressources/connexion2.png")
connexion_button = Button(windows, text="", relief=FLAT, image=connexion_button_img, command=launch_connexion)
connexion_button.place(x=477, y=20)

table_roll_button_img = PhotoImage(file="./ressources/table_roll_button.png")
table_roll_button = Button(windows, text="", relief=FLAT, image=table_roll_button_img, command=launch_table_roll)
table_roll_button.place(x=1036,y=361)

windows.mainloop()
