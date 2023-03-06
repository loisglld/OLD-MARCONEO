"""
MenuRepas.py

Configure la page contenant des items à consommer.
"""

#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.CarteUtilisateur import *
from PACKAGES.INTERFACE.MenuBasique import *
from PACKAGES.MarcoNeo import *

from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *
from PACKAGES.INTERFACE.WIDGETS.ConsoApp import *
from PACKAGES.INTERFACE.WIDGETS.TotalFrame import *

from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuValider import *

#-------------------------------------------------------------------#

class MenuConso(MenuBasique):
    def __init__(self, app: MarcoNeo, menu_id:str):
        super().__init__(app)
        
        self.app = app
        self.items = []
        self.menu_id = menu_id
        self.info = self.app.config["command_menus"][menu_id]
        self.requireAdmin = self.info["require_admin"]
            
        self.numOfItem = 0
        for item in self.info["items"]:
            self.numOfItem += 1
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        consoCanvas = CanvasApp(self.app.root, width=x0, height=y0)
        consoCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.addMenuItems(consoCanvas)
        
        # Images
        self.Icon_img = ImageApp(self.app, "icon", SMALLBTN, SMALLBTN, menuKey=self.menu_id,icon=1)
        self.soiree_img = ImageApp(self.app, "disco", SMALLBTN, SMALLBTN)
        # self.clubShots_img = ImageApp(self.app, "club-shots-logo", MEDIUMBTN, MEDIUMBTN)
        self.shot_img = ImageApp(self.app, "club-shots", SMALLBTN, SMALLBTN)
        self.oeno_img = ImageApp(self.app, "club-oeno", SMALLBTN, SMALLBTN)
        self.sortir_img = ImageApp(self.app, "exit", SMALLBTN, SMALLBTN)
        self.changerPrix_img = ImageApp(self.app, "price-settings", VERYSMALLBTN, VERYSMALLBTN)
        self.poubelle_img = ImageApp(self.app, "discard", SMALLBTN, SMALLBTN)
        self.confirmer_img = ImageApp(self.app, "confirm", MEDIUMBTN, MEDIUMBTN)
        self.confirmerRouge_img = ImageApp(self.app, "confirmRed", MEDIUMBTN, MEDIUMBTN)
        self.panierCommande_img = ImageApp(self.app, "commande", SMALLBTN, SMALLBTN)
        self.settingsVert_img = ImageApp(self.app, "settings", SMALLBTN, SMALLBTN)
        self.settingsRouge_img = ImageApp(self.app, "settings-red", SMALLBTN, SMALLBTN)
        self.rechargement_img =ImageApp(self.app, "recharge-icon", SMALLBTN, SMALLBTN)
        
        # Widgets
        self.labelIcon = Label(consoCanvas, image=self.Icon_img.image, borderwidth=0, background="black")
        self.btnSoiree = BoutonApp(consoCanvas, self.soiree_img.image, lambda: self.changeMenu("menu-soirees"))
        self.clubShot = BoutonApp(consoCanvas, self.shot_img.image, lambda: self.changeMenu("menu-shots"))
        self.clubOeno = BoutonApp(consoCanvas, self.oeno_img.image, lambda: self.changeMenu("menu-oeno"))
        self.btnSortir = BoutonApp(consoCanvas, self.sortir_img.image, self.sortir)
        self.btnConfirmer = BoutonApp(consoCanvas, self.confirmer_img.image, self.validate)
        #self.btnPoubelle = BoutonApp(consoCanvas, self.poubelle_img.image, self.discard)
        self.labelCommande = Label(consoCanvas, image=self.panierCommande_img.image, borderwidth=0, background="black")
        self.totalFrame = TotalFrame(self.app, consoCanvas)
        self.btnSettings = BoutonApp(consoCanvas, self.settingsVert_img.image, lambda: self.enableModify(currentState=0))
        self.btnRecharge = BoutonApp(consoCanvas, self.rechargement_img.image, lambda: self.changeMenu("menu-recharge"))
        
        # Affichage des widgets à l'écran
        self.labelIcon.place(x=x0-11*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        
        if self.menu_id == "menu-soirees":
            self.clubShot.place(x=x0-11*self.sortir_img.sizeX//8, y=12*self.sortir_img.sizeY//8)
            self.clubOeno.place(x=x0-11*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
            
        if self.menu_id == "menu-oeno":
            self.clubShot.place(x=x0-11*self.sortir_img.sizeX//8, y=12*self.sortir_img.sizeY//8)
            self.btnSoiree.place(x=x0-11*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
            
        if self.menu_id == "menu-shots":
            self.btnSoiree.place(x=x0-11*self.sortir_img.sizeX//8, y=12*self.sortir_img.sizeY//8)
            self.clubOeno.place(x=x0-11*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
            
        # Contourne le problème de devoir rajouter un bouton moins sur le pad (car les rechargements sont négatifs)
        if self.menu_id != "menu-recharge":
            self.btnRecharge.place(x=self.poubelle_img.sizeX//4, y=y0-5*self.poubelle_img.sizeY//4)
            self.btnSettings.place(x=3*self.shot_img.sizeX//8, y=12*self.shot_img.sizeY//8)
               
        self.btnSortir.place(x=3*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        #self.btnPoubelle.place(x=self.poubelle_img.sizeX//4, y=y0-5*self.poubelle_img.sizeY//4)
        self.btnConfirmer.place(x=x0-9*self.confirmer_img.sizeX//8, y=y0-5*self.confirmer_img.sizeY//4)
        self.labelCommande.place(x=x0//2-12*self.sortir_img.sizeX//8, y=y0-5*self.sortir_img.sizeY//4)
        self.totalFrame.place(x=x0//2-3*self.sortir_img.sizeX//8, y=y0-18*self.sortir_img.sizeY//16)
        
        self.app.currentUserFrame = CarteUtilisateur(consoCanvas, self.app.current_user, self.app)
        
    def sortir(self):
        if self.app.menuParent == "achats":
            from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuAchats import MenuAchats
            self.app.setView(MenuAchats)
        elif self.app.menuParent == "choix":
            from PACKAGES.INTERFACE.CHOIX.MenuChoix import MenuChoix
            self.app.setView(MenuChoix)
        else:
            self.app.setView(MenuConso, self.app.menuParent)

    def addMenuItems(self, parent):
        self.itemFrame = Frame(parent, background="black")
        self.itemFrame.rowconfigure(0, weight=1)

        i = 0
        for item in self.info["items"]:
            self.addItem(self.itemFrame, item, i)
            i += 1
        self.itemFrame.place(x=self.app.x0//2-(self.numOfItem*(SEMIMEDBTN//2+PAD)), y=self.app.y0//2-SMALLBTN)
        
        self.itemFrame.columnconfigure(i + 1, weight=1)

    def addItem(self, parent, conf, idx):
        itemView = ConsoApp(self.app, parent, conf, idx, self.menu_id, idx)
        itemView.grid(column=idx, row=0)
        
        itemView.setListener(self.onMenuItemChange)

        self.items.append(itemView)

    def onMenuItemChange(self, item, delta):
        self.totalFrame.update(self.totalRecap()[0])

    def discard(self):
        for item in self.items:
            item.set(0)

    def validate(self):
        if self.requireAdmin:
            self.adminCheck()
        elif self.totalRecap()[0] != 0 and self.app.currentUser != None:
            self.app.setView(MenuValider, self.totalRecap()[0], self.menu_id, produits=self.totalRecap()[1])

    def totalRecap(self):
        total = decimal.Decimal(0)
        dictTotal = {item.name:[item.value] for item in self.items}
        for item in self.items:
            total += item.value * item.amount
            dictTotal[item.name].append(item.amount)
        return [total, dictTotal]

    def setCommands(self, commands):
        for item in self.items:
            if item.name in commands:
                item.fromDict(commands[item.name])

        self.totalFrame.update(self.totalRecap())

    def commandToDict(self):
        ret = {}
        for item in self.items:
            ret[item.name] = item.toDict()
        return ret
    
    def enableModify(self, currentState):
        i = 0
        if currentState:
            self.btnSettings.configure(image=self.settingsVert_img.image,command=lambda: self.enableModify(0))
            self.btnConfirmer.configure(image=self.confirmer_img.image, command=self.validate)
            for children in self.itemFrame.winfo_children():
                if not i%5:
                    children.btnRemove.configure(image=children.minus_img.image, command=children.remove)
                i+=1
        else:
            self.btnSettings.configure(image=self.settingsRouge_img.image, command=lambda: self.enableModify(1))
            self.btnConfirmer.configure(image=self.confirmerRouge_img.image, command=None)
            for children in self.itemFrame.winfo_children():
                if not i%5:
                    item = children
                    children.btnRemove.configure(image=self.changerPrix_img.image)
                    children.btnRemove.configure(command=lambda i=i: self.changerPrix(item, i//5))
                i+=1
        
    def changerPrix(self, item, index):
        from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuPrixParam import MenuPrixParam
        self.app.setView(MenuPrixParam, self.menu_id, item.add_img.image, item.value, index)
    
    def adminCheck(self):
        # Ne rentre pas sur la page adminCheck si personne 
        # ne se fait pas recharger, ni si la recharge est de 0
        if self.app.currentUser == None or self.totalRecap()[0] == 0:
            return
        
        # Si un admin est déjà connecté, il n'a pas besoin de re-badger
        if self.app.currentUser.admin != 0:
            self.app.setView(MenuValider, self.totalRecap()[0], self.menu_id)
            return
        
        from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuAdminCheck import MenuAdminCheck
        self.app.setView(MenuAdminCheck, self.totalRecap()[0])
        
    def changeMenu(self, menu:str):
        from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuConso import MenuConso
        self.app.setView(MenuConso, menu)