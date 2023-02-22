"""
MenuAchats.py

Menu dans lequel l'utilisateurs doit choisir entre:
MIDI, GOUTER, SOIREE 
"""

#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.CarteUtilisateur import *
from PACKAGES.INTERFACE.MenuBasique import *
from PACKAGES.MarcoNeo import *

from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *

#-------------------------------------------------------------------#

class MenuAchats(MenuBasique):
    def __init__(self, app: MarcoNeo):
        super().__init__(app)
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        achatsCanvas = CanvasApp(self.app.root, width=x0, height=y0)
        achatsCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Images
        self.achatIcon_img = ImageApp(self.app, "basket", SMALLBTN, SMALLBTN)
        self.repas_img = ImageApp(self.app, "dish", REPASX, ACHATSY)
        self.gouter_img = ImageApp(self.app, "gouter", GOUTERX, ACHATSY)
        self.soiree_img = ImageApp(self.app, "party", SOIREEX, ACHATSY)
        self.sortir_img = ImageApp(self.app, "exit", SMALLBTN, SMALLBTN)
        
        # Widgets
        self.labelAchat = Label(achatsCanvas, image=self.achatIcon_img.image, borderwidth=0, background="black")
        self.btnSortir = BoutonApp(achatsCanvas, self.sortir_img.image, self.sortir)
        self.btnRepas = BoutonApp(achatsCanvas, self.repas_img.image, lambda: self.changeMenu("menu-midi"))
        self.btnGouter = BoutonApp(achatsCanvas, self.gouter_img.image, lambda: self.changeMenu("menu-gouter"))
        self.btnSoiree= BoutonApp(achatsCanvas, self.soiree_img.image, lambda: self.changeMenu("menu-soirees"))
        
        # Affichage des widgets à l'écran
        self.labelAchat.place(x=x0-11*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        self.btnSortir.place(x=3*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        self.btnRepas.place(x=SMALLBTN//3+10*SMALLBTN//16+2*VERYSMALLTXT, y=y0//2-19*CHOIXY//32)
        self.btnGouter.place(x=x0//2-2*SMALLBTN//16+2*VERYSMALLTXT, y=y0//2-21*CHOIXY//32)
        self.btnSoiree.place(x=x0//2-self.soiree_img.sizeX//2, y=y0//2+7*CHOIXY//8)
        
        self.app.currentUserFrame = CarteUtilisateur(achatsCanvas, self.app.currentUser, self.app)
        
    def sortir(self):
        #self.app.log.debug("Retour sur le menu des choix.")
        from PACKAGES.INTERFACE.CHOIX.MenuChoix import MenuChoix
        self.app.setView(MenuChoix)
        
    def changeMenu(self, menu:str):
        self.app.menuParent = "achats"
        from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuConso import MenuConso
        self.app.setView(MenuConso, menu)