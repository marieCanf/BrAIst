from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_Inserer_IRM_informations(object):
    def setupUi(self, Inserer_IRM_informations):
        Inserer_IRM_informations.setObjectName("Inserer_IRM_informations")
        Inserer_IRM_informations.resize(702, 604)
        Inserer_IRM_informations.setStyleSheet("""
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
        self.verticalLayout = QtWidgets.QVBoxLayout(Inserer_IRM_informations)
        self.verticalLayout.setObjectName("verticalLayout")
        self.IRM_nom_patient = QtWidgets.QLabel(parent=Inserer_IRM_informations)

        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(16)
        self.IRM_nom_patient.setFont(font)
        self.IRM_nom_patient.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.IRM_nom_patient.setObjectName("IRM_nom_patient")
        self.verticalLayout.addWidget(self.IRM_nom_patient)
        self.listePatients_comboBox = QtWidgets.QComboBox(parent=Inserer_IRM_informations)
        self.listePatients_comboBox.setEditable(False)
        self.listePatients_comboBox.setCurrentText("")
        self.listePatients_comboBox.setMaxVisibleItems(34)
        self.listePatients_comboBox.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAlphabetically)
        self.listePatients_comboBox.setFrame(True)
        self.listePatients_comboBox.setObjectName("listePatients_comboBox")
        self.verticalLayout.addWidget(self.listePatients_comboBox)
        self.information_label = QtWidgets.QLabel(parent=Inserer_IRM_informations)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(9)
        self.information_label.setFont(font)
        self.information_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.information_label.setObjectName("information_label")
        self.verticalLayout.addWidget(self.information_label)
        self.Faire_choix_masques = QtWidgets.QLabel(parent=Inserer_IRM_informations)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(15)
        self.Faire_choix_masques.setFont(font)
        self.Faire_choix_masques.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Faire_choix_masques.setObjectName("Faire_choix_masques")
        self.verticalLayout.addWidget(self.Faire_choix_masques)
        self.Confiance_IA_radioButton = QtWidgets.QRadioButton(parent=Inserer_IRM_informations)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(11)
        self.Confiance_IA_radioButton.setFont(font)
        self.Confiance_IA_radioButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.Confiance_IA_radioButton.setObjectName("Confiance_IA_radioButton")
        self.verticalLayout.addWidget(self.Confiance_IA_radioButton)
        self.Donner_masques_radioButton = QtWidgets.QRadioButton(parent=Inserer_IRM_informations)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(11)
        self.Donner_masques_radioButton.setFont(font)
        self.Donner_masques_radioButton.setObjectName("Donner_masques_radioButton")
        self.verticalLayout.addWidget(self.Donner_masques_radioButton)
        self.Encadrer_tumeur_radioButton = QtWidgets.QRadioButton(parent=Inserer_IRM_informations)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(11)
        self.Encadrer_tumeur_radioButton.setFont(font)
        self.Encadrer_tumeur_radioButton.setObjectName("Encadrer_tumeur_radioButton")
        self.verticalLayout.addWidget(self.Encadrer_tumeur_radioButton)
        self.label = QtWidgets.QLabel(parent=Inserer_IRM_informations)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Inserer_IRM_informations)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Inserer_IRM_informations)
        self.buttonBox.accepted.connect(Inserer_IRM_informations.accept) # type: ignore
        self.buttonBox.rejected.connect(Inserer_IRM_informations.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Inserer_IRM_informations)

    def retranslateUi(self, Inserer_IRM_informations):
        _translate = QtCore.QCoreApplication.translate
        Inserer_IRM_informations.setWindowTitle(_translate("Inserer_IRM_informations", "Dialog"))
        self.IRM_nom_patient.setText(_translate("Inserer_IRM_informations", "Nom du patient concerné par ces IRM"))
        self.information_label.setText(_translate("Inserer_IRM_informations", "Le patient doit être enregistré dans la base de donnée "))
        self.Faire_choix_masques.setText(_translate("Inserer_IRM_informations", "Veuillez choisir parmi une des options suivantes pour réaliser l\'analyse"))
        self.Confiance_IA_radioButton.setText(_translate("Inserer_IRM_informations", "Laisser le modèle détecter la masse cancéreuse"))
        self.Donner_masques_radioButton.setText(_translate("Inserer_IRM_informations", "Donner votre propre masque"))
        self.Encadrer_tumeur_radioButton.setText(_translate("Inserer_IRM_informations", "Encadrer la masse cancéreuse sur une slice des IRMs"))

    # Ajouter les noms des patients dans le déroulant :
    def add_nom_patients(self, liste_noms):
        self.listePatients_comboBox.clear()
        for patient in liste_noms:
            self.listePatients_comboBox.addItem(f"{patient[1]} {patient[2]}")  # Prénom + Nom

    def get_patient_info(self):
        texte = self.listePatients_comboBox.currentText().strip()
        if texte:
            parts = texte.split(" ", 1)
            if len(parts) == 2:
                return {"nom": parts[0], "prenom": parts[1]}
            else:
                return {"nom": texte, "prenom": ""}
        else:
            return {"nom": "", "prenom": ""}

    def get_choix_ia(self):#PROPOSE PAR DEEPSEEK POUR SEGMENTATION
        return self.Confiance_IA_radioButton.isChecked()
    def get_choix_box(self):
        return self.Encadrer_tumeur_radioButton.isChecked()
    def get_choix_donner_masque(self):
        return self.Donner_masques_radioButton.isChecked()

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

    Inserer_IRM_informations = QtWidgets.QDialog()
    ui = Ui_Inserer_IRM_informations()
    ui.setupUi(Inserer_IRM_informations)
    Inserer_IRM_informations.show()
    sys.exit(app.exec())
