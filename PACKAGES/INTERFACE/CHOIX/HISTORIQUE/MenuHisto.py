"""
MenuHisto.py

Menu contenant l'historique des achats de l'utilisateur connecté.
"""

#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.CarteUtilisateur import CarteUtilisateur
from PACKAGES.INTERFACE.WIDGETS.HistoriqueApp import HistoriqueApp
from PACKAGES.INTERFACE.MenuBasique import *
from PACKAGES.MarcoNeo import *

from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *

from PACKAGES.VARIABLES.VarIHM import *

#from datetime import datetime

#-------------------------------------------------------------------#

class MenuHisto(MenuBasique):
    def __init__(self, app: MarcoNeo):
        super().__init__(app)
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        histoCanvas = CanvasApp(self.app.root, width=x0, height=y0)
        histoCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Images
        self.histo_img = ImageApp(self.app, "histo", SMALLBTN, SMALLBTN)
        self.sortir_img = ImageApp(self.app, "exit", SMALLBTN, SMALLBTN)
        
        # Widgets
        self.labelHisto = Label(histoCanvas, image=self.histo_img.image, borderwidth=0, background="black")
        self.btnSortir = BoutonApp(histoCanvas, self.sortir_img.image, self.sortir)
        
        # Display des widgets
        self.labelHisto.place(x=x0-11*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        self.btnSortir.place(x=3*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        self.histoFrame = Frame(histoCanvas, background="black")
        self.histoFrame.place(x=2*SMALLBTN//3, y=3*IDY//2)
        
        self.historique = HistoriqueApp(self.app, self.histoFrame, histoCanvas)
        self.app.currentUserFrame = CarteUtilisateur(histoCanvas, self.app.currentUser, self.app)
        
    def sortir(self):
        from PACKAGES.INTERFACE.CHOIX.MenuChoix import MenuChoix
        self.app.setView(MenuChoix)