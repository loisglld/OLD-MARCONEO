"""
MenuPrincipal.py

Configure la page menu principal de la MARCONEO.
"""

#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.CarteUtilisateur import *
from PACKAGES.INTERFACE.CREDITS.MenuCredits import *
from PACKAGES.INTERFACE.ETEINDRE.MenuEteindre import *
from PACKAGES.INTERFACE.PARAMETRES.MenuParametres import *
from PACKAGES.INTERFACE.CHOIX.MenuChoix import *

from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *

from PACKAGES.MarcoNeo import *

#-------------------------------------------------------------------#

class MenuPrincipal(MenuBasique):
    def __init__(self, app:MarcoNeo):
        super().__init__(app)
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        # Canvas du menu principal
        mainCanvas = CanvasApp(self.app.root, width=x0, height=y0)
        mainCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Images du menu principal
        self.marconeo_img = ImageApp(self.app, "titleDark", LARGETTL, MEDIUMTTL)
        self.quitter_img = ImageApp(self.app, "quit", SMALLBTN, SMALLBTN)
        self.info_img = ImageApp(self.app, "info", SMALLBTN, SMALLBTN)
        self.settings_img = ImageApp(self.app, "settings", SMALLBTN, SMALLBTN)
        self.appuyez_img = ImageApp(self.app, "enter", MEDIUMBTN, MEDIUMBTN)
        self.version_img = ImageApp(self.app, "version", SMALLTXT, VERYSMALLTXT)
        
        # Widgets du menu principal
        self.btnQuit = BoutonApp(mainCanvas, self.quitter_img.image, self.confirmerEteindre)
        self.btnInfo = BoutonApp(mainCanvas, self.info_img.image, self.credits)
        self.btnSettings = BoutonApp(mainCanvas, self.settings_img.image, None)
        self.labelMarconeo = Label(mainCanvas, image=self.marconeo_img.image, borderwidth=0)
        self.btnAppuyez = BoutonApp(mainCanvas, self.appuyez_img.image, self.entrerMarco)
        self.labelVersion = Label(mainCanvas, image=self.version_img.image, borderwidth=0)
        
        # Affichage des widgets à l'écran
        self.btnInfo.place(x=6*self.quitter_img.sizeX//4, y=y0-5*self.quitter_img.sizeY//4)
        self.btnSettings.place(x=self.settings_img.sizeX//4, y=y0-5*self.settings_img.sizeY//4)
        self.btnQuit.place(x=11*self.quitter_img.sizeX//4, y=y0-5*self.quitter_img.sizeY//4)
        self.labelMarconeo.place(x=titleX-self.marconeo_img.sizeX//2, y=titleY-18*self.marconeo_img.sizeY//32)
        self.btnAppuyez.place(x=x0//2-self.appuyez_img.sizeX//2,y=y0//2+3*self.appuyez_img.sizeY//16)
        self.labelVersion.place(x=x0//2+17*self.version_img.sizeX//8, y=y0-6*self.version_img.sizeY//4)
          
    def credits(self):
        #self.app.log.debug("Ouverture des Crédits.")
        self.app.setView(MenuCredits)
        
    def confirmerEteindre(self):
        #self.app.log.debug("Voulez-vous éteindre MARCONEO?")
        self.app.setView(MenuEteindre)
        
    def parametres(self):
        #self.app.log.debug("Ouverture des paramètres de MARCONEO.")
        self.app.setView(MenuParametres)
        
    def entrerMarco(self):
        #self.app.log.debug("Ouverture de MARCONEO.")
        self.app.setView(MenuChoix)