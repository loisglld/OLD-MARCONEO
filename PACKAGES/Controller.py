# -*- coding: utf-8 -*-

"""
Controller.py

Script de connexion à la base de données MySQL des
cotisants au BDE.
"""

#-------------------------------------------------------------------#

from PACKAGES.Cotisant import *

from datetime import datetime
import mysql.connector as mysql
import os
import socket

#-------------------------------------------------------------------#

class Controller:
    """ 
    Définit les objets de type curseurs qui pointent sur la base de donnée MySQL.
    Ils pourront retourner des informations ou alors modifier des valeurs dans la BDD.
    """

    def __init__(self, app):
        """
        Connecte le programme python à la base de donnée MySQL 
        Initialise le curseur de navigation dans la base 
        de donnée mySQL.

        Args:
            app (PACKAGES.App.App): Application.
        """
        
        self.conn = None
        
        # Mots de passe et identifiants de connexion à la base de données
        self.readPwd()

        print(f"Connexion à la base de données {self.DATABASE.upper()}...")
        try:           
            self.conn = mysql.connect(host=self.HOST,
                                    database=self.DATABASE,
                                    user=self.USER,
                                    password=self.PASSWORD,
                                    port=self.PORT)
            if self.conn.is_connected():
                #print("Connecté à: ", self.conn.get_server_info())
                print("Connecté à la base de données.")

        except:
            print("Erreur lors de la connexion à la base de donnée.")
            if has_ipv6():
                print("La machine a une adresse IPv6")
            else:
                print("La machine n'a pas d'adresse IPv6")
            exit(1)

        self.app = app # Application actualisée
    
    def close(self):
        """
        Ferme la session MySQL.
        """
        
        cursor = self.conn.cursor()
        cursor.close()
        self.conn.close()
        
    def getCotisant(self, id:int):
        """
        Récupére de la base de données un utilisateur avec l'identifiant donné
        
        id - l'identifiant de l'utilisateur à rechercher
        Retourne l'utilisateur si une correspondance est trouvée, None sinon
        """
        
        # Si l'identifiant n'est pas valide alors quitter la procédure (voir la valeur initiale de id)
        if id < 0:      
            return None
        
        cursor = self.conn.cursor()
        cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")

        try:
            cursor.execute(f"""SELECT   id, 
                                        numero_carte,
                                        nom, 
                                        prenom, 
                                        surnom,
                                        promo,
                                        admin,
                                        note 
                                FROM    Cotisant 
                                WHERE   numero_carte={id}""")
            
            info_cotisant = cursor.fetchall()[0]
            return Cotisant(info_cotisant)
        
        except Exception as e:
            self.app.log.warn(f"Erreur lors de l'acquisition des détails cotisants: Erreur {e}")
            
        return None

    def pushOperation(self, currentUser:Cotisant, amount:float, parent_menu_name:str, produits=None): 
        """
        Inscrire dans la base de données une nouveau montant en euros
        pour l'utilisateur avec l'identifiant donné.
        
        Cette fonction fait deux choses: mettre à jour le solde de l'utilisateur 
        et également ajouter une nouvelle ligne dans la table d'histo

        user_id - l'identifiant de l'utilisateur
        amount - le montant en euros de l'opération
        parentMenu - str:nom du menu sur lequel revnir une fois l'operation terminée
        produits - dict: de la forme {item.nom:[item.value, item.amount], ...}
        """
        
        cursor = self.conn.cursor() # Crée un curseur sur la base de donnée
        prixRequete = 0
        if amount > 0: # ACHAT D'UN PRODUIT DANS LE MENU
            try:
                solde = currentUser.note
                # On décompose la commande en plusieurs sous-commandes et on ajoute les infos à la base de données
                for nomProduit, infosProduit in produits.items():
                    prixProduit = infosProduit[0]
                    nombreProduit = infosProduit[1]
                    
                    # Il n'y que les item commandés qui nous intéresse
                    if nombreProduit != 0:
                        prixRequete = prixProduit*nombreProduit
                        requete="INSERT INTO Commande (id,numero_carte,nom,prenom,old_note,new_note,delta,type_produit,date_histo,utilisateur_histo,amount,produit) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(requete,(currentUser.id,currentUser.numero_carte,currentUser.nom,currentUser.prenom,solde,solde-prixRequete,-prixRequete,parent_menu_name,str(datetime.now()),self.app.config["logging"]["name"],nombreProduit, nomProduit))
                        self.conn.commit() # Confirme l'actualisation des données
                    solde -= prixRequete
            except Exception as e:
                self.app.log.warn(f"Erreur lors de l'envoi de la requête à MySQL: \nErreur {e}")
                return False
            
            # Actualiser les informations du solde du cotisant qui consomme
            try:
                cursor.execute(f"UPDATE Cotisant SET note={currentUser.note-amount} WHERE id={currentUser.id};")
                self.conn.commit()
            except Exception as e:
                self.app.log.warn(f"Erreur lors de la tentative de rafraîchissement du montant sur la carte: {e}")
                return False
            return True
        
        elif amount < 0: # RECHARGEMENT DE CARTE FOUAILLE
            try:
                cursor = self.conn.cursor()
                requete="INSERT INTO Commande (numero_carte,nom,prenom,old_note,new_note,delta,date_histo,utilisateur_histo) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(requete,(currentUser.numero_carte,currentUser.nom,currentUser.prenom,currentUser.note,currentUser.note-amount,-amount,str(datetime.now()),self.app.config["logging"]["name"])) #On ne peut pas savoir qui a debloquer
                self.conn.commit()
            except Exception as e:
                self.app.log.warn(f"Erreur lors de la publication de la recharge sur les commandes: {e}")
                return False
            
            # Actualiser les informations du solde du cotisant qui consomme
            try:
                cursor.execute(f"UPDATE Cotisant SET note={currentUser.note-amount} where id={currentUser.id};")
                self.conn.commit()
            except Exception as e:
                self.app.log.warn(f"Erreur lors de la publication des modifications sur le cotisant dans la base de données: {e}")
                return False
            return True
    
    def readPwd(self):
        pwdPath = os.path.join(os.path.join(os.path.abspath(os.getcwd()), 'PACKAGES'),'pwd.txt')
        with open(pwdPath, 'r') as f:
            lines = f.readlines()
            self.HOST = lines[0].strip()
            self.DATABASE = lines[1].strip()
            self.USER = lines[2].strip()
            self.PASSWORD = lines[3].strip()
            self.PORT = int(lines[4].strip())

def has_ipv6():
    try:
        # Créer une socket pour l'IPv6
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

        # Bind la socket à une adresse IPv6 quelconque et un port aléatoire
        sock.bind(('::', 0))

        # Récupérer l'adresse IPv6 de la socket
        addr = sock.getsockname()[0]

        # Fermer la socket
        sock.close()

        # Si l'adresse IPv6 est définie, la machine a une adresse IPv6
        return bool(addr)

    except:
        # Si une exception est levée, la machine n'a pas d'adresse IPv6
        return False
