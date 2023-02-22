"""
MenuScore.py

Menu contenant le score des achats de l'utilisateur connecté.
"""

#-------------------------------------------------------------------#

from PACKAGES.INTERFACE.WIDGETS.ScoreApp import ScoreApp
from PACKAGES.INTERFACE.MenuBasique import *
from PACKAGES.MarcoNeo import *

from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *

from PACKAGES.VARIABLES.VarIHM import *

#from datetime import datetime

#-------------------------------------------------------------------#

class MenuScore(MenuBasique):
    def __init__(self, app: MarcoNeo):
        super().__init__(app)
        
        # Dimension de l'écran sur lequel est projeté l'interface
        x0 = self.app.x0
        y0 = self.app.y0
        
        scoreCanvas = CanvasApp(self.app.root, width=x0, height=y0)
        scoreCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Images
        self.score_img = ImageApp(self.app, "trophy", SMALLBTN, SMALLBTN)
        self.sortir_img = ImageApp(self.app, "exit", SMALLBTN, SMALLBTN)
        self.midi_img = ImageApp(self.app, "noon", SEMIMEDBTN, SEMIMEDBTN)
        self.soir_img = ImageApp(self.app, "night", SEMIMEDBTN, SEMIMEDBTN)
        
        # Widgets
        self.labelScore = Label(scoreCanvas, image=self.score_img.image, borderwidth=0, background="black")
        self.btnSortir = BoutonApp(scoreCanvas, self.sortir_img.image, self.sortir)
        self.btnMidi = BoutonApp(scoreCanvas, self.midi_img.image, self.stayOn)
        self.btnSoir = BoutonApp(scoreCanvas, self.soir_img.image, self.stayOn)
        
        # Display des widgets
        self.labelScore.place(x=x0-11*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        self.btnSortir.place(x=3*self.sortir_img.sizeX//8, y=3*self.sortir_img.sizeY//8)
        self.btnMidi.place(x=x0//3-self.midi_img.sizeX//2, y=3*self.sortir_img.sizeY//8)
        self.btnSoir.place(x=2*x0//3-self.soir_img.sizeX//2, y=3*self.sortir_img.sizeY//8)
        self.scoreFrame = Frame(scoreCanvas, background="black")
        self.scoreFrame.place(x=2*SMALLBTN//3, y=3*IDY//2)

        self.score = ScoreApp(self.app, self.scoreFrame, scoreCanvas)
        
    def stayOn(self):
        return
                
    def sortir(self):
        from PACKAGES.INTERFACE.CHOIX.MenuChoix import MenuChoix
        self.app.setView(MenuChoix)