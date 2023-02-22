"""
LabelApp.py


Classe des labels présents sur l'application MARCONEO.
"""

#-------------------------------------------------------------------#

from tkinter import *
from PACKAGES.VARIABLES.VarIHM import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *

#-------------------------------------------------------------------#

class LabelApp(Canvas):
    """
    Hérite des Label Tkinter.
    Classe des Label de l'application MARCONEO.
    """
    
    # Le mode de base est le mode sombre
    mode = "Dark"
    
    def __init__(self, parent, image=None, text=None, font=None):
        """
        Initialise les label de manière à ce qu'ils
        ne se voient pas sur un fond noir/blanc.
        
        On a donc l'impression que les images png sont les écriture de l'app.
        """
        Label.__init__(self, parent)
        
        self.image = image.configImageName + LabelApp.mode
        self.text = text
        self.font = font
        self.configure(parent, image=self.image, text=self.text, borderwidth=0)