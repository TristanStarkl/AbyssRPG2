import os
import sys
import json
import save
import random

class action():
	def __init__(self, name, cout, effet, cible, bonus, note):
		self.name = name
		self.cout = cout
		self.effet = effet
		self.cible = cible
		self.bonus = bonus
		self.note = note

	def apply(self, character):
		if (character.currentStam > self.cout):
			character.currentStam -= self.cout


class professions():
	def __init__(self, name, description, force=0, endurance=0, intelligence=0, perception=0, social=0, agilite=0, chance=0):
		self.force = force
		self.endurance = endurance
		self.intelligence = intelligence
		self.perception = perception
		self.social = social
		self.agilite = agilite
		self.chance = chance
		self.name = name
		self.description = description

	def apply(self, character):
		character.setForce(character.getForce() + self.force)
		character.setEndurance(character.getEndurance() + self.endurance)
		character.setIntelligence(character.getIntelligence() + self.intelligence)
		character.setPerception(character.getPerception() + self.perception)
		character.setSocial(character.getSocial() + self.social)
		character.setAgilite(character.getAgilite() + self.agilite)
		character.setChance(character.getChance() + self.chance)

class blessures():
	def __init__(self, name, force=0, endurance=0, intelligence=0, perception=0, social=0, agilite=0, chance=0, stam_max=0, stam_tour=0, degat=0, hit=0, pv=0):
		self.force = force
		self.endurance = endurance
		self.intelligence = intelligence
		self.perception = perception
		self.social = social
		self.agilite = agilite
		self.chance = chance
		self.name = name
		self.modStamMax = stam_max
		self.modStamTour = stam_tour
		self.degat = degat
		self.hit = hit
		self.pv = pv

	def apply(self, character):
		character.currentF = character.getCurrentForce() - self.force
		character.currentE = character.getCurrentEndurance() - self.endurance
		character.currentI = character.getCurrentIntelligence() - self.intelligence
		character.currentP = character.getCurrentPerception() - self.perception
		character.currentS = character.getCurrentSocial() - self.social
		character.currentA = character.getCurrentAgilite() - self.agilite
		character.currentC = character.getCurrentChance() - self.chance
		character.modStamTour = character.modStamTour - self.modStamTour
		character.stam_max = character.stam_max - self.modStamMax
		character.stam_tour = character.stam_tour - self.modStamTour
		character.modStamMax = character.modStamMax - self.modStamMax
		character.modDegat = self.degat
		character.modHit = self.hit

	def soigne(self, character):
		character.currentF = character.getCurrentForce() + self.force
		character.currentE = character.getCurrentEndurance() + self.endurance
		character.currentI = character.getCurrentIntelligence() + self.intelligence
		character.currentP = character.getCurrentPerception() + self.perception
		character.currentS = character.getCurrentSocial() + self.social
		character.currentA = character.getCurrentAgilite() + self.agilite
		character.currentC = character.getCurrentChance() + self.chance
		character.modStamTour = character.modStamTour + self.modStamTour
		character.modStamMax = character.modStamMax + self.modStamMax
		character.stam_max = character.stam_max + self.modStamMax
		character.stam_tour = character.stam_tour + self.modStamTour

		character.modDegat = 0
		character.modHit = 0

STAT_liste_blessure = save.loadFromFile("blessures")


class personnage():
	def __init__(self,force, endurance, intelligence, perception, social, agilite, 
		chance, pv=-1, stam_max=-1, psy=-1, mor=-1, currentMoral=-1, currentPsy=-1, 
		currentPv=-1, currentStam=-1, inventaire="", name="Jean", first_name="Dujardin", age=21,
		currentF=-1, currentE=-1, currentI=-1, currentP=-1, currentS=-1, currentA=-1, currentC=-1,
		 modHit=0, modStamMax=0, modDegat=0, modStamTour=0, bobo=[], stam_tour=-1, notes="", metier_pre_apo="",
		 metier_post_apo=""):
		self.name =name
		self.first_name = first_name
		self.age = age
		self.force = force
		self.endurance = endurance
		self.intelligence = intelligence
		self.perception = perception
		self.social = social
		self.agilite = agilite
		self.chance = chance
		self.modStamMax = modStamMax
		self.modStamTour = modStamTour
		self.notes = notes
		self.metier_post_apo = metier_post_apo
		self.metier_pre_apo = metier_pre_apo
		self.pv = pv
		if (pv == -1):
			self.pv = self.endurance * 10
		self.stam_max = stam_max
		if (stam_max == -1):
			self.stam_max = (self.endurance * 5) + (self.force * 5) + (self.agilite * 5)
		self.stam_tour = int(self.stam_max) - modStamTour

		self.psy = psy
		self.currentPsy = currentPsy
		if (self.currentPsy == -1):
			self.psy = psy
			self.currentPsy = (self.intelligence * 10) + (self.chance * 2)
		self.mor = mor
		if (mor == -1):
			self.mor = self.social * 10
		self.currentMoral = currentMoral
		if (currentMoral == -1):
			self.currentMoral = self.mor
		self.currentPsy = currentPsy
		if (currentPsy == -1):
			self.currentPsy = self.psy
		self.currentPv = currentPv
		if (currentPv == -1):
			self.currentPv = self.pv
		self.currentStam = currentStam
		if (currentStam == -1):
			self.currentStam = self.stam_max
		self.modHit = modHit
		self.modDegat = modDegat
		self.modStamMax = modStamMax
		self.inventaire = inventaire
		self.bobo = bobo

		self.currentF = currentF
		if (currentF == -1):
			self.currentF = self.force

		self.currentE = currentE
		if (currentE == -1):
			self.currentE = self.endurance

		self.currentI = currentI
		if (currentI == -1):
			self.currentI = self.intelligence

		self.currentP = currentP
		if (currentP == -1):
			self.currentP = self.perception

		self.currentS = currentS
		if (currentS == -1):
			self.currentS = self.social

		self.currentA = currentA
		if (currentA == -1):
			self.currentA = self.agilite

		self.currentC = currentC
		if (currentC == -1):
			self.currentC = self.chance

	def addBlessure(self, bobo):
		self.bobo.append(bobo.name)
		bobo.apply(self)

	def removeBlessure(self, name):
		global STAT_liste_blessure
		i = self.bobo.index(name)
		a = self.bobo.pop(i)
		for bobo in STAT_liste_blessure:
			if (bobo.name == name):
				break

		bobo.soigne(self)

	def updateSTATS(self):
		self.pv = self.endurance * 10
		self.stam_max = (self.endurance * 5) + (self.force * 5) + (self.agilite * 5)
		self.psy = (self.intelligence * 10) + (self.chance * 2)
		self.mor = self.social * 10
		global STAT_liste_blessure
		for b in self.bobo:
			for bobo in STAT_liste_blessure:
				if (bobo.name == b):
					bobo.apply(self)


	def get_list_blessures(self):
		a = []
		for bobo in self.bobo:
			a.append(bobo)			
		return (a)

	def getForce(self):
		return (self.force)

	def getEndurance(self):
		return (self.endurance)

	def getIntelligence(self):
		return (self.intelligence)

	def getPerception(self):
		return (self.perception)

	def getSocial(self):
		return (self.social)

	def getAgilite(self):
		return (self.agilite)

	def getChance(self):
		return (self.chance)

	def getCurrentForce(self):
		return (self.currentF)

	def getCurrentEndurance(self):
		return (self.currentE)

	def getCurrentIntelligence(self):
		return (self.currentI)

	def getCurrentPerception(self):
		return (self.currentP)

	def getCurrentSocial(self):
		return (self.currentS)

	def getCurrentAgilite(self):
		return (self.currentA)

	def getCurrentChance(self):
		return (self.currentC)


	def setForce(self, force):
		self.force = force

	def setEndurance(self, endurance):
		self.endurance = endurance

	def setIntelligence(self, intelligence):
		self.intelligence = intelligence

	def setPerception(self, perception):
		self.perception = perception

	def setSocial(self, social):
		self.social = social

	def setAgilite(self, agilite):
		self.agilite = agilite

	def setChance(self, chance):
		self.chance = chance

	def roll_hit_contondante(self):
		a = 7 * self.currentP + self.currentF * 5 + self.currentC * 2
		if (a > 100):
			return (100)
		return (a)

	def roll_hit_tranchante(self):
		a = 7 * self.currentP + self.currentA * 5 + self.currentC * 2
		if (a > 100):
			return (100)
		return (a)

	def roll_deviation(self):
		a = 5 * self.currentA + self.currentC * 2
		return (a)


	def roll(self, maximum=100):
		i = random.randint(0, maximum)
		return (i)

	def setStat(self, f, e, i, p, s, a, c):
		self.force = f
		self.endurance = e
		self.intelligence = i
		self.perception = p
		self.social = s
		self.agilite = a
		self.chance = c

if __name__ == "__main__":
	newUser = personnage(5,5,5,5,5,5,5)

	print("execution 1")
	save.saveToFile(newUser, "personnage")

	#professions = save.loadFromFile("professions")
	bobo = save.loadFromFile("blessures")
	#print(bobo)
	aie = bobo[0]
	newUser.addBlessure(aie)
	newUser.name = "Jean Après aie"
	newUser.get_list_blessures()
	save.saveToFile(newUser, "personnage")

	#newUser2 = save.loadFromFile("personnage")
	#print(newUser2)

