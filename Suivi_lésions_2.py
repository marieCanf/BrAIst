import os
from PyQt6 import QtCore, QtGui, QtWidgets
import webbrowser
from suivi_informations_3 import Ui_suivi_fenetre
from conversation_chatgpt import Ui_Discussion_chatgpt
class HoverTableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.hover_row = -1
        self.previous_hover_row = -1  # Initialisation cruciale

        self.setStyleSheet("""
            QTableView {
                background-color: #b8ccd1;
                gridline-color: #c0c0c0;
            }
            QTableView::item {
                background: white;  # Définit la couleur de base des items
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: 1px solid #c0c0c0;
            }
        """)

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        row = self.rowAt(pos.y())

        if row != self.hover_row:
            self.previous_hover_row = self.hover_row
            self.hover_row = row
            self.update_row_style()
        super().mouseMoveEvent(event)  # Conserve le comportement par défaut

    def leaveEvent(self, event):
        self.previous_hover_row = self.hover_row
        self.hover_row = -1
        self.update_row_style()
        super().leaveEvent(event)

    def update_row_style(self):
        # Réinitialiser l'ancienne ligne
        if self.previous_hover_row >= 0 and self.previous_hover_row < self.rowCount():
            for col in range(self.columnCount()):
                if item := self.item(self.previous_hover_row, col):
                    item.setBackground(QtGui.QColor("white"))

        # Surbrillance de la nouvelle ligne
        if self.hover_row >= 0 and self.hover_row < self.rowCount():
            for col in range(self.columnCount()):
                if item := self.item(self.hover_row, col):
                    item.setBackground(QtGui.QColor("#e0f0ff"))  # Bleu clair

        self.viewport().update()  # Force le rafraîchissement

class Ui_Suivi_Lesions(object):
    def setupUi(self, Suivi_Lesions):
        Suivi_Lesions.setObjectName("Suivi_Lesions")
        Suivi_Lesions.resize(995, 678)

        # Créer un layout principal vertical
        main_layout = QtWidgets.QVBoxLayout(Suivi_Lesions)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- Barre supérieure (bouton retour + bouton info) ---
        top_bar_layout = QtWidgets.QHBoxLayout()

        self.Retour_En_Arriere_tool = QtWidgets.QToolButton()
        self.Retour_En_Arriere_tool.setArrowType(QtCore.Qt.ArrowType.LeftArrow)
        self.Retour_En_Arriere_tool.clicked.connect(Suivi_Lesions.close)
        top_bar_layout.addWidget(self.Retour_En_Arriere_tool)

        top_bar_layout.addStretch()  # Espace flexible

        self.pushButton = QtWidgets.QPushButton()
        icon = QtGui.QIcon("../../../../Downloads/info.png")
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(40, 40))
        top_bar_layout.addWidget(self.pushButton)
        self.pushButton.clicked.connect(lambda:self.ouvrir_conversation_chatgpt())

        main_layout.addLayout(top_bar_layout)

        # --- Tableau de données (prend tout l'espace restant) ---
        self.Tableau_donnees_table = HoverTableWidget()
        self.Tableau_donnees_table.setColumnCount(2)  # AJOUTÉ
        self.Tableau_donnees_table.setHorizontalHeaderLabels(["IRM déposées", "Résultats et suivi obtenu"])
        self.Tableau_donnees_table.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )

        # Configurer les en-têtes pour s'étirer
        self.Tableau_donnees_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.Tableau_donnees_table.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        main_layout.addWidget(self.Tableau_donnees_table)

        # Style (conservé de votre code original)

        Suivi_Lesions.setStyleSheet("""
                    QWidget {
                        background-color: #dceef2;
                        color: black;
                    }
                    QPushButton {
                        background-color: #8babb3;
                        border: 1px solid #050505;
                        padding: 5px;
                    }
                    QTabWidget::pane {
                        border: 1px solid #c0c0c0;
                    }
                    QPushButton:pressed {
                        background-color: #c0c0c0;
                    }
                    QProgressBar {
                        border: 2px solid grey;
                        border-radius: 5px;
                        text-align: center;
                        height: 20px;
                    }
                    
                    QProgressBar::chunk {
                        background-color: #2196F3;
                        width: 10px;
                    }
                """)

        self.retranslateUi(Suivi_Lesions)
        QtCore.QMetaObject.connectSlotsByName(Suivi_Lesions)
        self.Tableau_donnees_table.cellClicked.connect(self.cellule_cliquee)

    def ajouter_telechargement_google_drive(self,liste_liens):
        n = len(liste_liens)
        self.Tableau_donnees_table.setRowCount(n)
        for i in range(n):
            lien_url = liste_liens[i][0]
            lien = QtWidgets.QTableWidgetItem(liste_liens[i][0])
            lien.setForeground(QtGui.QColor("blue"))
            lien.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            lien.setToolTip("Cliquez pour ouvrir le lien")
            lien.setData(QtCore.Qt.ItemDataRole.UserRole, lien_url)
            self.Tableau_donnees_table.setItem(i,0,lien)
            resultats = QtWidgets.QTableWidgetItem("Obtenir les résultats")
            resultats.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.Tableau_donnees_table.setItem(i,1,resultats)
        self.Tableau_donnees_table.cellClicked.connect(self.ouvrir_lien_depuis_tableau)

    def ouvrir_lien_depuis_tableau(self, row, column):
        if column == 0:  # colonne des liens
            item = self.Tableau_donnees_table.item(row, column)
            if item:
                url = item.data(QtCore.Qt.ItemDataRole.UserRole)
                if url:
                    print(f"Ouverture du lien : {url}")
                    webbrowser.open(url)

    def cleanup_temp(self,dir_path):
        if os.path.exists(dir_path):
            for f in os.listdir(dir_path):
                os.remove(os.path.join(dir_path, f))
            os.rmdir(dir_path)
        else:
            print(f"Dossier {dir_path} non trouvé.")

    def cellule_cliquee(self, row, column):
        if column == 1:
            try:
                dialogue = QtWidgets.QDialog()
                ui_dialog = Ui_suivi_fenetre()
                ui_dialog.setupUi(dialogue)
                ui_dialog.set_patient_data(self.niss_patient)
                dialogue.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
                dialogue.setWindowTitle("Résultats de l'analyse")
                if dialogue.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                    print("Traitement réussi")
            except Exception as e:
                print(e, "Erreur de connexion avec la page des graphiques et résultats")
        self.cleanup_temp('temp_csvs')


    def retranslateUi(self, Suivi_Lesions):
            _translate = QtCore.QCoreApplication.translate
            Suivi_Lesions.setWindowTitle(_translate("Suivi_Lesions", "Form"))
            self.Retour_En_Arriere_tool.setText(_translate("Suivi_Lesions", "..."))

    def ouvrir_conversation_chatgpt(self):
        try :
            dialogue = QtWidgets.QDialog()
            dialogue.setStyleSheet("""
                        QWidget {
                            background-color: #2d2d2d;
                            color: #ffffff;
                        }
                        QPlainTextEdit {
                            background-color: #3d3d3d;
                            color: #ffffff;
                            border: 1px solid #555555;
                        }
                        QTableView {
                            background-color: #3d3d3d;
                            alternate-background-color: #454545;
                            gridline-color: #555555;
                        }
                        QTableView::item {
                            color: #ffffff;
                            border-bottom: 1px solid #555555;
                            padding: 10px;
                        }
                        QHeaderView::section {
                            background-color: #404040;
                            color: #ffffff;
                        }
                        QPushButton {
                            background-color: #505050;
                            border: 1px solid #606060;
                            padding: 5px;
                        }
                        QPushButton:hover {
                            background-color: #606060;
                        }
                    """)
            ui_dialogue = Ui_Discussion_chatgpt()
            ui_dialogue.get_data_patient(self.niss_patient)
            ui_dialogue.setupUi(dialogue)
            dialogue.setWindowTitle("Discussion avec l'API de chatgpt")
            if dialogue.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                print("Traitement réussi")
        except Exception as e:
            print(e,"Erreur de connexion avec la page de discussion avec chatgpt")

    def recuperer_niss(self, niss):
        self.niss_patient = niss


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(240, 240, 240))
    palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(0, 0, 0))
    palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(255, 255, 255))
    palette.setColor(QtGui.QPalette.ColorRole.Highlight,QtGui.QColor(0, 120, 215))  # Bleu = couleur de surbrillance du texte sélectionné
    palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(255, 255, 255))
    app.setPalette(palette)
    Suivi_Lesions = QtWidgets.QWidget()
    ui = Ui_Suivi_Lesions()
    ui.setupUi(Suivi_Lesions)
    Suivi_Lesions.showMaximized()
    sys.exit(app.exec())
