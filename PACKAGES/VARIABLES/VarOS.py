"""
VarOS.py

Recense les variables globales du projet relatives au module os.
"""

#-------------------------------------------------------------------#

import os
from pathlib import Path

#-------------------------------------------------------------------#

def getParent(dir:str):
    path = Path(dir)
    return path.parent.absolute()

ABSOLUTE_PATH = str(getParent(getParent(os.path.dirname(os.path.abspath(__file__)))))