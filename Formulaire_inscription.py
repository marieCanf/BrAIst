import mysql.connector
from PyQt6 import QtCore, QtGui, QtWidgets
import re
from database import get_connection
from argon2 import PasswordHasher #Afin de hasher le mdp

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1000, 600)
        self.dialog = Dialog
        Dialog.setStyleSheet("""
                                    
                                    QWidget {
                                        background-color: #dceef2;
                                        color: black;
                                    }
                                    QPushButton {
                                        background-color: #e0e0e0;
                                        border: 1px solid #a0a0a0;
                                        padding: 5px;
                                    }
                                    QTabWidget::pane {
                                        border: 1px solid #c0c0c0;
                                    }
                                    QPushButton:pressed {
                                        background-color: #c0c0c0;
                                    }
                                """)
        self.formulaire_inscription_label = QtWidgets.QLabel(parent=Dialog)
        self.formulaire_inscription_label.setGeometry(QtCore.QRect(352, 20, 371, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.formulaire_inscription_label.setFont(font)
        self.formulaire_inscription_label.setStyleSheet("color: rgb(85, 170, 127);\n""\n""")
        self.formulaire_inscription_label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.formulaire_inscription_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.formulaire_inscription_label.setObjectName("formulaire_inscription_label")
        self.nom_utilisateur_label = QtWidgets.QLabel(parent=Dialog)
        self.nom_utilisateur_label.setGeometry(QtCore.QRect(230, 110, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.nom_utilisateur_label.setFont(font)
        self.nom_utilisateur_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.nom_utilisateur_label.setObjectName("nom_utilisateur_label")
        self.nom_lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.nom_lineEdit.setGeometry(QtCore.QRect(360, 110, 421, 31))
        self.nom_lineEdit.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.nom_lineEdit.setObjectName("nom_lineEdit")
        self.prenom_utilisateur_label = QtWidgets.QLabel(parent=Dialog)
        self.prenom_utilisateur_label.setGeometry(QtCore.QRect(230, 170, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.prenom_utilisateur_label.setFont(font)
        self.prenom_utilisateur_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.prenom_utilisateur_label.setObjectName("prenom_utilisateur_label")
        self.prenom_lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.prenom_lineEdit.setGeometry(QtCore.QRect(360, 170, 421, 31))
        self.prenom_lineEdit.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.prenom_lineEdit.setObjectName("prenom_lineEdit")
        self.inami_utilisateur_label_2 = QtWidgets.QLabel(parent=Dialog)
        self.inami_utilisateur_label_2.setGeometry(QtCore.QRect(180, 230, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.inami_utilisateur_label_2.setFont(font)
        self.inami_utilisateur_label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.inami_utilisateur_label_2.setObjectName("inami_utilisateur_label_2")
        self.inami_lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.inami_lineEdit.setGeometry(QtCore.QRect(360, 230, 421, 31))
        self.inami_lineEdit.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.inami_lineEdit.setObjectName("inami_lineEdit")
        self.email_utilisateur_label = QtWidgets.QLabel(parent=Dialog)
        self.email_utilisateur_label.setGeometry(QtCore.QRect(180, 290, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.email_utilisateur_label.setFont(font)
        self.email_utilisateur_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.email_utilisateur_label.setObjectName("email_utilisateur_label")
        self.email_lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.email_lineEdit.setGeometry(QtCore.QRect(360, 290, 421, 31))
        self.email_lineEdit.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.mdp_utilisateur_label = QtWidgets.QLabel(parent=Dialog)
        self.mdp_utilisateur_label.setGeometry(QtCore.QRect(180, 350, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.mdp_utilisateur_label.setFont(font)
        self.mdp_utilisateur_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mdp_utilisateur_label.setObjectName("mdp_utilisateur_label")
        self.mdp_lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.mdp_lineEdit.setGeometry(QtCore.QRect(360, 350, 421, 31))
        self.mdp_lineEdit.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.mdp_lineEdit.setObjectName("mdp_lineEdit")
        self.critere_mdp_label = QtWidgets.QLabel(parent=Dialog)
        self.critere_mdp_label.setGeometry(QtCore.QRect(360, 385, 421, 40))
        self.Visualiser_mdp_checkBox = QtWidgets.QCheckBox(parent=Dialog)
        self.Visualiser_mdp_checkBox.setGeometry(QtCore.QRect(360, 430, 181, 20))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.Visualiser_mdp_checkBox.setFont(font)
        self.Visualiser_mdp_checkBox.setAutoFillBackground(False)
        self.Visualiser_mdp_checkBox.setTristate(False)
        self.Visualiser_mdp_checkBox.setObjectName("Visualiser_mdp_checkBox")
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(9)
        self.critere_mdp_label.setFont(font)
        self.critere_mdp_label.setStyleSheet("color : rgb(255, 0, 0)")
        self.critere_mdp_label.setObjectName("critere_mdp_label")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(770, 350, 54, 16))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("color : rgb(255, 0, 0)")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.confirmation_mdp_label = QtWidgets.QLabel(parent=Dialog)
        self.confirmation_mdp_label.setGeometry(QtCore.QRect(40, 430, 301, 81))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.confirmation_mdp_label.setFont(font)
        self.confirmation_mdp_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.confirmation_mdp_label.setObjectName("nom_utilisateur_label_2")
        self.lineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(360, 460, 421, 31))
        self.lineEdit.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.lineEdit.setObjectName("lineEdit")
        self.valider_pushButton = QtWidgets.QPushButton(parent=Dialog)
        self.valider_pushButton.setGeometry(QtCore.QRect(429, 540, 231, 28))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.valider_pushButton.setFont(font)
        self.valider_pushButton.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.valider_pushButton.setObjectName("valider_pushButton")
        self.label.raise_()
        self.formulaire_inscription_label.raise_()
        self.nom_utilisateur_label.raise_()
        self.nom_lineEdit.raise_()
        self.prenom_utilisateur_label.raise_()
        self.prenom_lineEdit.raise_()
        self.inami_utilisateur_label_2.raise_()
        self.inami_lineEdit.raise_()
        self.email_utilisateur_label.raise_()
        self.email_lineEdit.raise_()
        self.mdp_utilisateur_label.raise_()
        self.mdp_lineEdit.raise_()
        self.Visualiser_mdp_checkBox.raise_()
        self.critere_mdp_label.raise_()
        self.confirmation_mdp_label.raise_()
        self.lineEdit.raise_()
        self.valider_pushButton.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.Visualiser_mdp_checkBox.stateChanged.connect(self.afficher_mdp)
        self.mdp_lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.valider_pushButton.clicked.connect(self.valider_formulaire)
        self.ph = PasswordHasher()
        self.nom_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.prenom_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.inami_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.email_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mdp_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        self.nom_lineEdit.setFont(font)
        self.prenom_lineEdit.setFont(font)
        self.inami_lineEdit.setFont(font)
        self.email_lineEdit.setFont(font)
        self.mdp_lineEdit.setFont(font)
        self.lineEdit.setFont(font)
        self.critere_mdp_label.setWordWrap(True)

    def afficher_mdp(self,state):
        #On affiche le mdp de base
        self.mdp_lineEdit.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Normal if state
            else QtWidgets.QLineEdit.EchoMode.Password
        )
        #On affiche la confirmation de mdp
        self.lineEdit.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Normal if state
            else QtWidgets.QLineEdit.EchoMode.Password
        )

    def valid_password(self,password: str) -> bool:
        # - (?=.*[A-Z]) : au moins une lettre majuscule
        # - (?=.*\W)    : au moins un caractère spécial (non alphanumérique)
        # - (?=.*\d)    : au moins un chiffre
        pattern = r'^(?=.*[A-Z])(?=.*\W)(?=.*\d).+$'
        return re.search(pattern, password) is not None

    def valider_formulaire(self):
        password = self.mdp_lineEdit.text()
        confirm_password = self.lineEdit.text()
        nom = self.nom_lineEdit.text().strip()
        prenom = self.prenom_lineEdit.text().strip()
        inami = self.inami_lineEdit.text().strip()
        email = self.email_lineEdit.text().strip()
        password = self.mdp_lineEdit.text()
        confirm_password = self.lineEdit.text()
        if not nom or not prenom or not inami or not email or not password or not confirm_password:
            QtWidgets.QMessageBox.warning(None, "Champs obligatoires",
                                          "Tous les champs doivent être remplis.")
            return
        if not self.valid_password(password):
            QtWidgets.QMessageBox.warning(None, "Mot de passe invalide",
                                          "Le mot de passe doit contenir au moins une lettre majuscule, un caractère spécial et un chiffre.")
            return
        if password != confirm_password:
            QtWidgets.QMessageBox.warning(None, "Erreur",
                                          "Les mots de passe ne correspondent pas.")
            return
        # Si tout est bon, on affiche un message de succès
        QtWidgets.QMessageBox.information(None, "Inscription réussie",
                                          "Votre inscription a été validée avec succès !")
        self.enregistrer_utilisateur_db()
        self.dialog.close()

    def enregistrer_utilisateur_db(self):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            password = self.mdp_lineEdit.text()
            hashed_pw = self.ph.hash(password)

            query = """
                        INSERT INTO Utilisateur (INAMI, Adresse_mail, Nom, Prenom, Mot_de_passe) VALUES (%s, %s, %s, %s, %s)"""

            values = (
                self.inami_lineEdit.text().strip(),
                self.email_lineEdit.text().strip(),
                self.nom_lineEdit.text().strip(),
                self.prenom_lineEdit.text().strip(),
                hashed_pw
            )

            cursor.execute(query, values)
            conn.commit()
            return True

        except mysql.connector.Error as e:
            if "Duplicate entry" in str(e):
                QtWidgets.QMessageBox.critical(
                    None,
                    "Erreur d'inscription",
                    "Ce numéro INAMI ou cette adresse email est déjà enregistré!"
                )
            else:
                QtWidgets.QMessageBox.critical(
                    None,
                    "Erreur base de données",
                    f"Erreur technique : {e}"
                )
            return False

        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(
                None,
                "Erreur de connexion",
                f"Impossible de se connecter à la base de données : {e}"
            )
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.formulaire_inscription_label.setText(_translate("Dialog", "Formulaire d\'inscription"))
        self.nom_utilisateur_label.setText(_translate("Dialog", "Nom"))
        self.prenom_utilisateur_label.setText(_translate("Dialog", "Prénom"))
        self.inami_utilisateur_label_2.setText(_translate("Dialog", "Numéro INAMI"))
        self.email_utilisateur_label.setText(_translate("Dialog", "Adresse email"))
        self.mdp_utilisateur_label.setText(_translate("Dialog", "Mot de passe"))
        self.Visualiser_mdp_checkBox.setText(_translate("Dialog", "Visualiser le mot de passe"))
        self.critere_mdp_label.setText(_translate("Dialog", "*Le mot de passe doit contenir au moins une lettre majuscule,un caractère spécial ainsi qu\'un chiffre"))
        self.label.setText(_translate("Dialog", "*"))
        self.confirmation_mdp_label.setText(_translate("Dialog", "Confirmation du mot de passe"))
        self.valider_pushButton.setText(_translate("Dialog", "Confirmer l\'inscription"))


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

    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
