"""
CarteUtilisateur.py

Gère l'affichage de la carte identité du cotisant détecté par le lecteur RFID.
"""

#-------------------------------------------------------------------#

from tkinter import *
from PACKAGES.Cotisant import Cotisant
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *

#-------------------------------------------------------------------#

class CarteUtilisateur(Frame):
    def __init__(self, parent:CanvasApp, user: Cotisant, app:MarcoNeo):
        Frame.__init__(self, parent)
        self.parent = parent  
        self.app = app
        self.user = user
        
        self.cartonID_img = ImageApp(self.app, "IDcard", IDX, IDY)
        self.carteID_img = ImageApp(self.app, "ID", SMALLBTN, SMALLBTN)
        self.reset_img = ImageApp(self.app, "reset", VERYSMALLBTN, VERYSMALLBTN)
        
        self.labelCarton = Label(self.parent, image=self.cartonID_img.image, borderwidth=0)
        self.labelCarte = Label(self.parent, image=self.carteID_img.image, borderwidth=0, background="black")
        
        self.idLabel = Label(self.parent, text="n/a", font=fontTextM, background="black", fg="white")
        self.nameLabel = Label(self.parent, text="None", font=fontTextML, background="black", fg="white")
        self.soldeLabel = Label(self.parent, text="Solde : -", font=fontTextL, background="black", fg="gold")
        self.btnReset = BoutonApp(self.parent, self.reset_img.image, lambda:self.logOutUser(user))
        
        self.labelCarton.place(x=titleX-self.cartonID_img.sizeX//2, y=titleY-5*self.cartonID_img.sizeY//4)
        self.labelCarte.place(x=11*SMALLBTN//4, y=5*SMALLBTN//8)
        self.idLabel.place(x=13*SMALLBTN//6, y=5*SMALLBTN//8+self.carteID_img.sizeY)
        self.nameLabel.place(x=titleX-13*SMALLBTN//12, y=titleX//3-8*self.cartonID_img.sizeY//16-6*SMALLBTN//12)
        self.soldeLabel.place(x=titleX-13*SMALLBTN//12, y=2*titleY//3-2*self.cartonID_img.sizeY//16-5*SMALLBTN//12)
        self.btnReset.place(x=titleX+22*SMALLBTN//6, y=2*titleY//3-11*self.reset_img.sizeY//16)
        
        self.updateUser(user)

    def updateUser(self, user):
        self.user = user
        self.couronne_img = ImageApp(self.app, "crown", VERYSMALLBTN-10, VERYSMALLBTN-10)
        self.btnCouronne = Label(self.parent, image=self.couronne_img.image, borderwidth=0, background="black")
        
        self.displayBeautifulID()
        self.displayBeautifulName()
        
        if self.user is not None:
            self.nameLabel["text"] = str(self.nameToDisplay)
            self.idLabel["text"] = "#" + str(self.idToDisplay)
            self.soldeLabel["text"] = str(self.user.note) + " €"
            
            # Ajoute une couronne pour indiquer le statut d'admin
            if  self.user.admin != 0:
                self.btnCouronne.place(x=LARGEBTN+9*SMALLBTN//16, y=self.carteID_img.sizeY-7*SMALLBTN//16)
            else:
                try:
                    self.btnCouronne.destroy()
                except:
                    pass
        else:
            try:
                self.btnCouronne.destroy()
            except:
                pass
            
            self.idLabel["text"] = "#"
            self.nameLabel["text"] = "-"
            self.soldeLabel["text"] = "- €"
            
    def displayBeautifulID(self):
        if self.user != None:
            self.idToDisplay = str(self.user.numero_carte)
            if len(self.idToDisplay) < 10:
                N = 10 - len(self.idToDisplay)
                for i in range(N):
                    self.idToDisplay += "-"
    
    def displayBeautifulName(self):
        if self.user != None:
            if self.user.surnom != None: # S'il a un surnom
                self.nameToDisplay = str(self.user.surnom)
                if len(self.nameToDisplay) > 20:
                    self.nameLabel["font"] = fontTextM
                else:
                    self.nameLabel["font"] = fontTextML
            else: # s'il n'a pas de surnom
                self.nameLabel["font"] = fontTextML
                self.nameToDisplay = str(self.user.prenom)+" "+str(self.user.nom)
                if len(self.nameToDisplay) > 20:
                    self.nameToDisplay = self.user.prenom
                
    def logOutUser(self, user):
        """
        Cette fonction reset le système de scan des cartes fouailles.
        """
        self.app.currentUser = None
        self.app.rfidBuf = ""
        self.updateUser(user)