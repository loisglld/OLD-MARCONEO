"""
ImageApp.py

Classe ImageApp, objets contenant les images du projet.
"""

#-------------------------------------------------------------------#

from PACKAGES.VARIABLES.VarOS import *
from PACKAGES.VARIABLES.VarIHM import *

from PACKAGES.MarcoNeo import *

from PIL import Image as imgpil
from PIL import ImageTk

import logging
# Modifie le niveau de sévérité des logMessages de PIL pour enlever une pollution du log
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)

#-------------------------------------------------------------------#

class ImageApp:
    """
    Classe des images présentes sur l'interface de l'application MARCONEO.
    """
    
    def __init__(self, app:MarcoNeo, configImageName:str, sizeX:float, sizeY:float, menuKey="", itemKey=0, icon=0):
        """
        Définitions des images.
        """
        
        self.sizeX = sizeX
        self.sizeY = sizeY
        
        if menuKey == "": # Images dans le gros tas du json
            self.image = self.resize_image(app.config["icones"][configImageName], self.sizeX, self.sizeY)
        elif icon: # Icone dans l'attribut "icon" des menus du json
            self.image = self.resize_image(app.config["command_menus"][menuKey]["icon"], self.sizeX, self.sizeY)
        else: # Icones des items dans les menus du json
            self.image = self.resize_image(app.config["command_menus"][menuKey]["items"][itemKey]["icon"], self.sizeX, self.sizeY)
         
    
    def resize_image(self, image:str, x:int, y:int, dir=ABSOLUTE_PATH):
        """
        Redimmensionne l'image aux dimensions souhaitées.

        Args:
            image (str): nom de l'image dans le fichier contenant les images.
            x (int): dimension selon abscisse.
            y (int): dimension selon l'ordonnée.
            dir (str): direction dans l'arborescence des images.
            extension (str, optional): extension de l'image. Defaults to 'png'.

        Returns:
            PIL.ImageTk.PhotoImage: image redimensionnée.
        """
        image0 = imgpil.open(f"{dir}/IMAGES/{image}")
        image_resized = image0.resize((x,y), imgpil.ANTIALIAS)
        return ImageTk.PhotoImage(image_resized)