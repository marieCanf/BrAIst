import os
import mysql.connector
from PyQt6.QtWidgets import QMessageBox
from fenêtre_irm_patients_save_2 import Ui_Inserer_IRM_informations
from Suivi_lésions_2 import Ui_Suivi_Lesions
from Ajout_patient import Ui_Ajout_patient
from database import get_connection
from Ajout_fichier import ajouter_dossier, upload_dossier
from Modèles_IA import Code_Segmentation_Masques, Code_Segmentation_Masques_2, Pyradiomics, MLP



#%% Classe Worker :
from PyQt6.QtCore import QThread, pyqtSignal


class UploadWorker(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(int) #int pour émettre l'Id_irm
    error_occurred = pyqtSignal(str)

    def __init__(self, dossier, patient_info,inami):
        super().__init__()
        self.dossier = dossier
        self.patient_info = patient_info
        self.inami = inami

    def run(self):
        try:
            from Ajout_fichier import zip_dossier, upload_dossier
            total_files = sum([len(files) for _, _, files in os.walk(self.dossier)])
            # Étape 1: Création du ZIP avec progression
            def zip_progress(progress):
                self.progress_updated.emit(int(progress * 0.5))  # 50% pour le ZIP

            nom_archive = zip_dossier(
                self.dossier,
                self._generate_zip_name(),
                progress_callback=zip_progress
            )

            # Étape 2: Upload avec progression simulée
            for progress in range(50, 101):
                self.progress_updated.emit(progress)
                self.msleep(50)  # Simule la progression de l'upload
            url = upload_dossier(
                self.patient_info.get("nom", "Patient"),
                self.patient_info.get("prenom", "Inconnu"),
                nom_archive
            )

            niss_patient = self.patient_info.get("niss", "")
            id_irm = self.save_to_db(url,niss_patient,self.inami)
            self.finished.emit(id_irm)


        except Exception as e:
            self.error_occurred.emit(str(e))

    def _generate_zip_name(self):
        from datetime import datetime
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.patient_info.get('nom', 'Patient')}_{self.patient_info.get('prenom', 'Inconnu')}_{date_str}.zip"
    def save_to_db(self, url, niss, inami):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO IRM (Lien_irm, NISS, INAMI) VALUES (%s, %s, %s)",
                (url, niss, inami)
            )
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_irm = cursor.fetchone()[0]
            conn.commit()
            return id_irm
        except Exception as e:
            print(f"Erreur DB : {str(e)}")
            raise
        finally:
            cursor.close()
            conn.close()

#%%  ====INTERFACE====

from PyQt6 import QtCore, QtGui, QtWidgets


#Permettre le surlignage de la ligne du tableau quand je passe dessus avec la souris
class HoverTableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.hover_row = -1
        self.previous_hover_row = -1  # Initialisation cruciale
        self.setStyleSheet("""
            QTableView {
                background-color: #b8cfca;
                gridline-color: #c0c0c0;
            }
            QTableView::item {
                background: white;  # Définit la couleur de base des items
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: 2px solid #c0c0c0;
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

#Permettre le drag and drop à partir de notre explorateur de fichier
# Crée une zone de dépot intercative qui accepte les fichiers
class DragDropLabel(QtWidgets.QLabel):
    fichier_dropped = QtCore.pyqtSignal(list)  # Signal émis avec les chemins

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                padding: 20px;
            }
        """)

    def dragEnterEvent(self, event): #Cette fonction est déclenchée quand un fichier survole la zone
        if event.mimeData().hasUrls():
            event.acceptProposedAction() #vérifie si les fichiers sont valides
            self.setStyleSheet("border: 2px dashed #2196F3;") #change le visuel avec des bordures bleues quand un fichier survole

    def dragLeaveEvent(self, event):
        self.setStyleSheet("border: 2px dashed #aaa;") #réinitialise le style quand le drag quitte la zone

    def dropEvent(self, event):
        self.setStyleSheet("border: 2px dashed #aaa;")
        paths = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            # Si c'est un dossier, on ajoute le dossier entier
            if os.path.isdir(path):
                paths.append(path)
            else:
                paths.append(path)
        if paths:
            self.fichier_dropped.emit(paths)


#classe principale
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.dossier_irm = None
        #   MAIN WINDOW
        self.dialog = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1121, 761)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777214))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonFollowStyle)
        MainWindow.setStyleSheet("""
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
                        background-color: #b8ccd1;
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
        """
        Les QWidget ont un fond gris clair et la couleur du texte est en noir
        Les QPushButton ont un fond gris clair, ont une bordure de 1 pixel en gris plus foncé et padding ajoute un espace de 5 pixels autour du texte du bouton
        les QTabWidget ont une bordure fine de 1 pixel autour du panneau, en gris clair
        Les QPushButton ont une couleur plus foncée quand on appuie dessus (gris foncé)
        """

        #   WIDGET CENTRAL + VERTICAL LAYOUT ASSOCIE
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # TAB WIDGET PROFIL
        self.Profil_tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        self.Profil_tabWidget.setFont(font)
        self.Profil_tabWidget.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.Profil_tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.Profil_tabWidget.setObjectName("Profil_tabWidget")

        #   TAB PATIENT
        self.Patients = QtWidgets.QWidget()
        self.Patients.setObjectName("Patients")
        self.verticalLayout_patients = QtWidgets.QVBoxLayout(self.Patients)
        self.verticalLayout_patients.setObjectName("VerticalLayoutPatients")

        #   TABLEAU CONTENANT LES PATIENTS
        self.table_patients_Widget = HoverTableWidget(parent=self.Patients) #avant : QtWidgets.QTableWidget(parent=self.Patients)
        self.table_patients_Widget.setShowGrid(True)
        self.table_patients_Widget.setObjectName("table_patients_Widget")
        self.table_patients_Widget.setColumnCount(3) #Ici, on souhaite 3 colonnes ==> NISS, Nom et prénom
        self.table_patients_Widget.setHorizontalHeaderLabels(["NISS", "Nom", "Prénom"])
        self.table_patients_Widget.setRowCount(0)
        header = self.table_patients_Widget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) #Repartition automatique de l'espace de façon égale entre les 3 colonnes
        self.verticalLayout_patients.addWidget(self.table_patients_Widget)
        self.Profil_tabWidget.addTab(self.Patients, "")

        #   TAB IRM
        self.IRM = QtWidgets.QWidget()
        self.IRM.setObjectName("IRM")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.IRM)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        #   PAGE IRM AVEC DRAG AND DROP FILE ET AJOUTER UN FILE
        self.label = DragDropLabel(parent=self.IRM)
        self.label.fichier_dropped.connect(self.on_files_dropped)
        self.label.setAcceptDrops(True)
        self.label.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.Insrer_IRM_pushButton = QtWidgets.QPushButton(parent=self.IRM)
        self.Insrer_IRM_pushButton.setIconSize(QtCore.QSize(30, 20))
        self.Insrer_IRM_pushButton.setObjectName("Insrer_IRM_pushButton")
        self.verticalLayout_2.addWidget(self.Insrer_IRM_pushButton)

        #   TAB PROFIL
        self.Profil_tabWidget.addTab(self.IRM, "")
        self.Profil = QtWidgets.QWidget()
        self.Profil.setObjectName("Profil")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Profil)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        #   AJOUT DES CHAMPS DANS LA PAGE PROFIL
        self.INAMI_label = QtWidgets.QLabel(parent=self.Profil)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(14)
        self.INAMI_label.setFont(font)
        self.INAMI_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.INAMI_label.setObjectName("INAMI_label")
        self.verticalLayout_4.addWidget(self.INAMI_label)
        self.label_inami_rempli = QtWidgets.QLineEdit(parent=self.Profil)
        self.label_inami_rempli.setText("")
        self.label_inami_rempli.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_inami_rempli.setEnabled(False)
        self.label_inami_rempli.setObjectName("label_inami_rempli")
        self.verticalLayout_4.addWidget(self.label_inami_rempli)
        self.nom_label = QtWidgets.QLabel(parent=self.Profil)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(14)
        self.nom_label.setFont(font)
        self.nom_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.nom_label.setObjectName("nom_label")
        self.verticalLayout_4.addWidget(self.nom_label)
        self.label_nom_rempli = QtWidgets.QLineEdit(parent=self.Profil)
        self.label_nom_rempli.setText("")
        self.label_nom_rempli.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_nom_rempli.setEnabled(False)
        self.label_nom_rempli.setObjectName("label_nom_rempli")
        self.verticalLayout_4.addWidget(self.label_nom_rempli)
        self.prenom_label = QtWidgets.QLabel(parent=self.Profil)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(14)
        self.prenom_label.setFont(font)
        self.prenom_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.prenom_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.prenom_label.setObjectName("prenom_label")
        self.verticalLayout_4.addWidget(self.prenom_label)
        self.label_prenom_rempli = QtWidgets.QLineEdit(parent=self.Profil)
        self.label_prenom_rempli.setText("")
        self.label_prenom_rempli.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_prenom_rempli.setEnabled(False)
        self.label_prenom_rempli.setObjectName("label_prenom_rempli")
        self.verticalLayout_4.addWidget(self.label_prenom_rempli)
        self.mail_utilisateur_label = QtWidgets.QLabel(parent=self.Profil)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(14)
        self.mail_utilisateur_label.setFont(font)
        self.mail_utilisateur_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mail_utilisateur_label.setObjectName("mail_utilisateur_label")
        self.verticalLayout_4.addWidget(self.mail_utilisateur_label)
        self.label_email_rempli = QtWidgets.QLineEdit(parent=self.Profil)
        self.label_email_rempli.setText("")
        self.label_email_rempli.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_email_rempli.setEnabled(False)
        self.label_email_rempli.setObjectName("label_email_rempli")
        self.verticalLayout_4.addWidget(self.label_email_rempli)
        self.Profil_tabWidget.addTab(self.Profil, "")
        self.verticalLayout.addWidget(self.Profil_tabWidget)

        # BOUTON POUR AJOUTER UN PATIENT SUR LA PAGE PATIENTS
        self.ajouter_patient_pushButton = QtWidgets.QPushButton(parent=self.Patients)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        self.ajouter_patient_pushButton.setFont(font)
        self.ajouter_patient_pushButton.setIconSize(QtCore.QSize(30, 20))
        self.ajouter_patient_pushButton.setObjectName("ajouter_patient_pushButton")
        self.verticalLayout_patients.addWidget(self.ajouter_patient_pushButton)


        #   MAIN WINDOW ET MENU BAR
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1121, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.Profil_tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.Profil_tabWidget.currentChanged.connect(self.tab_changed)
        self.Insrer_IRM_pushButton.clicked.connect(lambda: self.ouvrir_explorateur_fichier())
        self.ajouter_patient_pushButton.clicked.connect(lambda: self.ajouter_patient_db())


        self.table_patients_Widget.itemClicked.connect(self.cliquer_sur_patient)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(14)
        self.label_inami_rempli.setFont(font)
        self.label_nom_rempli.setFont(font)
        self.label_email_rempli.setFont(font)
        self.label_prenom_rempli.setFont(font)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        font.setBold(True)
        self.nom_label.setFont(font)
        self.prenom_label.setFont(font)
        self.mail_utilisateur_label.setFont(font)
        self.INAMI_label.setFont(font)

        #Barre de progression
        self.progressBar = QtWidgets.QProgressBar(parent=self.IRM)
        self.progressBar.setVisible(False)
        self.verticalLayout_2.addWidget(self.progressBar)
        self.progress_timer = QtCore.QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.upload_thread = None
        self.progressBar.setRange(0, 100)

    def tab_changed(self, index):
        if index == 0:  # Index de l'onglet Patients
            self.tableau_patient()

    def tableau_patient(self): #But : remplir la table de patients (Widget) avec la table de patients de la base de données
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Patient")
            patients = cursor.fetchall()
            self.table_patients_Widget.setRowCount(len(patients))
            self.table_patients_Widget.setColumnCount(3)
            for rangées, patient in enumerate(patients):
                for colonnes, data in enumerate(patient):
                    self.table_patients_Widget.setItem(rangées, colonnes, QtWidgets.QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.about(None, "Erreur", f"Erreur DB patients:\n{str(e)}")


    def ouvrir_explorateur_fichier(self):

        dossier = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            "Veuillez choisir un dossier contenant toutes les IRM",
            "",
            QtWidgets.QFileDialog.Option.ShowDirsOnly
        )
        if dossier:
            # Lancer le dialogue pour choisir le patient AVANT l'upload
            self.save_IRM_patient_info()
            self.dossier_irm = dossier
            if hasattr(self, "patient_info") and self.patient_info and (self.choix_ia or self.choix_box_encadrer or self.choix_deposer_masque):
                self.handle_upload(dossier) #Enregistrement du dossier dans Google Drive et génération de l'URL
            else:
                QMessageBox.warning(None, "Annulé", "Aucun patient sélectionné, upload annulé.")

    def on_files_dropped(self, paths):

        if paths and os.path.isdir(paths[0]):
            dossier = paths[0]
            self.dossier_irm = dossier = paths[0]
            # Lancer le dialogue pour choisir le patient
            self.save_IRM_patient_info()

            if hasattr(self, "patient_info") and self.patient_info and (self.choix_ia or self.choix_box_encadrer or self.choix_deposer_masque):
                self.handle_upload(dossier)
            else:
                QMessageBox.warning(None, "Annulé", "Aucun patient sélectionné, upload annulé.")
                self.progressBar.setVisible(False)
        else:
            QMessageBox.warning(None, "Erreur", "Veuillez déposer un dossier valide")

    #Ouvrir la fenêtre de dialogue pour enregistrer les données sous le nom d'un patient
    def save_IRM_patient_info(self):
        try :
            #Boite de dialogue
            dialogue = QtWidgets.QDialog()
            ui_dialog = Ui_Inserer_IRM_informations()
            ui_dialog.setupUi(dialogue)
            #On récup les noms et prénoms des patients
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Patient")
            patients = cursor.fetchall() #Liste avec tous les noms de patients + id


            ui_dialog.add_nom_patients(patients) #Les noms des patients sont maintenant dans la liste déroulant
            dialogue.setWindowTitle("Veuillez sélectionner le patient et le type d'analyse")
            if dialogue.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                print("Traitement réussi")
                #On souhaite connaître quel type d'analyse l'utilisateur veut faire
                self.choix_ia = ui_dialog.get_choix_ia() #Si le bouton choix ia est coché
                self.choix_box_encadrer = ui_dialog.get_choix_box() #Si le bouton choix faire encadrement est coché
                self.choix_deposer_masque = ui_dialog.get_choix_donner_masque() #Si le bouton donner son propre masque est coché
                patient_info = ui_dialog.get_patient_info()
                cursor.execute(
                    "SELECT NISS FROM Patient WHERE Nom = %s AND Prenom = %s",  # Deux placeholders
                    (patient_info['nom'], patient_info['prenom'])  # Deux valeurs
                )
                niss = cursor.fetchone()
                patient_info['niss'] = niss[0]
                print("Patient sélectionné (patient info):", patient_info)
                self.patient_info = patient_info
                #En fonction du choix de l'analyse

        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur DB patients:\n{str(e)}")


    def cliquer_sur_patient(self,item):
        row = self.table_patients_Widget.currentRow()
        texte = f"{self.table_patients_Widget.item(row, 1).text()} {self.table_patients_Widget.item(row, 2).text()} - NISS : {self.table_patients_Widget.item(row, 0).text()}"
        niss_patient = self.table_patients_Widget.item(row, 0).text()
        try :
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT Lien_irm FROM IRM WHERE NISS=%s", (niss_patient,))
            lien_url = cursor.fetchall()
            dialogue = QtWidgets.QDialog()
            ui_dialog = Ui_Suivi_Lesions()
            ui_dialog.setupUi(dialogue)
            dialogue.setWindowTitle(f"Suivi des lésions de {texte}")
            ui_dialog.ajouter_telechargement_google_drive(lien_url)
            ui_dialog.recuperer_niss(niss_patient)
            dialogue.setWindowState(QtCore.Qt.WindowState.WindowFullScreen)
            if dialogue.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                print("Traitement réussi")
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur affichage fenêtre:\n{str(e)}")

    #Ajouter un patient à la base de donnée à travers l'application
    def ajouter_patient_db(self):
        try :
            dialogue = QtWidgets.QDialog()
            ui_dialog = Ui_Ajout_patient()
            ui_dialog.setupUi(dialogue)
            ui_dialog.dialog = dialogue
            dialogue.setWindowTitle("Ajout d'un patient")
            if dialogue.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                print("Traitement réussi")
            self.tableau_patient()
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur affichage fenêtre:\n{str(e)}")

    def ajouter_infos_profil(self,email):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT INAMI, Nom, Prenom, Adresse_mail FROM Utilisateur WHERE Adresse_mail = %s""", (email,))
            utilisateur = cursor.fetchone()

            if utilisateur :
                print(f"""
                Données reçues :
                - INAMI: {utilisateur[0]}
                - Nom: {utilisateur[1]}
                - Prenom: {utilisateur[2]}
                - Email: {utilisateur[3]}
                """)
                self.label_inami_rempli.setText(str(utilisateur[0]))
                self.label_nom_rempli.setText(utilisateur[1])
                self.label_prenom_rempli.setText(utilisateur[2])
                self.label_email_rempli.setText(utilisateur[3])
            else:
                QMessageBox.warning(None,"Erreur","Utilisateur non trouvé dans la base de données")
        except mysql.connector.Error as e:
            QMessageBox.critical(None,"Erreur DB",f"Erreur lors du chargement du profil : {e}")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'con' in locals(): conn.close()



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Application suivi des lésions - cancer du sein"))
        self.Profil_tabWidget.setTabText(self.Profil_tabWidget.indexOf(self.Patients), _translate("MainWindow", "Patients"))
        self.label.setText(_translate("MainWindow", "Veuillez déposé un fichier"))
        self.Insrer_IRM_pushButton.setText(_translate("MainWindow", "Choisir un fichier"))
        self.Profil_tabWidget.setTabText(self.Profil_tabWidget.indexOf(self.IRM), _translate("MainWindow", "IRM"))
        self.INAMI_label.setText(_translate("MainWindow", "Numéro INAMI"))
        self.nom_label.setText(_translate("MainWindow", "Nom"))
        self.prenom_label.setText(_translate("MainWindow", "Prénom"))
        self.mail_utilisateur_label.setText(_translate("MainWindow", "Adresse électronique"))
        self.Profil_tabWidget.setTabText(self.Profil_tabWidget.indexOf(self.Profil), _translate("MainWindow", "Profil"))
        self.label.setToolTip(_translate("MainWindow", "Déposez des fichiers IRM ici"))
        self.ajouter_patient_pushButton.setText(_translate("MainWindow", "Ajouter un patient"))

    #Fonctions liées à la barre de progression :
    def start_progress(self):
        self.progressBar.setVisible(True)
        self.progressBar.setValue(0)
        self.progress_timer.start(100)  # Mise à jour toutes les 100ms

    def update_progress(self):
        if self.progressBar.value() < 100:
            self.progressBar.setValue(self.progressBar.value() + 2)
        else:
            self.progress_timer.stop()
            self.progressBar.setVisible(False)

    def handle_upload(self, dossier): #MARCHE TRES BIEN
        try:
            if not hasattr(self, "patient_info"):
                raise ValueError("Informations patient manquantes")

            self.start_progress()

            # Créer le worker avec TOUS les paramètres nécessaires
            self.upload_thread = UploadWorker(
                dossier=dossier,
                patient_info=self.patient_info,
                inami=self.label_inami_rempli.text()
            )

            # Connecter les signaux
            self.upload_thread.finished.connect(self.on_upload_and_db_complete)
            self.upload_thread.progress_updated.connect(self.progressBar.setValue)
            self.upload_thread.error_occurred.connect(self.on_upload_error)

            self.upload_thread.start()


        except Exception as e:
            self.progressBar.setVisible(False)
            QMessageBox.critical(None, "Erreur", str(e))


    def finish_upload(self, dossier):
        ajouter_dossier(dossier)
        if hasattr(self, "patient_info") and self.patient_info:
            upload_dossier(
                self.patient_info.get("nom", "Patient"),
                self.patient_info.get("prenom", "Inconnu")
            )
        self.progressBar.setValue(100)
        QtCore.QTimer.singleShot(500, lambda: self.progressBar.setVisible(False))

    def on_upload_complete(self):
        self.progressBar.setVisible(False)
        QMessageBox.information(None, "Succès", "Upload terminé avec succès!")

    def on_upload_error(self, message):
        self.progressBar.setVisible(False)
        QMessageBox.critical(None, "Erreur", message)

    def get_last_id_irm(self, niss_patient):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Récupère le dernier Id_irm du patient, trié par ID décroissant
            cursor.execute("""
                SELECT Id_irm 
                FROM IRM 
                WHERE NISS = %s 
                ORDER BY Id_irm DESC 
                LIMIT 1
            """, (niss_patient,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()
            conn.close()

    def on_upload_and_db_complete(self,id_irm):
        print(f"ID IRM généré : {id_irm}")
        # Lancer la segmentation avec l'Id_irm valide
        if hasattr(self, "patient_info") and self.choix_ia:
            masques_save = Code_Segmentation_Masques.save_dicom_to_jpeg(self.dossier_irm, self.patient_info, id_irm)
            print("Segmentation terminée avec ID valide")
        elif hasattr(self,"patient_info") and self.choix_box_encadrer:
            masques_save = Code_Segmentation_Masques_2.save_dicom_to_jpeg(self.dossier_irm, self.patient_info, id_irm)
        elif hasattr(self,"patient_info") and self.choix_deposer_masque:
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "Veuillez choisir un masque, en format jpeg",
                "",  # répertoire de départ ("" = dossier courant)
                "Images (*.jpg *.jpeg *.png)"  # filtres pour ne montrer que les images
            )

            if file_path:
                self.dossier_masque = file_path
                dicom_files = sorted([
                    f for f in os.listdir(self.dossier_irm)
                    if f.lower().endswith(".dcm")
                ])
                for i, filename in enumerate(dicom_files, 1):
                    dicom_path = os.path.join(self.dossier_irm, filename)
                    jpeg_name = filename.replace(".dcm", ".jpeg")
                    jpeg_path = os.path.join(self.dossier_irm, jpeg_name)
                    Code_Segmentation_Masques.dicom_to_jpeg(dicom_path, jpeg_path)
                    print(f"{jpeg_path} sauvegardé, pour l'insertion du masque")
                    chemin_csv = Pyradiomics.get_caracteristics(jpeg_path, self.dossier_masque,self.patient_info, id_irm, choix=3)
                    upload_url = Pyradiomics.upload_csv(self.patient_info["nom"],self.patient_info["prenom"],chemin_csv)
                    if os.path.exists(jpeg_path):
                        os.remove(jpeg_path)
                        print(f"{jpeg_path} supprimé.")
            else:
                print("erreur : pas de masques sélectionné")
        self.avoir_statut_traitement(niss_patient=self.patient_info["niss"])

    def rajouter_dans_bdd(self, resultat, niss_patient):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Utilisation du même nom de colonnes que dans le CREATE TABLE
            cursor.execute(
                "UPDATE Patient SET Résultat_suivi = %s WHERE NISS = %s",
                (resultat, niss_patient)
            )
            conn.commit()
            # Message avec parent explicite
            QtWidgets.QMessageBox.information(
                None,
                "Success",
                "Analyse réalisée avec succès"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.dialog,
                "Erreur inattendue",
                f"Erreur : {str(e)}"
            )
            if conn: conn.rollback()
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def avoir_statut_traitement(self, niss_patient):
        resultat_texte = MLP.in_mlp(niss_patient)
        if resultat_texte == "Pas assez de date pour avoir un résultat sur le traitement":
            self.rajouter_dans_bdd(-1, niss_patient)
        elif resultat_texte == "La patiente ne réagit pas positivement au traitement":
            self.rajouter_dans_bdd(0, niss_patient)
        elif resultat_texte == "La patiente réagit positivement au traitement":
            self.rajouter_dans_bdd(1, niss_patient)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #Pour que l'appli ait le thème clair
    app.setStyle("Fusion")
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(240, 240, 240))
    palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(0, 0, 0))
    palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(255, 255, 255))
    palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(0, 120, 215))  # Bleu = couleur de surbrillance du texte sélectionné
    palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(255, 255, 255))
    app.setPalette(palette)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized() #Ouvrir direct l'appli en grand écran
    sys.exit(app.exec())