"""
BoutonApp.py

Classe des boutons présents sur l'application MARCONEO.
"""

#-------------------------------------------------------------------#

from tkinter import *
from PACKAGES.VARIABLES.VarIHM import *

#-------------------------------------------------------------------#

class BoutonApp(Button):
    """
    Hérite des boutons Tkinter.
    Classe des boutons de l'application MARCONEO.
    """
    
    couleur = "black"
    
    def __init__(self, parent, img, commande):
        """
        Initialise les boutons de manière à ce qu'ils ne se voient pas sur un fond noir.
        On a donc l'impression que les images png sont les boutons.
        """
        Button.__init__(self, parent)
        
        self.img = img
        self.commande = commande
        
        # bg = background inactif (bouton non-pressé)
        # activebackground = background actif (bouton pressé)
        self.configure(image=self.img, bg=self.couleur,
                       activebackground=self.couleur, borderwidth=0,
                       command=self.commande, border=0, highlightcolor="black",
                       highlightbackground="black", highlightthickness=0)

    def modeClairBouton(self):
        self.configure(bg="white",
                       activebackground="white")
        
    def modeSombreBouton(self):
        self.configure(bg="black",
                       activebackground="black")