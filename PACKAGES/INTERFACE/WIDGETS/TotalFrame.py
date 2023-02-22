"""
TotalFrame.py

Frame dans laquelle est affiché le total de la commande en cours.
"""

#-------------------------------------------------------------------#

from PACKAGES.MarcoNeo import *
from PACKAGES.VARIABLES.VarIHM import *

#-------------------------------------------------------------------#

class TotalFrame(Frame):
    def __init__(self, app:MarcoNeo, *argv, **kwargs):
        Frame.__init__(self, *argv, **kwargs)
        self.total = 0
        self.app = app
        self.labelTotal = Label(self, font=fontTextL, background="black")
        self.labelTotal.grid(column=0, row=1)

        self.update(self.total)

    def update(self, total):
        """
        Veiller à ce que le total soit un montant que
        le cotisant connecté peut payer

        Args:
            total (float): montant à déduire du solde cotisant
        """
        self.total = total
        if self.app.currentUser is not None and self.total > self.app.currentUser.note:
            self.labelTotal.configure(fg="red")
        else:
            self.labelTotal.configure(fg="white")
        self.labelTotal.configure(text="{:.2f} €".format(self.total))
