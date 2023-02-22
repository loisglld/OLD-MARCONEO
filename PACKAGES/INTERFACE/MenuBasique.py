"""
MenuBasique.py

Classe parent des classes pages, celles présentes sur la MARCONEO 
(exemple: MenuPrincipal, MenuValider...)
"""

#-------------------------------------------------------------------#

from tkinter import Frame

#-------------------------------------------------------------------#

class MenuBasique(Frame):
    def __init__(self, app):
        Frame.__init__(self, app.root)
        self.app = app