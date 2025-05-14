import mysql.connector
from PyQt6 import QtCore, QtGui, QtWidgets
from Formulaire_inscription import Ui_Dialog
from database import get_connection
from argon2 import PasswordHasher, exceptions
from fenêtre_principale import Ui_MainWindow


class Ui_Dialog_portail_connexion(object):
    def setupUi(self, Dialog_portail_connexion):
        self.dialog = Dialog_portail_connexion
        Dialog_portail_connexion.setObjectName("Dialog_portail_connexion")
        Dialog_portail_connexion.resize(842, 566)
        Dialog_portail_connexion.setWindowOpacity(1.0)
        Dialog_portail_connexion.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        Dialog_portail_connexion.setStyleSheet("""
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
                                background-color: #e8d7c5;
                                border: 1px solid #c0c0c0;
                            }
                            QPushButton:pressed {
                                background-color: #c0c0c0;
                            }
                        """)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_portail_connexion)
        self.verticalLayout.setObjectName("verticalLayout")
        self.explain_label = QtWidgets.QLabel(parent=Dialog_portail_connexion)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.explain_label.sizePolicy().hasHeightForWidth())
        self.explain_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.explain_label.setFont(font)
        self.explain_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.explain_label.setObjectName("explain_label")
        self.verticalLayout.addWidget(self.explain_label)
        self.speech_label = QtWidgets.QLabel(parent=Dialog_portail_connexion)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(18)
        font.setItalic(False)
        self.speech_label.setFont(font)
        self.speech_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.speech_label.setObjectName("speech_label")
        self.verticalLayout.addWidget(self.speech_label)
        self.email_connexion_label = QtWidgets.QLabel(parent=Dialog_portail_connexion)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(14)
        self.email_connexion_label.setFont(font)
        self.email_connexion_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.email_connexion_label.setObjectName("email_connexion_label")
        self.verticalLayout.addWidget(self.email_connexion_label)
        self.email_lineEdit = QtWidgets.QLineEdit(parent=Dialog_portail_connexion)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_lineEdit.sizePolicy().hasHeightForWidth())
        self.email_lineEdit.setSizePolicy(sizePolicy)
        self.email_lineEdit.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.email_lineEdit.setText("")
        self.email_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.verticalLayout.addWidget(self.email_lineEdit)
        self.mdp_connexion_label = QtWidgets.QLabel(parent=Dialog_portail_connexion)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(14)
        self.mdp_connexion_label.setFont(font)
        self.mdp_connexion_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mdp_connexion_label.setObjectName("mdp_connexion_label")
        self.verticalLayout.addWidget(self.mdp_connexion_label)
        self.mdp_lineEdit = QtWidgets.QLineEdit(parent=Dialog_portail_connexion)
        self.mdp_lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdp_lineEdit.sizePolicy().hasHeightForWidth())
        self.mdp_lineEdit.setSizePolicy(sizePolicy)
        self.mdp_lineEdit.setText("")
        self.mdp_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mdp_lineEdit.setObjectName("mdp_lineEdit")
        self.verticalLayout.addWidget(self.mdp_lineEdit)
        self.checkBox = QtWidgets.QCheckBox(parent=Dialog_portail_connexion)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(9)
        self.checkBox.setFont(font)
        self.checkBox.setTristate(False)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.Connexion_pushButton = QtWidgets.QPushButton(parent=Dialog_portail_connexion)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.Connexion_pushButton.setFont(font)
        self.Connexion_pushButton.setAutoFillBackground(False)
        self.Connexion_pushButton.setObjectName("Connexion_pushButton")
        self.verticalLayout.addWidget(self.Connexion_pushButton)
        self.separateur = QtWidgets.QFrame(parent=Dialog_portail_connexion)
        self.separateur.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.separateur.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        # Ajout de 20 pixels de marge au-dessus du séparateur
        self.verticalLayout.addSpacing(20)
        self.verticalLayout.addWidget(self.separateur)
        self.verticalLayout.addWidget(self.separateur)
        self.label = QtWidgets.QLabel(parent=Dialog_portail_connexion)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Inscription_pushButton = QtWidgets.QPushButton(parent=Dialog_portail_connexion)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.Inscription_pushButton.setFont(font)
        self.Inscription_pushButton.setObjectName("Inscription_pushButton")
        self.verticalLayout.addWidget(self.Inscription_pushButton)

        self.retranslateUi(Dialog_portail_connexion)
        QtCore.QMetaObject.connectSlotsByName(Dialog_portail_connexion)

        self.checkBox.stateChanged.connect(self.afficher_mdp)
        self.Inscription_pushButton.clicked.connect(lambda:self.inscription_clicked())
        self.ph = PasswordHasher()  # Initialiser le vérificateur de mot de passe
        self.Connexion_pushButton.clicked.connect(self.verifier_identifiants)
        self.mdp_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.email_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        self.email_lineEdit.setFont(font)
        self.mdp_lineEdit.setFont(font)
    #Fonction pour afficher et masquer le mot de passe
    def afficher_mdp(self,state):
        self.mdp_lineEdit.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Normal if state
            else QtWidgets.QLineEdit.EchoMode.Password
        )

    def inscription_clicked(self):
        try :
            dialogue = QtWidgets.QDialog()
            ui_dialogue = Ui_Dialog()
            ui_dialogue.setupUi(dialogue)
            dialogue.setWindowTitle("Formulaire d'inscription à l'application")
            if dialogue.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                print("Traitement réussi")
        except Exception as e:
            print(e,"Erreur de connexion avec la page d'inscription")

    def verifier_identifiants(self):
        email = self.email_lineEdit.text().strip()
        password = self.mdp_lineEdit.text()

        if not email or not password:
            QtWidgets.QMessageBox.warning(None, "Champs manquants", "Veuillez remplir tous les champs")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Récupérer le hash stocké
            cursor.execute(
                "SELECT Mot_de_passe FROM Utilisateur WHERE Adresse_mail = %s",
                (email,)
            )
            result = cursor.fetchone()

            if not result:
                QtWidgets.QMessageBox.critical(None, "Erreur", "Utilisateur non trouvé")
                return

            stored_hash = result[0]

            # Vérifier le mot de passe
            try:
                if self.ph.verify(stored_hash, password):
                    QtWidgets.QMessageBox.information(None, "Succès", "Connexion réussie!")
                    self.email_utilisateur = email
                    self.dialog.accept() #pour fermer la fenêtre de connexion
                else:
                    QtWidgets.QMessageBox.critical(None, "Erreur", "Mot de passe incorrect")

            except exceptions.VerifyMismatchError:
                QtWidgets.QMessageBox.critical(None, "Erreur", "Mot de passe incorrect")

            except exceptions.VerificationError:
                QtWidgets.QMessageBox.critical(None, "Erreur", "Problème de vérification du mot de passe")

        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(None, "Erreur DB", f"Erreur de base de données : {e}")

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    def retranslateUi(self, Dialog_portail_connexion):
        _translate = QtCore.QCoreApplication.translate
        Dialog_portail_connexion.setWindowTitle(_translate("Dialog_portail_connexion", "Connexion à l'application"))
        self.explain_label.setText(_translate("Dialog_portail_connexion", "Bienvenue sur notre application de suivi du cancer du sein"))
        self.speech_label.setText(_translate("Dialog_portail_connexion", "Veuillez vous identifier"))
        self.email_connexion_label.setText(_translate("Dialog_portail_connexion", "Adresse électronique"))
        self.email_lineEdit.setPlaceholderText(_translate("Dialog_portail_connexion", "Entrez votre email..."))
        self.mdp_connexion_label.setText(_translate("Dialog_portail_connexion", "Mot de passe"))
        self.mdp_lineEdit.setPlaceholderText(_translate("Dialog_portail_connexion", "Entrez votre mot de passe..."))
        self.checkBox.setText(_translate("Dialog_portail_connexion", "Visualiser le mot de passe"))
        self.Connexion_pushButton.setText(_translate("Dialog_portail_connexion", "Connexion"))
        self.label.setText(_translate("Dialog_portail_connexion", "Vous n\'êtes pas encore inscrit ? "))
        self.Inscription_pushButton.setText(_translate("Dialog_portail_connexion", "Inscription"))






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle("Fusion")

    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(240, 240, 240))
    palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(0, 0, 0))
    palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(255, 255, 255))
    palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(0, 120, 215))  # Bleu, par exemple
    palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor(255, 255, 255))
    app.setPalette(palette)
    login_dialog = QtWidgets.QDialog()
    ui_login = Ui_Dialog_portail_connexion()
    ui_login.setupUi(login_dialog)
    ui_login.dialog = login_dialog

    if login_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        # Si connexion réussie, ouvrir la fenêtre principale
        main_window = QtWidgets.QMainWindow()
        ui_main = Ui_MainWindow()
        ui_main.setupUi(main_window)
        ui_main.ajouter_infos_profil(ui_login.email_utilisateur)
        main_window.showMaximized()
        sys.exit(app.exec())
    else:
        sys.exit(0)