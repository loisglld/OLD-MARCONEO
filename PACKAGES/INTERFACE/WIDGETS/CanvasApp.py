"""
CanvasApp.py

Classe des canvas présents sur l'application MARCONEO.
"""

#-------------------------------------------------------------------#

from tkinter import *
from PACKAGES.VARIABLES.VarIHM import *

#-------------------------------------------------------------------#

class CanvasApp(Canvas):
    """
    Hérite des Canvas Tkinter.
    Classe des Canvas de l'application MARCONEO.
    """
    
    couleur = "black"
    
    def __init__(self, parent, width, height):
        """
        Initialise les canvas de manière à ce qu'ils
        ne se voient pas sur un fond noir/blanc.
        
        On a donc l'impression que les images png sont les boutons.
        """
        Canvas.__init__(self, parent)
        
        self.width = width
        self.height = height
        self.bg = CanvasApp.couleur
        
        self.configure(width=self.width, height=self.height, bg=self.bg)