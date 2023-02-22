"""
MenuAdminCheck.py

Configure la page de confirmation des droits amdin.
"""

#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.CarteUtilisateur import *
from PACKAGES.INTERFACE.MenuBasique import *
from PACKAGES.MarcoNeo import *

from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *

#-------------------------------------------------------------------#

class MenuAdminCheck(MenuBasique):
    def __init__(self, app: MarcoNeo, total):
        super().__init__(app)
        self.app = app
        self.total = total
        self.oldUser = self.app.currentUser
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        adminCanvas = CanvasApp(self.app.root, width=x0, height=y0)
        adminCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Images du menu principal
        self.Icon_img = ImageApp(self.app, "recharge-icon", SMALLBTN, SMALLBTN)
        self.admin_img = ImageApp(self.app, "admin?", 7*LARGETTL//6, 3*MEDIUMTTL//12)
        self.avncer_img = ImageApp(self.app, "enter", MEDIUMBTN, MEDIUMBTN)
        self.sortir_img = ImageApp(self.app, "exit", SMALLBTN, SMALLBTN)
        
        # Widgets du menu principal
        self.labelIcon = Label(adminCanvas, image=self.Icon_img.image, borderwidth=0, background="black")
        self.labelAdmin = Label(adminCanvas, image=self.admin_img.image, borderwidth=0)
        self.btnSortir = BoutonApp(adminCanvas, self.sortir_img.image, self.retour)
        self.btnAppuyez = BoutonApp(adminCanvas, self.avncer_img.image, self.isAmdinDetected)
        
        # Affichage des widgets à l'écran
        self.labelIcon.place(x=x0-11*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        self.labelAdmin.place(x=titleX-self.admin_img.sizeX//2, y=titleY)
        self.btnSortir.place(x=3*self.Icon_img.sizeX//8, y=3*self.Icon_img.sizeY//8)
        self.btnAppuyez.place(x=x0//2-self.avncer_img.sizeX//2,y=y0//2+3*self.avncer_img.sizeY//16)
        
        self.app.currentUserFrame = CarteUtilisateur(adminCanvas, self.app.currentUser, self.app)
        
    def isAmdinDetected(self, event=None):
        if self.app.currentUser.admin != 0:
            self.app.currentUser = self.oldUser
            from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuValider import MenuValider
            self.app.setView(MenuValider, self.total, "menu-recharge")
        else:
            self.app.log.warn(f"Tentative de rechargment sans les droits administrateurs par {self.app.currentUser.nom} {self.app.currentUser.prenom} - ID: {self.app.currentUser.numero_carte}")
            
    def retour(self):
        from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuConso import MenuConso
        self.app.setView(MenuConso, "menu-recharge")