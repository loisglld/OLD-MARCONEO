"""
MenuCredits.py

Configure la page des crédits de la MARCONEO.
"""

#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.MenuBasique import *
from PACKAGES.MarcoNeo import *

from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *

#-------------------------------------------------------------------#

class MenuCredits(MenuBasique):
    def __init__(self, app: MarcoNeo):
        super().__init__(app)
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        creditsCanvas = CanvasApp(self.app.root, width=x0, height=y0)
        creditsCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Images du menu principal
        self.credits_img = ImageApp(self.app, "credits", x0-SMALLBTN, y0-SMALLBTN) # A CHANGER (utiliser du texte -> + pratique/modifiable)
        self.sortir_img = ImageApp(self.app, "exit", SMALLBTN, SMALLBTN)
        
        # Widgets du menu principal
        self.labelCredits = Label(creditsCanvas, image=self.credits_img.image, borderwidth=0)
        self.btnSortir = BoutonApp(creditsCanvas, self.sortir_img.image, self.menuPrincipal)
        
        # Affichage des widgets à l'écran
        self.labelCredits.place(x=VERYSMALLTXT, y=VERYSMALLTXT)
        self.btnSortir.place(x=x0-9*self.sortir_img.sizeX//8, y=y0-5*self.sortir_img.sizeY//4)
        
    def menuPrincipal(self):
        #self.app.log.debug("Retour sur le menu principal.")
        from PACKAGES.INTERFACE.MenuPrincipal import MenuPrincipal
        self.app.setView(MenuPrincipal)
        