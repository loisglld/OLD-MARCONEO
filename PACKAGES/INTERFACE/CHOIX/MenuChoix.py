"""
MenuChoix.py

Menu dans lequel l'utilisateurs doit choisir entre:
RECHARGER, ACHATS, SCORES, HISTORIQUE   
"""

#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.CarteUtilisateur import *
from PACKAGES.INTERFACE.MenuBasique import *
from PACKAGES.MarcoNeo import *

from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *

#-------------------------------------------------------------------#

class MenuChoix(MenuBasique):
    def __init__(self, app: MarcoNeo):
        super().__init__(app)
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        choixCanvas = CanvasApp(self.app.root, width=x0, height=y0)
        choixCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Images du menu principal
        self.achats_img = ImageApp(self.app, "shop", ACHATSX, CHOIXY)
        self.rechargement_img = ImageApp(self.app, "recharge", RECHX, CHOIXY)
        self.histo_img = ImageApp(self.app, "history", HISTOX, CHOIXY)
        self.score_img = ImageApp(self.app, "score", SCOREX, CHOIXY)
        self.sortir_img = ImageApp(self.app, "exit", SMALLBTN, SMALLBTN)
        
        # Widgets du menu principal
        self.btnSortir = BoutonApp(choixCanvas, self.sortir_img.image, self.sortir)
        self.btnAchats = BoutonApp(choixCanvas, self.achats_img.image, self.menuAchats)
        self.btnRechargement = BoutonApp(choixCanvas, self.rechargement_img.image, self.menuRecharge)
        self.btnHisto= BoutonApp(choixCanvas, self.histo_img.image, self.menuHisto)
        self.btnScore = BoutonApp(choixCanvas, self.score_img.image, self.menuScore)
        
        # Affichage des widgets à l'écran
        self.btnSortir.place(x=3*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        self.btnAchats.place(x=SMALLBTN//3+5*SMALLBTN//16, y=y0//2-10*CHOIXY//16)
        self.btnRechargement.place(x=x0//2-2*SMALLBTN//16, y=y0//2-25*CHOIXY//32)
        self.btnHisto.place(x=x0//2, y=y0//2+7*CHOIXY//8)
        self.btnScore.place(x=6*SMALLBTN//16+10*CHOIXY//24, y=y0//2+19*CHOIXY//24)
        
        self.app.currentUserFrame = CarteUtilisateur(choixCanvas, self.app.current_user, self.app)
        
    def sortir(self):
        #self.app.log.debug("Retour sur le menu principal.")
        from PACKAGES.INTERFACE.MenuPrincipal import MenuPrincipal
        self.app.setView(MenuPrincipal)
    
    def menuAchats(self):
        #self.app.log.debug("Ouverture du menu des achats.")
        from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuAchats import MenuAchats
        self.app.setView(MenuAchats)
        
    def menuRecharge(self):
        self.app.menuParent = "choix"
        from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuConso import MenuConso
        self.app.setView(MenuConso, "menu-recharge")
    
    def menuHisto(self):
        self.app.menuParent = "choix"
        from PACKAGES.INTERFACE.CHOIX.HISTORIQUE.MenuHisto import MenuHisto
        self.app.setView(MenuHisto)
        
    def menuScore(self):
        self.app.menuParent = "choix"
        from PACKAGES.INTERFACE.CHOIX.SCORES.MenuScore import MenuScore
        self.app.setView(MenuScore)