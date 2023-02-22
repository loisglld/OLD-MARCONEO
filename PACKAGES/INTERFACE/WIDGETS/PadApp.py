"""
PadApp.py

Pad numérique pour saisir les nouveaux prix lors de la modification des prix.
"""

#-------------------------------------------------------------------#

from PACKAGES.MarcoNeo import *
from PACKAGES.INTERFACE.WIDGETS.BoutonApp import *
from PACKAGES.INTERFACE.WIDGETS.ImageApp import *
from PACKAGES.INTERFACE.WIDGETS.CanvasApp import *

#-------------------------------------------------------------------#

class PadApp(Frame):
    def __init__(self, app:MarcoNeo, framePad:Frame, parent:CanvasApp, menu_id:str, item_index):
        Frame.__init__(self, framePad)
        self.app = app
        self.framePad = framePad
        self.parent = parent
        self.menu_id = menu_id
        self.index = item_index
        self.newValue = None
        self.padEntry = Entry(self.parent,
                             insertbackground="white", # petite barre qui clignote lorsque le focus est dans l'entrybox
                             background='black',
                             border=10,
                             width=10,
                             font=fontTextL,
                             fg='white')
        
        # Images
        self.N0_img = ImageApp(self.app, "N0", SEMIMEDBTN, SEMIMEDBTN)
        self.N1_img = ImageApp(self.app, "N1", SEMIMEDBTN, SEMIMEDBTN)
        self.N2_img = ImageApp(self.app, "N2", SEMIMEDBTN, SEMIMEDBTN)
        self.N3_img = ImageApp(self.app, "N3", SEMIMEDBTN, SEMIMEDBTN)
        self.N4_img = ImageApp(self.app, "N4", SEMIMEDBTN, SEMIMEDBTN)
        self.N5_img = ImageApp(self.app, "N5", SEMIMEDBTN, SEMIMEDBTN)
        self.N6_img = ImageApp(self.app, "N6", SEMIMEDBTN, SEMIMEDBTN)
        self.N7_img = ImageApp(self.app, "N7", SEMIMEDBTN, SEMIMEDBTN)
        self.N8_img = ImageApp(self.app, "N8", SEMIMEDBTN, SEMIMEDBTN)
        self.N9_img = ImageApp(self.app, "N9", SEMIMEDBTN, SEMIMEDBTN)
        self.virgule_img = ImageApp(self.app, "coma", SEMIMEDBTN, SEMIMEDBTN)
        self.effacer_img = ImageApp(self.app, "discard", SEMIMEDBTN, SEMIMEDBTN)
        self.Nentrer_img = ImageApp(self.app, "enter-price", SEMIMEDBTN, SEMIMEDBTN)
        
        # Widgets
        self.btn0 = BoutonApp(self.framePad, self.N0_img.image, lambda: self.button_click(0))
        self.btn1 = BoutonApp(self.framePad, self.N1_img.image, lambda: self.button_click(1))
        self.btn2 = BoutonApp(self.framePad, self.N2_img.image, lambda: self.button_click(2))
        self.btn3 = BoutonApp(self.framePad, self.N3_img.image, lambda: self.button_click(3))
        self.btn4 = BoutonApp(self.framePad, self.N4_img.image, lambda: self.button_click(4))
        self.btn5 = BoutonApp(self.framePad, self.N5_img.image, lambda: self.button_click(5))
        self.btn6 = BoutonApp(self.framePad, self.N6_img.image, lambda: self.button_click(6))
        self.btn7 = BoutonApp(self.framePad, self.N7_img.image, lambda: self.button_click(7))
        self.btn8 = BoutonApp(self.framePad, self.N8_img.image, lambda: self.button_click(8))
        self.btn9 = BoutonApp(self.framePad, self.N9_img.image, lambda: self.button_click(9))
        self.btnVirgule = BoutonApp(self.framePad, self.virgule_img.image, lambda: self.button_click("."))
        self.btnEntrerPrix = BoutonApp(self.framePad, self.Nentrer_img.image, lambda: self.getNewValue(self.padEntry))
        self.btnEffacerPrix = BoutonApp(parent, self.effacer_img.image, lambda: self.button_clear(self.padEntry))
        self.labelDone = Label(parent, text="", fg="PaleGreen2", background="black", font=fontTextM, borderwidth=0)
        
        # Affichage des widgets à l'écran
        self.btn7.grid(row=1, column=0)
        self.btn8.grid(row=1, column=1)
        self.btn9.grid(row=1, column=2)
        
        self.btn4.grid(row=2, column=0)
        self.btn5.grid(row=2, column=1)
        self.btn6.grid(row=2, column=2)
        
        self.btn1.grid(row=3, column=0)
        self.btn2.grid(row=3, column=1)
        self.btn3.grid(row=3, column=2)
        
        self.btnVirgule.grid(row=4, column=0)
        self.btn0.grid(row=4, column=1)
        self.btnEntrerPrix.grid(row=4, column=2)
        
        self.padEntry.place(x=self.app.x0//2-22*SMALLBTN//12, y=SMALLBTN//2)
        self.labelDone.place(x=self.app.x0//4-5*SEMIMEDBTN//3, y=self.app.y0//2+SEMIMEDBTN//2)
        self.btnEffacerPrix.place(x=self.effacer_img.sizeX//4, y=self.app.y0-5*self.effacer_img.sizeY//4)
        
    def button_click(self, number):
        current = self.padEntry.get()
        self.padEntry.delete(0, END)
        self.padEntry.insert(0, str(current) + str(number))
        
    def button_clear(self, entry):
        entry.delete(0, END)
        
    def getNewValue(self, entry):
        self.app.config["command_menus"][self.menu_id]["items"][self.index]["value"] = self.padEntry.get()
        self.newValue = self.padEntry.get()
        self.labelDone.configure(text=f"MODIFICATION\nEFFECTUÉE.")
        self.app.log.warn(f"Le prix de l'item {self.index} de {self.menu_id} a été modifié. Nouveau prix: {self.newValue}.")
        entry.delete(0, END)