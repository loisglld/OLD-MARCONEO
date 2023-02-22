"""
Cotisant.py

Définit la classe Cotisant.
"""

#-------------------------------------------------------------------#

from decimal import Decimal

#-------------------------------------------------------------------#

class Cotisant:
    """
    Définit les objets de type Cotisants.
    """
    
    # Valeurs initiales
    id = -1
    numero_carte = -1
    nom = "n/a"
    prenom = "n/a"
    surnom = "n/a"
    promo = "n/a"
    admin = False
    note = Decimal(0)

    def __init__(self, info_cotisant:dict):
        """
        Fait correspondre les informations de la base de données avec les attributs de l'objet.
        """
        
        self.id=info_cotisant[0]
        self.numero_carte=info_cotisant[1]
        self.nom=info_cotisant[2]
        self.prenom=info_cotisant[3]
        self.surnom=info_cotisant[4]
        self.promo=info_cotisant[5]
        self.admin=info_cotisant[6]
        self.note=info_cotisant[7]

    def __repr__(self):
        """
        Outil python qui sert à afficher sous le type str l'objet de type Cotisant et ses attributs.
        """
        return f"""{self.nom} {self.prenom}: {self.note}€"""