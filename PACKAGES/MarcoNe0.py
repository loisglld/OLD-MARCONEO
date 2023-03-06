"""
MarcoNeo.py

Defines MarcoNeo's app class.
MarcoNeo class encapsulates the whole logic of the application
as well as the connections to the database and the RFID reader.
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
    MarcoNeo's app class.
    MarcoNeo class encapsulates the whole logic of the application
    as well as the connections to the database and the RFID reader.
    """

    VERSION = "0.5.3"

    def __init__(self):
        """
        MarcoNeo's app class's constructor.
        """
        # Setup attributes
        self.config = None # json configuration file's content
        self.default_config = None # json configuration file's content
        self.root = None # Tkkinter window of MarcoNeo
        self.current_view = None # Active menu of MarcoNeo
        self.db = None # Base de données des cotisants
        self.controller = None # Curseur pointant sur la base de données
        self.current_user = None
        self.current_user_frame = None
        self.scanner_active = True
        self.rfid_buf = ""
        self.old_user = None
        self.menu_parent = None
        
        self.setup_marco()

    def setup_marco(self):
        """
        Connects to the database and creates the log file.
        Creates a log according to the config.json model.
        Creates a Tkinter User Interface.
        """

        self.setup_log()
        self.log.info(f"Launching MARCONEO v{MarcoNeo.VERSION}...")
        
        self.controller = Controller(self) # Se connecte à la base de données MySQL des cotisants BDE
        self.setup_config()
        self.setup_win()

    def setup_config(self):
            """
            Reads the json file (./config.json).
            Shuts down the process if an error occurs.
            
            The json file is used to configure the images and the shopping menus
            (items, prices, etc.)
            """
            
            file_object = open("config.json", "r")
            json_content = file_object.read()
            file_object.close()
            
            try:
                self.config = loads(json_content, parse_float=decimal.Decimal)
            except JSONDecodeError as decode_err:
                self.log(f"Error while parsing the config.json file at line {decode_err.lineno}")
                quit()
                
            # Stocks the default config in cas anything changes during the session, so we can reset it
            self.defaultConfig = self.config 
            
            # This part is commented out if you want the config.json to be downloaded from the ITS website
            """
            resp = requests.get("https://onlistefan.bde-tps.fr/config-marco.json")
            # contents = resp.json(parse_float=decimal.Decimal) # Stocke le contenu du config.json en arrondissant les valeurs décimales
            
            contents = resp.json(parse_float=decimal.Decimal)
            self.config=contents
            self.defaultConfig=contents
            """
                                   
    def setup_log(self):
        """
        Setup the session log file.
        
        Creates a log file named MARCONEO.log in which will be stored
        an history of the actions performed during the session.
        """
        
        log_level_switch = {"DEBUG": logging.DEBUG,
                            "INFO": logging.INFO,
                            "WARNING": logging.WARNING,
                            "ERROR": logging.ERROR,
                            "CRITICAL": logging.CRITICAL}
            
        self.log_level = log_level_switch["DEBUG"] # Configure error level to be logged
        self.log_name = "MARCONEO"
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" # Display format
        self.log_date_format = "%Y-%m-%d %I:%M:%S" # Date format
        self.log_out_path = os.path.abspath(os.path.join(os.getcwd(), "LOG")) # Absolute path to the log folder
        self.log_path = os.path.join(self.log_out_path, self.log_name + ".log")

        # Creates the log folder if it doesn't exist
        if not os.path.exists(self.log_out_path):
            os.mkdir(self.log_out_path)
            
        # Deletes the log file if it already exists
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
        
        self.log = logging.getLogger(self.log_name)
        self.log.setLevel(self.log_level)
        logging.basicConfig(filename=self.log_path, format=self.log_format,
                            datefmt=self.log_date_format, level=self.log_level, encoding='utf-8')
    
    def refreshLog(self):
        """
        Actualise day log.
        
        It copies the session log into the day log.
        """
        now = datetime.now()
        
        self.day_log_path = os.path.join(self.log_out_path, now.strftime("%d-%m-%Y.log"))
        
        # Copies each line of the session log and adds it to the day log
        with open(self.day_log_path, "a", encoding="UTF-8") as day_log, open(self.log_path, "r", encoding="UTF-8") as session_log:
            for line in session_log:
                day_log.write(line)

            # Separates the logs of each session
            day_log.write("--------------------------------------------------------------\n")
            
    def start(self):
        """
        Starts the User Interface.
        """
        self.root.mainloop()

    def quit(self):
        """
        Quits the application.
        
        Saves the session log into the day log.
        """
        
        self.root.destroy()
        
        for i in range(5):
            try:
                self.controller.close()
                break
            except:
                self.log.warn("Error while closing the database connection. Retrying...")
        else:
            self.log.error("Could not close the database connection after 5 attempts.")

        self.log.info("Closing MARCONEO...")
        print("Closing MARCONEO...")

    def setup_win(self):
        """
        Configures the main window.
        
        Gives it its properties and binds the keyboard to it.
        """
        
        self.root = Tk()
        self.root.title(f"MARCONEO v{MarcoNeo.VERSION}")
        #self.root.iconbitmap(self.config["icones"]["logo"])
        self.root.attributes('-fullscreen', True)
        #self.root.state('zoomed')
        self.root.minsize(800, 480)
        self.root.bind("<Escape>", lambda e: self.quit())
        
        # These numbers are the dimension of the screens used 
        # the MARCONEO is installed on (in the Fouaille)
        self.x0 = 800
        self.y0 = 480
        
        # Lecteur RFID (+keyboard when using MarcoNeo on laptop)
        self.root.bind("<Key>", self.keyPressed) 

    def set_view(self, View: MenuBasique, *argv, **kwargs):
        """
        Définir la vue actuelle dans la fenêtre principale.
        
        Vue - classe de la nouvelle vue actuelle à définir.
        argv et kwargs sont les arguments à passer lors de la création de la vue.
        
        /!\ NE PAS TOUCHER /!\ 
        """

        self.clearRoot()
        
        if self.current_user_frame is not None:
            self.current_user_frame.destroy()
            self.current_user_frame = None

        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = View(self, *argv, **kwargs)

    def clearRoot(self):
        """
        Efface tous les widgets de la fenêtre principale.
        """
        
        for widget in self.root.winfo_children():
            widget.destroy()

    def set_current_user(self, id:int):   
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
            self.current_user = self.controller.getCotisant(id)
        else:
            self.current_user = None

        self.log.info(f"L'actuel Utilisateur est : {self.current_user}")
        if self.current_user_frame is not None:
            self.current_user_frame.updateUser(self.current_user)

    def key_pressed(self, event=None):
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
        if not self.scanner_active:
            return

        if event.keysym == 'Return':
            #self.log.debug(f"Analyse de la carte numéro {self.rfid_buf}...")
            try:
                id = int(self.rfid_buf)
            except Exception:
                self.log.warn(f"Echec de l'analyse: {self.rfid_buf} n'est pas un numéro valide.")
            else:
                #self.log.info(f"Lecture de la carte {id}")
                self.setcurrent_user(id)
            finally:
                self.rfid_buf = ""
            
        else:
            self.rfid_buf += event.char
    
    def restartMarco(self):
        self.quit()
        self.refreshLog()
