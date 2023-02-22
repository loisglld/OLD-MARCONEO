"""
MenuEteindre.py

Configure la page de confirmation lorsque le bouton power-off
est cliqué.
"""

#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.MenuBasique import *
from PACKAGES.MarcoNeo import *

from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *

#-------------------------------------------------------------------#

class MenuEteindre(MenuBasique):
    """
    Sers de garde-fou, en cas de fausse manipulation du fouaille.
    """
    
    def __init__(self, app: MarcoNeo):
        super().__init__(app)
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        eteindreCanvas = CanvasApp(self.app.root, width=x0, height=y0)
        eteindreCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
            
        self.eteindre_img = ImageApp(self.app, "shut-down", LARGETTL, 3*MEDIUMTTL//12)
        self.confirmer_img = ImageApp(self.app, "confirm", MEDIUMBTN, MEDIUMBTN)
        self.retour_img = ImageApp(self.app, "cancel", MEDIUMBTN, MEDIUMBTN)
        
        # Widgets du menu principal
        self.labelEteindre = Label(eteindreCanvas, image=self.eteindre_img.image, borderwidth=0)
        self.btnConfirmer = BoutonApp(eteindreCanvas, self.confirmer_img.image, self.app.quit)
        self.btnRetour = BoutonApp(eteindreCanvas, self.retour_img.image, self.menuPrincipal)
        
        # Affichage des widgets à l'écran
        self.labelEteindre.place(x=titleX-self.eteindre_img.sizeX//2, y=titleY-29*self.eteindre_img.sizeY//32)
        self.btnConfirmer.place(x=x0//2-3*self.confirmer_img.sizeX//2, y=titleY+self.confirmer_img.sizeY//2)
        self.btnRetour.place(x=x0//2+self.retour_img.sizeX//2, y=titleY+self.retour_img.sizeY//2)
    
    def menuPrincipal(self):
        #self.app.log.debug("Retour sur le menu principal.")
        from PACKAGES.INTERFACE.MenuPrincipal import MenuPrincipal
        self.app.setView(MenuPrincipal)