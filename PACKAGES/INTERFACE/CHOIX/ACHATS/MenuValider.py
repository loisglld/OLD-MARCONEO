"""
MenuValider.py

Menu de validation de la commande en cours.
"""

#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.CarteUtilisateur import CarteUtilisateur
from PACKAGES.INTERFACE.MenuBasique import MenuBasique
from PACKAGES.INTERFACE.WIDGETS.TotalFrame import TotalFrame
from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.MarcoNeo import *

#-------------------------------------------------------------------#

class MenuValider(MenuBasique):
    def __init__(self, app: MarcoNeo, total:float, parent_menu_name:str, produits=None):
        super().__init__(app)
        self.app = app
        self.app.scannerActive = False
        self.parent_menu_name = parent_menu_name # Pour un éventuel retour dynamique
        self.produits = produits
        # Il s'agit d'un rechargement donc on veut display un text cohérent avec le fait qu'on recharge
        if total<0:
            labelText = f"TOTAL: +{-total}€"
        else:
            labelText = f"TOTAL: -{total}€"
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0

        validerCanvas =  CanvasApp(self.app.root, width=x0, height=y0)
        validerCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.confirmer_img = ImageApp(self.app, "confirm", MEDIUMBTN, MEDIUMBTN)
        self.retour_img = ImageApp(self.app, "cancel", MEDIUMBTN, MEDIUMBTN)
        self.panierCommande_img = ImageApp(self.app, "commande", SEMIMEDBTN, SEMIMEDBTN)
        
        # Widgets du menu principal
        self.btnConfirmer = BoutonApp(validerCanvas, self.confirmer_img.image, lambda: self.validateOperation(total))
        self.btnRetour = BoutonApp(validerCanvas, self.retour_img.image, self.annulationCommande)
        self.labelTotal = Label(validerCanvas, text=labelText, background="black", fg="white", font=fontTextXL)
        self.labelCommande = Label(validerCanvas, image=self.panierCommande_img.image, borderwidth=0, background="black")
        
        # Affichage des widgets à l'écran
        self.btnConfirmer.place(x=x0//2-3*self.confirmer_img.sizeX//2, y=titleY+self.confirmer_img.sizeY//2)
        self.btnRetour.place(x=x0//2+self.retour_img.sizeX//2, y=titleY+self.retour_img.sizeY//2)
        self.labelCommande.place(x=x0//2-5*SMALLBTN//2-9*self.panierCommande_img.sizeX//8+SMALLBTN//4,y=2*SMALLBTN-self.panierCommande_img.sizeY//6)
        self.labelTotal.place(x=x0//2-5*SMALLBTN//2+SMALLBTN//4,y=2*SMALLBTN)

        self.app.currentUserFrame = CarteUtilisateur(self, self.app.currentUser, self.app)

        self.bind("<Destroy>", self.onDestroy)

    def validateOperation(self, total):
        # on verifie si on achete qqchose
        if total == 0:
            self.app.log.debug("Le montant de la commande est nul.")
            return

        # on verifie qu'un utilisateur a bien ete badge
        if self.app.currentUser is None:
            self.app.log.info("Personne n'est connecté. Vous ne pouvez pas consommer.")
            return

        # on verifie que le solde est suffisant
        if total > self.app.currentUser.note:
            self.app.log.info("PAIEMENT REFUSÉ: %.2f€ - %s", total, str(self.app.currentUser.prenom))
            return

        if total<0:
            self.app.log.info("RECHARGEMENT ACCEPTÉ: +%.2f€ - %s", -total, str(self.app.currentUser))
            if self.app.controller.pushOperation(self.app.currentUser, total, self.parent_menu_name):
                self.app.setCurrentUser(None)
                #self.app.log.debug(f"Ouverture de {self.parent_menu_name}.")
                from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuConso import MenuConso
                self.app.setView(MenuConso, self.parent_menu_name)
        else:
            self.app.log.info("PAIEMENT ACCEPTÉ: %.2f€ - %s", total, str(self.app.currentUser))
            # On passe le nom du produit consommé
            if self.app.controller.pushOperation(self.app.currentUser, total, self.parent_menu_name, self.produits):
                self.app.setCurrentUser(None)
                #self.app.log.debug(f"Ouverture de {self.parent_menu_name}.")
                from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuConso import MenuConso
                self.app.setView(MenuConso, self.parent_menu_name)
        
    def onDestroy(self, event):
        self.app.scannerActive = True
        
    def annulationCommande(self):
        self.app.log.info("Annulation de la commande. Retour sur le menu des choix des achats.")
        from PACKAGES.INTERFACE.CHOIX.ACHATS.MenuConso import MenuConso
        self.app.setView(MenuConso, self.parent_menu_name)
        
    def update(self, total):
        self.total = total
        if self.app.currentUser is not None and self.total > self.app.currentUser.note:
            self.labelTotal.configure(fg="red")
        else:
            self.labelTotal.configure(fg="white")
        self.labelTotal.configure(text="{:.2f} €".format(self.total))