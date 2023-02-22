"""
HALL OF FAME MENU
"""


from tkinter import *

from PACKAGES.INTERFACE.ImgBtn import ImgBtn
from PACKAGES.INTERFACE.CurrentUserFrame import CurrentUserFrame
from PACKAGES.INTERFACE.BaseMenu import BaseMenu
from PACKAGES.Marconeo import *
from datetime import datetime, date, timedelta


class HOFMenu(BaseMenu):
    def __init__(self, app: Marconeo):
        super().__init__(app)
        self.contentRow = None
        self.date = datetime.now().replace(hour=0,
                                           minute=0, second=0, microsecond=0)

        self.grid(column=0, row=0, sticky=(N, E, S, W))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.addHeader()
        self.setContent()
        self.addActionButton()

        self.update()

    def update(self):
        self.labelPaginate.configure(
            text="{}".format(self.date.strftime("%d/%m/%Y"))
        )

    def changeDate(self, delta):
        self.date = self.date + timedelta(days=delta)
        self.update()
        self.setContent()

    def setContent(self):
        if self.contentRow is not None:
            self.contentRow.destroy()

        self.contentRow = Frame(self)
        self.contentRow.grid(column=0, row=1, sticky=(E, W, N, S))
        self.contentRow.columnconfigure(0, weight=1)
        self.contentRow.columnconfigure(1)
        self.contentRow.columnconfigure(3, weight=1)
        self.contentRow.rowconfigure(0, weight=1)
        self.contentRow.rowconfigure(4, weight=1)
        self.contentRow.rowconfigure(7, weight=1)
        self.contentRow.rowconfigure(10, weight=1)
        self.contentRow.rowconfigure(13, weight=1)

        begin = self.date.replace(
            hour=self.app.config["general"]["partyBegin"]["hour"],
            minute=self.app.config["general"]["partyBegin"]["minutes"],
            second=0)
        end = self.date.replace(
            hour=self.app.config["general"]["partyEnd"]["hour"],
            minute=self.app.config["general"]["partyEnd"]["minutes"],
            second=0)

        scoreboard = self.app.controller.getScoreboard(begin, end)

        totalCons = scoreboard["totalPayment"]
        totalRech = scoreboard["totalRefill"]
        bestClient = scoreboard["bestClient"]
        userCount = scoreboard["userCount"]
        
        if bestClient is not None:
            name = "{} {}".format(
                bestClient["prenom"], bestClient["nom"])
            total = "{:.2f} €".format(-bestClient["total"])
        else:
            name = "-"
            total = "- €"

        highScoreTitle = Label(
            self.contentRow, text="Meilleur consommateur", font=("Helvetica", 21, "bold"))
        consTitle = Label(self.contentRow,
                          text="Consommation totale", font=("Helvetica", 21, "bold"))
        rechTitle = Label(
            self.contentRow, text="Rechargement total", font=("Helvetica", 21, "bold"))

        highScorerLabel = Label(
            self.contentRow, text=name, font=("Helvetica", 21))
        highScoreLabel = Label(
            self.contentRow, text=total, font=("Helvetica", 21))
        totalConsLabel = Label(
            self.contentRow,
            text=str(totalCons) + " €",
            font=("Helvetica", 21))
        totalRechLabel = Label(
            self.contentRow, text=str(totalRech) + " €", font=("Helvetica", 21))

        userCountTitle = Label(
            self.contentRow, text="Nombre de clients différents", font=("Helvetica", 21, "bold"))
        userCountLabel = Label(
            self.contentRow, text=str(userCount), font=("Helvetica", 21))

        highScoreTitle.grid(column=1, columnspan=2, row=1)
        highScorerLabel.grid(column=1, columnspan=2, row=2)
        highScoreLabel.grid(column=1, columnspan=2, row=3)
        rechTitle.grid(column=1, row=5)
        totalRechLabel.grid(column=2, row=5)
        consTitle.grid(column=1, row=8)
        totalConsLabel.grid(column=2, row=8)
        userCountTitle.grid(column=1, row=11)
        userCountLabel.grid(column=2, row=11)

    def addActionButton(self):
        row = Frame(self)
        row.grid(column=0, row=2, sticky=(E, W, S))
        row.columnconfigure(1, weight=1)
        row.rowconfigure(0, weight=1)

        self.btnLeft = ImgBtn(row, self.app.config["icons"]["leftArrow"])
        self.btnLeft.grid(column=0, row=0, sticky=(W))
        self.btnLeft.setSize("medium")
        self.btnLeft.configure(command=lambda: self.changeDate(-1))

        self.btnRight = ImgBtn(row, self.app.config["icons"]["rightArrow"])
        self.btnRight.grid(column=2, row=0, sticky=(E))
        self.btnRight.setSize("medium")
        self.btnRight.configure(command=lambda: self.changeDate(+1))

    def addHeader(self):
        row = Frame(self)
        row.grid(column=0, row=0, sticky=(E, W, N))
        row.columnconfigure(1, weight=1)
        row.columnconfigure(2, minsize=100)

        self.btnHome = ImgBtn(row, self.app.config["icons"]["home"])
        self.btnHome.grid(column=0, row=0, sticky=(W))

        from PACKAGES.INTERFACE.MainMenu import MainMenu
        self.btnHome.configure(command=lambda: self.app.setView(
            MainMenu), width=100, height=100)

        self.labelTitle = Label(row, text="Tableau de score",
                                font=("Helvetica", 21, "bold"))
        self.labelTitle.grid(column=1, row=0)

        self.labelPaginate = Label(row, font=("TkDefaultFont", 18))
        self.labelPaginate.grid(column=2, row=0)
