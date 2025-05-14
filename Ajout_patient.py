import re
import mysql.connector
from PyQt6 import QtCore, QtGui, QtWidgets
from database import get_connection

class Ui_Ajout_patient(object):
    def setupUi(self, Ajout_patient):
        self.dialog = Ajout_patient
        Ajout_patient.setObjectName("Ajout_patient")
        Ajout_patient.resize(545, 442)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Ajout_patient.sizePolicy().hasHeightForWidth())
        Ajout_patient.setSizePolicy(sizePolicy)
        Ajout_patient.setMaximumSize(QtCore.QSize(545, 442))
        Ajout_patient.setStyleSheet("""
                            QWidget {
                                background-color: #f0f0f0;
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
        self.Titre_label = QtWidgets.QLabel(parent=Ajout_patient)
        self.Titre_label.setGeometry(QtCore.QRect(80, 40, 391, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.Titre_label.setFont(font)
        self.Titre_label.setStyleSheet("color: rgb(0, 85, 127);")
        self.Titre_label.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.Titre_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Titre_label.setObjectName("Titre_label")
        self.NISS_label = QtWidgets.QLabel(parent=Ajout_patient)
        self.NISS_label.setGeometry(QtCore.QRect(80, 120, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(14)
        self.NISS_label.setFont(font)
        self.NISS_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.NISS_label.setObjectName("NISS_label")
        self.NISS_lineEdit = QtWidgets.QLineEdit(parent=Ajout_patient)
        self.NISS_lineEdit.setGeometry(QtCore.QRect(240, 120, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        self.NISS_lineEdit.setFont(font)
        self.NISS_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.NISS_lineEdit.setObjectName("NISS_lineEdit")
        self.Nom_label = QtWidgets.QLabel(parent=Ajout_patient)
        self.Nom_label.setGeometry(QtCore.QRect(80, 190, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(14)
        self.Nom_label.setFont(font)
        self.Nom_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Nom_label.setObjectName("Nom_label")
        self.Nom_lineEdit = QtWidgets.QLineEdit(parent=Ajout_patient)
        self.Nom_lineEdit.setGeometry(QtCore.QRect(240, 190, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        self.Nom_lineEdit.setFont(font)
        self.Nom_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Nom_lineEdit.setPlaceholderText("")
        self.Nom_lineEdit.setObjectName("Nom_lineEdit")
        self.Prenom_label = QtWidgets.QLabel(parent=Ajout_patient)
        self.Prenom_label.setGeometry(QtCore.QRect(80, 260, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(14)
        self.Prenom_label.setFont(font)
        self.Prenom_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Prenom_label.setObjectName("Prenom_label")
        self.Prenom_lineEdit = QtWidgets.QLineEdit(parent=Ajout_patient)
        self.Prenom_lineEdit.setGeometry(QtCore.QRect(240, 260, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        self.Prenom_lineEdit.setFont(font)
        self.Prenom_lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Prenom_lineEdit.setPlaceholderText("")
        self.Prenom_lineEdit.setObjectName("Prenom_lineEdit")
        self.Save_button = QtWidgets.QPushButton(parent=Ajout_patient)
        self.Save_button.setGeometry(QtCore.QRect(150, 370, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(11)
        self.Save_button.setFont(font)
        self.Save_button.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.Save_button.setObjectName("Save_button")
        self.Cancel_button = QtWidgets.QPushButton(parent=Ajout_patient)
        self.Cancel_button.setGeometry(QtCore.QRect(290, 370, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.Cancel_button.setFont(font)
        self.Cancel_button.setStyleSheet("background-color: rgb(222, 88, 90);")
        self.Cancel_button.setObjectName("Cancel_button")

        self.retranslateUi(Ajout_patient)
        QtCore.QMetaObject.connectSlotsByName(Ajout_patient)


        #==================AJOUT================
        #self.Save_button.clicked.connect(lambda:self.)
        self.niss_valid = False
        self.mandatory_fields = [
            self.Nom_lineEdit,
            self.Prenom_lineEdit,
            self.NISS_lineEdit,
        ]
        self.Save_button.clicked.connect(lambda : self.validate_and_submit())
        self.NISS_lineEdit.textChanged.connect(lambda : self.niss_validation())
        self.Cancel_button.clicked.connect(lambda : self.annuler_clic())


    def retranslateUi(self, Ajout_patient):
            _translate = QtCore.QCoreApplication.translate
            Ajout_patient.setWindowTitle(_translate("Ajout_patient", "Dialog"))
            self.Titre_label.setText(_translate("Ajout_patient", "Ajouter un patient à la base de donnée"))
            self.NISS_label.setText(_translate("Ajout_patient", "Numéro NISS"))
            self.NISS_lineEdit.setPlaceholderText(_translate("Ajout_patient", "AA.MM.JJ-XXX.XX"))
            self.Nom_label.setText(_translate("Ajout_patient", "Nom "))
            self.Prenom_label.setText(_translate("Ajout_patient", "Prénom"))
            self.Save_button.setText(_translate("Ajout_patient", "Enregistrer"))
            self.Cancel_button.setText(_translate("Ajout_patient", "Annuler"))

    def niss_validation(self):
        niss = self.NISS_lineEdit.text()
        is_valid = re.fullmatch(r"^\d{2}\d{2}\d{2}\d{3}\d{2}$", niss)
        self.niss_valid = is_valid
        color = "#dff0d8" if is_valid else "#edafaf"
        self.NISS_lineEdit.setStyleSheet(f"background-color: {color};")

    def annuler_clic(self):
        self.dialog.close()

    def validate_and_submit(self):
        # Vérification des champs vides
        empty_fields = [
            field for field in self.mandatory_fields
            if isinstance(field, QtWidgets.QLineEdit) and not field.text().strip()
        ]

        # Highlight des champs manquants
        for field in self.mandatory_fields:
            if isinstance(field, QtWidgets.QLineEdit):
                field.setStyleSheet(
                    "background-color: #f2dede;" if not field.text().strip()
                    else ""
                )

        # Vérification NISS
        error_messages = []
        if not self.niss_valid:
            error_messages.append("- Format NISS invalide")
            self.NISS_lineEdit.setStyleSheet("background-color: #f2dede;")

        # Construction du message d'erreur
        if empty_fields or not self.niss_valid:
            message = "Erreurs :\n"
            if empty_fields:
                message += "- Champs obligatoires manquants\n"
            message += "\n".join(error_messages)

            QtWidgets.QMessageBox.critical(
                self.dialog,  # Utilisez la fenêtre parente ici
                "Formulaire incomplet",
                message
            )
            return

        # Si tout est valide
        self.sauver_patient_db()

    def sauver_patient_db(self):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Vérification supplémentaire des données
            niss = self.NISS_lineEdit.text().strip()
            if not niss:
                raise ValueError("Le NISS ne peut pas être vide")

            # Utilisation du même nom de colonnes que dans le CREATE TABLE
            cursor.execute(
                "INSERT INTO Patient (NISS, Nom, Prenom) VALUES (%s, %s, %s)",
                (
                    niss,
                    self.Nom_lineEdit.text().strip(),
                    self.Prenom_lineEdit.text().strip()
                )
            )

            conn.commit()

            # Message avec parent explicite
            QtWidgets.QMessageBox.information(
                self.dialog,
                "Succès",
                "Patient enregistré avec succès!"
            )
            self.dialog.close()
            # Réinitialisation sécurisée
            self.NISS_lineEdit.clear()
            self.Nom_lineEdit.clear()
            self.Prenom_lineEdit.clear()
            self.niss_valid = False  # Réinitialiser l'état de validation

        except mysql.connector.IntegrityError as e:
            QtWidgets.QMessageBox.critical(
                self.dialog,  # Fenêtre parente
                "Erreur",
                "Ce NISS existe déjà dans la base de données!"
            )
            if conn: conn.rollback()

        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(
                self.dialog,
                "Erreur technique",
                f"Erreur de base de données : {e}"
            )
            if conn: conn.rollback()

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


    Ajout_patient = QtWidgets.QDialog()
    ui = Ui_Ajout_patient()
    ui.setupUi(Ajout_patient)
    Ajout_patient.show()
    sys.exit(app.exec())
