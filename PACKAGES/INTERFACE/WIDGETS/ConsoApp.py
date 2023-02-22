"""
ConsoApp.py

Classe des objets consommables affichés à l'écran:
ils sont constitués d'un bouton ajouter, d'un bouton
enlever, avec les icônes correspondantes.
"""

#-------------------------------------------------------------------#

from PACKAGES.MarcoNeo import *
from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *

#-------------------------------------------------------------------#

class ConsoApp(Frame):
    def __init__(self, app:MarcoNeo, parent:Frame, conf:dict, idy:str, menuKey:str, itemKey:int):
        """
        Crée une colonne d'objets: -bouton_add
                                   -amount
                                   -bouton_minus
                                   -prix individuel
        """
        Frame.__init__(self, parent)
        self.app = app
        self.parent = parent
        self.idy = idy
        self.amount = 0
        self.value = decimal.Decimal(conf["value"])
        self.name = conf["name"]
        self.listener = None

        # Met image (?) si il ne trouve pas l'icon demandée
        icon = "help"
        path = ABSOLUTE_PATH + "/IMAGES/TECH_IMAGES/" + conf["icon"]
        if "icon" in conf and os.path.exists(path):
            icon = conf["icon"]
            
        # Images
        self.add_img = ImageApp(self.app, "icon", SEMIMEDBTN, SEMIMEDBTN, menuKey, itemKey)
        self.minus_img = ImageApp(self.app, "minus", VERYSMALLBTN, VERYSMALLBTN)
        
        # Wigets
        self.btnAdd = BoutonApp(self.parent, self.add_img.image, self.add)
        self.btnRemove = BoutonApp(self.parent, self.minus_img.image, self.remove)
        self.labelAmount = Label(self.parent, font=fontTextM, background="black", fg="white")
        self.labelValue = Label(self.parent, text=str(self.value) + " €", font=fontTextM, background="black", fg="white")
         
        # Display   
        self.btnAdd.grid(column=self.idy, row=0, padx=PAD)
        self.labelAmount.grid(column=self.idy, row=1, padx=PAD)
        self.btnRemove.grid(column=self.idy, row=2, padx=PAD)
        self.labelValue.grid(column=self.idy, row=3, padx=PAD)

        self.updateText()

    def setListener(self, listener):
        self.listener = listener

    def add(self):
        self.amount += 1
        self.updateText()
        self.listener(self, 1)

    def set(self, amount):
        old = self.amount
        self.amount = 0
        self.updateText()
        self.listener(self, amount - old)

    def remove(self):
        if self.amount > 0:
            self.amount -= 1
            self.updateText()
            self.listener(self, -1)

    def updateText(self):
        self.labelAmount.configure(text=str(self.amount))

    def fromDict(self, dict):
        self.value = dict["value"]
        self.amount = dict["amount"]
        self.updateText()

    def toDict(self):
        return {
            "value": self.value,
            "amount": self.amount
        }