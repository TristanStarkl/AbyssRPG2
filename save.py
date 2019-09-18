import json
from os import listdir
from os.path import isfile, join, exists
import os
import glob

def convert_to_dict(obj):
	obj_dict = {
    	"__class__": obj.__class__.__name__,
    	"__module__": obj.__module__
  	}
	obj_dict.update(obj.__dict__)
	return obj_dict


def dict_to_obj(our_dict):
    if "__class__" in our_dict:
        class_name = our_dict.pop("__class__")
        module_name = our_dict.pop("__module__")
        module = __import__(module_name)
        class_ = getattr(module,class_name)
        obj = class_(**our_dict)
    else:
        obj = our_dict
    return obj

a = "contact@portail-autoentrepreneur.fr"


def saveToFile(obj, typeObject, multiplayer = False):
	if (not multiplayer):
		fileName = "./save/{}/{}.json".format(typeObject, obj.name)
		with open(fileName, "w+") as f:
			data = json.dumps(obj, default=convert_to_dict,sort_keys=True)
			f.write(data)
	else:
		fileName = "./save/personnage/multiplayer/{}.json".format(obj.name)
		with open(fileName, "w+") as f:
			data = json.dumps(obj, default=convert_to_dict,sort_keys=True)
			f.write(data)

def loadFromFile(typeObject):
	files = glob.glob("./save/{}/*.json".format(typeObject))
	if (typeObject == "personnage"):
		files_multi = glob.glob("./save/personnage/multiplayer/*.json")
	data = []
	for file in files:
		with open(file, "r") as f:
			data.append(json.loads(f.read(), object_hook=dict_to_obj))
	if (typeObject == "personnage"):
		for file in files_multi:
			with open(file, "r") as f:
				data.append(json.loads(f.read(), object_hook=dict_to_obj))

	return (data)
