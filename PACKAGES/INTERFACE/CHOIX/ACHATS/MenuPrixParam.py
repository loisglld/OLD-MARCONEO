"""
MenuPrixParam.py

Menu pour paramétrer les prix de l'item choisi.
"""

#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.CarteUtilisateur import *
from PACKAGES.INTERFACE.MenuBasique import *
from PACKAGES.MarcoNeo import *

from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *
from PACKAGES.INTERFACE.WIDGETS.ConsoApp import *
from PACKAGES.INTERFACE.WIDGETS.PadApp import *

#-------------------------------------------------------------------#

class MenuPrixParam(MenuBasique):
    def __init__(self, app: MarcoNeo, menu_id:str, item_img, item_value, index_item):
        super().__init__(app)
        self.menu_id = menu_id
        self.icon = item_img
        self.oldValue = item_value
        self.index = index_item
        self.defaultValue = self.app.defaultConfig["command_menus"][self.menu_id]["items"][self.index]["value"]
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        prixParamCanvas = CanvasApp(self.app.root, width=x0, height=y0)
        prixParamCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Images
        self.Icon_img = ImageApp(self.app, "price-settings", SMALLBTN, SMALLBTN)
        self.sortir_img = ImageApp(self.app, "exit", SMALLBTN, SMALLBTN)
        self.defaut_img = ImageApp(self.app, "default", MEDIUMBTN, MEDIUMBTN)
        
        # Widgets
        self.labelIcon = Label(prixParamCanvas, image=self.Icon_img.image, borderwidth=0, background="black")
        self.btnSortir = BoutonApp(prixParamCanvas, self.sortir_img.image, lambda: self.changeMenu(self.menu_id))
        self.btnDefaut = BoutonApp(prixParamCanvas, self.defaut_img.image, self.setToDefaultValue)
        self.labelDefaut = Label(prixParamCanvas, text=f"VALEUR PAR DÉFAUT:\n{self.defaultValue}", fg="PaleGreen2", background="black", font=fontTextM, borderwidth=0)
        
        # Affichage des widgets à l'écran
        self.labelIcon.place(x=x0-11*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        self.btnSortir.place(x=3*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        self.btnDefaut.place(x=3*x0//4, y=y0//2-self.defaut_img.sizeY//2)
        self.labelDefaut.place(x=3*x0//4-self.defaut_img.sizeX//3, y=y0//2+self.defaut_img.sizeY//2)
        
        self.padFrame = Frame(prixParamCanvas, background="black")
        self.padFrame.place(x=x0//2-3*SEMIMEDBTN//2, y=y0//2-3*SEMIMEDBTN//2)
        PadApp(self.app, self.padFrame, prixParamCanvas, self.menu_id, self.index)
        
    def setToDefaultValue(self):
        self.app.config["command_menus"][self.menu_id]["items"][self.index]["value"] = self.defaultValue
        
    def changeMenu(self, menu:str):
        from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuConso import MenuConso
        self.app.setView(MenuConso, menu)