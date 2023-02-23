#coding: utf-8

"""
Marconeo.py

Définit la classe Marconeo.
"""

#-------------------------------------------------------------------#

from PACKAGES.Controller import *

from PACKAGES.INTERFACE.MenuBasique import *
from PACKAGES.VARIABLES.VarOS import *

from datetime import datetime
from tkinter import *
from json import *
import logging
import decimal

#-------------------------------------------------------------------#

class MarcoNeo:
    """
    Classe de l'application MARCONEO.
    
    Singleton qui encapsule toute la logique de l'application.
    """

    VERSION = "0.5.3"

    def __init__(self):
        """
        Initialise les attributs de l'objet instancié de classe App.
        
        Crée un log selon le modèle du config.json.
        Crée un interface graphique Tkinter.
        """

        self.logger = None # Journal d'activité de la MARCONEO
        self.config = None # Fichier json de configuration des données
        self.root = None # Fenêtre Tkinter associée
        self.currentView = None
        self.db = None # Base de données des cotisants
        self.controller = None # Curseur pointant sur la base de données
        self.currentUser = None
        self.currentUserFrame = None
        self.x0 = 1 # Dimensions de l'écran sur
        self.y0 = 1 # lequel est projeté l'application
        self.scannerActive = True
        self.rfidBuf = ""
        self.oldUser = None
        self.controller = Controller(self) # Se connecte à la base de données MySQL des cotisants BDE
        self.menuParent = None
        
        self.readConfig()
        self.initLog()
        self.log.info(f"Démarrage de MARCONEO v{MarcoNeo.VERSION}...")

        try:
            self.setupWin()
            self.log.info("Succès de l'ouverture de l'application.")
        except Exception as e:
            self.log.exception(f"L'application a planté lors de l'initialisation. \nErreur: {e}")

    def readConfig(self):
            """
            Lis le fichier json de configuration (./config.json)
            Eteint le processus si une erreur se produit.
            """
            
            # Télécharge le contenu du config.json depuis le site ITS dans le répertoire de travail.
            try:
                # Cette partie est à utiliser si on veut que le config.json soit téléchargé en local
                fileObject = open("config.json", "r")
                jsonContent = fileObject.read()
                self.defaultConfig = loads(jsonContent, parse_float=decimal.Decimal) # Sauvegarde les valeurs par defaut
                self.config = loads(jsonContent, parse_float=decimal.Decimal)
                
                # Cette partie en commentaire est à utiliser si on veut que le config.json soit téléchargé depuis le site ITS
                """resp = requests.get("https://onlistefan.bde-tps.fr/config-marco.json")
                # contents = resp.json(parse_float=decimal.Decimal) # Stocke le contenu du config.json en arrondissant les valeurs décimales
                
                contents = resp.json(parse_float=decimal.Decimal)
                self.config=contents
                self.defaultConfig=contents"""
                
            except JSONDecodeError as decodeErr:
                print(f"Erreur lors de l'analyse du fichier de configuration à la ligne {decodeErr.lineno} colonne {decodeErr.colno}")
                quit()
                                   
    def initLog(self):
        """
        Initialise les log de l'application.
        
        Crée un fichier MARCONEO.log dans lequel se trouvera un
        historique des actions réalisées lors de la session.
        """
        
        logLevelSwitch = {"DEBUG": logging.DEBUG,
                          "INFO": logging.INFO,
                          "WARNING": logging.WARNING,
                          "ERROR": logging.ERROR,
                          "CRITICAL": logging.CRITICAL}
        
        self.logLevel = logLevelSwitch["DEBUG"] # Configure le niveau d'alarme des messages visibles dans le log
        self.logName = "MARCONEO" # Majuscules pour que ça soit plus cool (c'est plus cool soyons francs)
        self.logFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" # Format d'affichage des info dans le log
        self.logDateFormat = "%Y-%m-%d %I:%M:%S"
        self.logOutPath = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "LOG")) # Chemin absolu vers le dossier LOG
        self.logPath = os.path.join(self.logOutPath, self.logName + ".log")

        # Création du dossier LOG s'il n'existe pas
        if not os.path.exists(self.logOutPath):
            os.mkdir(self.logOutPath)

        # Supprime latest.log et en crée un nouveau
        # (On décide de faire cette étape avant d'ouvrir le log pour ne 
        # pas avoir de conflit avec l'ouverture du fichier en .log (voir WinError 32))
        try:
            os.remove(self.logPath)
        except:
            print("MARCONEO.log existe déjà, \non le supprime et on en crée un nouveau.")
        
        self.log = logging.getLogger(self.logName)
        self.log.setLevel(self.logLevel)
        logging.basicConfig(filename=self.logPath, format=self.logFormat,
                            datefmt=self.logDateFormat, level=self.logLevel, encoding='utf-8')
    
    def refreshLog(self):
        # Actualisation du log du jour
        now = datetime.now()  # Date et heure actuelles
        
        # Définitions des chemins absolues vers les fichiers concernés
        self.logOfTheDayNamePath = os.path.join(self.logOutPath, now.strftime("%d-%m-%Y.log"))
        
        # Copie chaque ligne du log de session et les ajoute au log du jour
        with open(self.logOfTheDayNamePath, "a", encoding="UTF-8") as logOfTheDay, open(self.logPath, "r", encoding="UTF-8") as logOfSession:
            for line in logOfSession:
                logOfTheDay.write(line)

            # Séparation des logs de session dans le log du jour (plus propre)
            logOfTheDay.write("--------------------------------------------------------------\n")
            
    def start(self):
        """
        Démarre l'application et affiche la fenêtre principale.
        """
        try:
            self.root.mainloop()
        except Exception as e:
            self.log.exception(f"L'application a planté. \nErreur: {type(e).__name__}")

    def quit(self):
        """
        Quitte l'application.
        Sauvegarde le contenu du log de session dans un log du jour.
        """
        
        self.root.destroy()
        
        try:
            self.controller.close()
        except:
            self.log.warn("Problème lors de la coupure de la connexion à la base de donnée.")
        
        self.log.info("Arrêt de la MARCONEO...")
        print("Arrêt de la MARCONEO...")

    def setupWin(self):
        """
        Configure la fenêtre principale
        """
        
        self.root = Tk()
        self.root.title(f"MARCONEO v{MarcoNeo.VERSION}")
        #self.root.iconbitmap(self.config["icones"]["logo"])
        self.root.attributes('-fullscreen', True)
        #self.root.state('zoomed')
        self.root.minsize(800, 480)

        """self.x0 = self.root.winfo_screenwidth()
        self.y0 = self.root.winfo_screenheight()"""
        self.x0 = 800
        self.y0 = 480
        
        self.root.bind("<Key>", self.keyPressed) # Lecteur RFID (+clavier)

    def setView(self, View: MenuBasique, *argv, **kwargs):
        """
        Définir la vue actuelle dans la fenêtre principale.
        
        Vue - classe de la nouvelle vue actuelle à définir.
        argv et kwargs sont les arguments à passer lors de la création de la vue.
        
        /!\ NE PAS TOUCHER /!\ 
        """

        self.clearRoot()
        
        if self.currentUserFrame is not None:
            self.currentUserFrame.destroy()
            self.currentUserFrame = None

        if self.currentView is not None:
            self.currentView.destroy()

        self.currentView = View(self, *argv, **kwargs)

    def clearRoot(self):
        """
        Efface tous les widgets de la fenêtre principale.
        """
        
        for widget in self.root.winfo_children():
            widget.destroy()

    def setCurrentUser(self, id:int):   
        """
        Définir l'utilisateur actuel de l'application
        id - l'identifiant de l'utilisateur. Peut être Aucun

        Cette fonction récupérera dans la base de données l'utilisateur avec l'identifiant donné
        Si id est None ou si aucun utilisateur n'est trouvé avec l'id donné, la fonction
        ne fais rien
        Si un utilisateur correspondant est trouvé, l'application mettra à jour un User Frame
        
        /!\ NE PAS TOUCHER /!\ 
        """
        
        if id == 000:
            self.restartMarco()
            print("Arrêt forcé de la Marco.")
        
        if id is not None:
            self.currentUser = self.controller.getCotisant(id)
        else:
            self.currentUser = None

        self.log.info(f"L'actuel Utilisateur est : {self.currentUser}")
        if self.currentUserFrame is not None:
            self.currentUserFrame.updateUser(self.currentUser)

    def keyPressed(self, event=None):
        """
        Action a réaliser lorsqu'une touche est pressée.
        
        Utilisée pour gérer le lecteur RFID qui est considéré comme un clavier
        Lorsqu'une carte RFID est détectée, la RFID écrira l'identifiant de la carte
        (agissant comme un clavier), et termine avec le caractère "Return".

        CONSEIL DE DEBUG : lors de l'utilisation d'un environnement de développement avec une base de données de développement,
        le clavier peut servir de faux lecteur RFID.
        
        /!\ NE PAS TOUCHER /!\ 
        """
        
        # Sécurité de scan de la carte 
        if not self.scannerActive:
            return

        if event.keysym == 'Return':
            #self.log.debug(f"Analyse de la carte numéro {self.rfidBuf}...")
            try:
                id = int(self.rfidBuf)
            except Exception:
                self.log.warn(f"Echec de l'analyse: {self.rfidBuf} n'est pas un numéro valide.")
            else:
                #self.log.info(f"Lecture de la carte {id}")
                self.setCurrentUser(id)
            finally:
                self.rfidBuf = ""
            
        else:
            self.rfidBuf += event.char
    
    def restartMarco(self):
        self.quit()
        self.refreshLog()
