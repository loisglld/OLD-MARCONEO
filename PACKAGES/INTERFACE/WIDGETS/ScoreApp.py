"""
ScoreApp.py

Tableau contenant le score de l'utilisateur scanné.
"""


#-------------------------------------------------------------------#

from datetime import *

from PACKAGES.MarcoNeo import *
from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *

#-------------------------------------------------------------------#

class ScoreApp(Frame):
    def __init__(self, app:MarcoNeo, frameScore:Frame, parent:CanvasApp):
        Frame.__init__(self, frameScore)
        self.app = app
        self.parent = parent
        self.frameScore = frameScore
        
        self.MAXLINE = 8
        self.dateHistoLimit = datetime.now().strftime("%Y-%m-%d")
        
        shotAmount = self.requestSQL(f"SELECT SUM(amount) FROM Commande WHERE date_histo>'{self.dateHistoLimit}' and produit='shot'")
        Label(self.frameScore, text=f"Nombre de shots vendus: {shotAmount}", fg="white", bg="black", font=fontTextM).grid(row=0, column=0, sticky=W)
        metreShotAmount = self.requestSQL(f"SELECT SUM(amount) FROM Commande WHERE date_histo>'{self.dateHistoLimit}' and produit='metre-shot'")
        Label(self.frameScore, text=f"Nombre de mètre de shots vendus: {metreShotAmount}", fg="white", bg="black", font=fontTextM).grid(row=1, column=0, sticky=W)
        


    def requestSQL(self, commande:str):
        cursor = self.app.controller.conn.cursor() # Crée un curseur sur la base de donnée
        cursor.execute(commande)
        commandOutput = cursor.fetchone()[0]
        self.app.controller.conn.commit() # Confirme l'actualisation des données
        return commandOutput 
    
    def clearGrid(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()