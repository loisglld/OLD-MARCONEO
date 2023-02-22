"""
MenuParametres.py

Configure la page des paramètres de la MARCONEO.
"""
#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.MenuBasique import *
from PACKAGES.MarcoNeo import *

from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *
from PACKAGES.INTERFACE.WIDGETS.LabelApp import *

#-------------------------------------------------------------------#

class MenuParametres(MenuBasique):
    def __init__(self, app: MarcoNeo):
        super().__init__(app)
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        self.paramCanvas = CanvasApp(self.app.root, width=x0, height=y0)
        self.paramCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Images du menu principal
        self.sortir_img = ImageApp(self.app, "exit", SMALLBTN, SMALLBTN)
        self.switchOn_img = ImageApp(self.app, "switch-on", SMALLBTN, SMALLBTN)
        self.switchOff_img = ImageApp(self.app, "switch-off", SMALLBTN, SMALLBTN)
        
        # Widgets du menu principal
        self.btnSortir = BoutonApp(self.paramCanvas, self.sortir_img.image, self.menuPrincipal)
       
        # Affichage des widgets à l'écran
        self.btnSortir.place(x=x0-9*self.sortir_img.sizeX//8, y=y0-5*self.sortir_img.sizeY//4)
        self.changeStateSwitch(0)
        
    def menuPrincipal(self):
        #self.app.log.debug("Retour sur le menu principal.")
        from PACKAGES.INTERFACE.MenuPrincipal import MenuPrincpipal
        self.app.setView(MenuPrincpipal)
        
    def changeStateSwitch(self, state:bool):
        """
        Change le mode (jour/nuit)

        Args:
            state (bool): mode actuel, que l'ont va changer
        """
        
        if state: # PASSAGE EN MODE JOUR
            BoutonApp.couleur = "white"
            CanvasApp.couleur = "white"
            LabelApp.mode = "Bright"
            self.paramCanvas.config(background="white") # Actualise la page actuelle
            self.btnSortir.configure(bg=BoutonApp.couleur, activebackground=BoutonApp.couleur)
            self.btnSwitchOff = BoutonApp(self.paramCanvas, self.switchOff_img.image, lambda:self.changeStateSwitch(0))

            # Détruit le bouton à l'écran
            try:
                self.btnSwitchOn.destroy()
            except:
                pass
            # Remplace le mauvais bouton par celui du mode actuel
            self.btnSwitchOff.place(x=self.app.x0//2, y=self.app.y0//2)
        else: # PASSAGE EN MODE NUIT
            BoutonApp.couleur = "black"
            CanvasApp.couleur = "black"
            LabelApp.mode = "Dark"
            self.paramCanvas.config(background="black") # Actualise la page actuelle
            self.btnSortir.configure(bg=BoutonApp.couleur, activebackground=BoutonApp.couleur)
            self.btnSwitchOn = BoutonApp(self.paramCanvas, self.switchOn_img.image, lambda:self.changeStateSwitch(1))
            
            # Détruit le bouton à l'écran 
            try:
                self.btnSwitchOff.destroy()
            except:
                pass
            
            self.btnSwitchOn.place(x=self.app.x0//2, y=self.app.y0//2)