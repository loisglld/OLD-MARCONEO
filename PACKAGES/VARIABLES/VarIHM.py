"""
VarIHM.py

Recense les variables relatives à l'interface humain-machine.
"""
#-------------------------------------------------------------------#

from PACKAGES.VARIABLES.VarOS import *

#-------------------------------------------------------------------#
"""
Importation des polices d'écriture.
"""

# pyglet.font.add_file(ABSOLUTE_PATH + "/PACKAGES/INTERFACE/FONTS/MAKISUPA.TTF")
# pyglet.font.add_file(ABSOLUTE_PATH + "/PACKAGES/INTERFACE/FONTS/Batrider-Textured.ttf")

fontTitle = ("Batrider-Textured", 200)
fontTextS = "MAKISUPA 5 bold"
fontTextM = "MAKISUPA 15 bold"
fontTextML =  "MAKISUPA 20 bold"
fontTextL = "MAKISUPA 25 bold"
fontTextXL = "MAKISUPA 40 bold"

#-------------------------------------------------------------------#
"""
Coefficient multiplicateur de passage entre écran 1920x1080 à 800x480.
"""

coeffX = 800/1920
coeffY = 480/1080

#-------------------------------------------------------------------#
"""
Taille des boutons.
"""
VERYSMALLBTN = round(150*coeffX)-10
SMALLBTN = round(150*coeffX)
SEMIMEDBTN = round(210*coeffX) 
MEDIUMBTN = round(300*coeffX)
LARGEBTN = round(600*coeffX)

ESP = round(25*coeffX) 
PAD = 10

#-------------------------------------------------------------------#
"""
Taille pour les titres.
"""

titleX = round((1920//2)*coeffX)
titleY = round((6*1080//16)*coeffY)

SMALLTTL = round(350*coeffX)
MEDIUMTTL = round(600*coeffX)
LARGETTL = round(1500*coeffX)

PETITTITRE = round(300*coeffX)
MOYENTITRE = round(730*coeffX)

#-------------------------------------------------------------------#
"""
Taille pour les titres.
"""

VERYSMALLTXT = round(50*coeffX)
SMALLTXT = round(300*coeffX)
MEDIUMTXT = round(625*coeffX)
LARGETXT = round(1000*coeffX)

#-------------------------------------------------------------------#
"""
Taille pour les boutons de choix.
"""

CHOIXY = round(230*coeffX)
ACHATSY = round(250*coeffX)

ACHATSX = round(680*coeffY)
HISTOX = round(830*coeffY)
SCOREX = round(635*coeffY)
RECHX = round(850*coeffX)
REPASX = round(620*coeffX)
GOUTERX = round(680*coeffX)
SOIREEX = round(680*coeffX)

#-------------------------------------------------------------------#
"""
Taille pour le carton d'identité.
"""

IDX = round(1400*coeffX)
IDY = round(300*coeffX)