"""
HistoriqueApp.py

Tableau contenant l'historique de l'utilisateur scanné.
"""


#-------------------------------------------------------------------#

from datetime import *

from PACKAGES.MarcoNeo import *
from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *

#-------------------------------------------------------------------#

class HistoriqueApp(Frame):
    def __init__(self, app:MarcoNeo, frameHisto:Frame, parent:CanvasApp):
        Frame.__init__(self, frameHisto)
        self.app = app
        self.parent = parent
        self.frameHisto = frameHisto
        
        self.MAXLINE = 6
        self.compteur = 0
        self.nomSQL, self.prenomSQL = "", ""
        self.amountCommand = self.getAmountCommand() # Récupère le nombre max de commande
        self.limit = self.MAXLINE
        
        if self.app.currentUser == None:
            self.currentCommand = f"SELECT * FROM Command ORDER BY date_histo DESC LIMIT {self.MAXLINE}"
        else:
            self.currentCommand = f"SELECT * FROM Commande WHERE prenom = '{self.nomSQL}' AND nom = '{self.prenomSQL}' ORDER BY date_histo DESC LIMIT {self.limit}"
            self.nomSQL = self.app.currentUser.nom
            self.prenomSQL = self.app.currentUser.prenom
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        # Images
        self.up_img = ImageApp(self.app, "up", SEMIMEDBTN, SEMIMEDBTN)
        self.down_img = ImageApp(self.app, "down", SEMIMEDBTN, SEMIMEDBTN)
        self.avncer_img = ImageApp(self.app, "enter", SMALLBTN, SMALLBTN)
        
        # Widgets
        self.btnUp = BoutonApp(self.parent, self.up_img.image, lambda: self.decaleHisto(1))
        self.btnDown = BoutonApp(self.parent, self.down_img.image, lambda: self.decaleHisto(0))
        self.btnAppuyez = BoutonApp(self.parent, self.avncer_img.image, lambda: self.isSomeoneDiffDetected())
        
        # Display des widgets
        self.btnUp.place(x=x0-10*self.up_img.sizeX//8, y=y0-12*self.up_img.sizeY//4)
        self.btnDown.place(x=x0-10*self.down_img.sizeX//8, y=y0-7*self.down_img.sizeY//4)
        self.btnAppuyez.place(x=3*self.avncer_img.sizeX//8, y=12*self.avncer_img.sizeY//8)
        
        self.displayHisto(self.requestSQL(0, self.MAXLINE))
            
    def decaleHisto(self, isUp:bool):
        if not isUp: # DECALE VERS LE BAS L'HISTORIQUE
            if self.compteur+self.MAXLINE>=self.amountCommand-1:
                return
            self.clearGrid(self.frameHisto)
            self.displayHisto(self.requestSQL(self.compteur+1, self.MAXLINE+self.compteur+1))
            self.compteur+=1
        else: # DECALE VERS LE HAUT L'HISTORIQUE
            if self.compteur<=0:
                return
            self.clearGrid(self.frameHisto)
            self.displayHisto(self.requestSQL(self.compteur-1, self.MAXLINE+self.compteur-1))
            self.compteur-=1
            
    def requestSQL(self, offset:int, limit:int):
        cursor = self.app.controller.conn.cursor() # Crée un curseur sur la base de donnée
        
        if self.app.currentUser == None:
            self.currentCommand = f"SELECT * FROM Commande ORDER BY date_histo DESC LIMIT {self.MAXLINE} OFFSET {offset}"
        else:
            self.currentCommand = f"SELECT * FROM Commande WHERE prenom = '{self.prenomSQL}' AND nom = '{self.nomSQL}' ORDER BY date_histo DESC LIMIT {limit} OFFSET {offset}"
        cursor.execute(self.currentCommand)
        commandsUser = cursor.fetchall()
        self.app.controller.conn.commit() # Confirme l'actualisation des données  
        return commandsUser 
      
    def displayHisto(self, commandsUser:list):
        self.amountCommand = self.getAmountCommand()
        rangeDisplay = min(self.MAXLINE, self.amountCommand)
        for i in range(rangeDisplay):
            date = commandsUser[i][9].strftime("%d/%m")
            
            produit = commandsUser[i][8]
            produitText = "rechargement" if produit==None else str(produit)
            
            delta = commandsUser[i][6]
            deltaColor = "green3" if delta>0 else "red"
            deltaText = f"+{delta}" if delta>0 else str(delta)
            
            prenomText = commandsUser[i][3].title() + " " + commandsUser[i][2].title()
            Label(self.frameHisto, text=str(date), font=fontTextM, background="black", fg="white").grid(row=i, column=1, padx=15, pady=5)
            Label(self.frameHisto, text=produitText, font=fontTextM, background="black", fg="white").grid(row=i, column=2, padx=15, pady=5)
            Label(self.frameHisto, text=deltaText, font=fontTextM, background="black", fg=deltaColor).grid(row=i, column=3, padx=30, pady=5)
            Label(self.frameHisto, text=prenomText, font=fontTextM, background="black", fg="white").grid(row=i, column=4, padx=5, pady=5)
            
    def clearGrid(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
            
    def getAmountCommand(self):
        cursor = self.app.controller.conn.cursor() # Crée un curseur sur la base de donnée
        if self.app.currentUser != None:
            requete = f"SELECT COUNT(*) FROM Commande WHERE prenom = '{self.prenomSQL}' AND nom = '{self.nomSQL}'"
        else:
            requete = f"SELECT COUNT(*) FROM Commande"
        cursor.execute(requete)
        amount = cursor.fetchone()[0]
        self.app.controller.conn.commit() # Confirme l'actualisation des données   
        return amount 
    
    def isSomeoneDiffDetected(self):
        self.compteur = 0
        if self.app.currentUser == None:
            self.currentCommand = f"SELECT * FROM Commande ORDER BY date_histo DESC LIMIT {self.MAXLINE}"
            self.clearGrid(self.frameHisto)
            self.displayHisto(self.requestSQL(0, self.MAXLINE))
        else:
            self.nomSQL = self.app.currentUser.nom
            self.prenomSQL = self.app.currentUser.prenom
            self.clearGrid(self.frameHisto)
            self.displayHisto(self.requestSQL(0, self.MAXLINE))