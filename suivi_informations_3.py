from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import pandas as pd
import gdown
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
from database import get_connection
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import mysql.connector
from PyQt6.QtWidgets import QMessageBox
matplotlib.use('Agg')  # Désactive l'affichage interactif

class Ui_suivi_fenetre(object):
    def setupUi(self, suivi_fenetre):
        suivi_fenetre.setObjectName("suivi_fenetre")
        suivi_fenetre.setStyleSheet("""
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
                                border: 1px solid #b6c7cf;
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
        suivi_fenetre.resize(1209, 705)
        self.file_to_process = None
        self.niss_patient = None
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(suivi_fenetre.sizePolicy().hasHeightForWidth())
        suivi_fenetre.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(suivi_fenetre)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.graphique2 = QtWidgets.QWidget(parent=suivi_fenetre)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphique2.sizePolicy().hasHeightForWidth())
        self.graphique2.setSizePolicy(sizePolicy)
        self.graphique2.setObjectName("graphique2")
        self.lineEdit_graph3 = QtWidgets.QLineEdit(parent=self.graphique2)
        self.lineEdit_graph3.setGeometry(QtCore.QRect(60, 10, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        font.setItalic(False)
        self.lineEdit_graph3.setFont(font)
        self.lineEdit_graph3.setStyleSheet("background-color: #c5e8ed;")
        self.lineEdit_graph3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_graph3.setReadOnly(True)
        self.lineEdit_graph3.setObjectName("lineEdit_graph3")
        self.gridLayout_2.addWidget(self.graphique2, 1, 0, 1, 1)
        self.graphique1 = QtWidgets.QWidget(parent=suivi_fenetre)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphique1.sizePolicy().hasHeightForWidth())
        self.graphique1.setSizePolicy(sizePolicy)
        self.graphique1.setStyleSheet("")
        self.graphique1.setObjectName("graphique1")
        self.lineEdit_graph1 = QtWidgets.QLineEdit(parent=self.graphique1)
        self.lineEdit_graph1.setGeometry(QtCore.QRect(50, 10, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        font.setItalic(False)
        self.lineEdit_graph1.setFont(font)
        self.lineEdit_graph1.setStyleSheet("background-color: #c5e8ed;")
        self.lineEdit_graph1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_graph1.setReadOnly(True)
        self.lineEdit_graph1.setObjectName("lineEdit_graph1")
        self.gridLayout_2.addWidget(self.graphique1, 0, 0, 1, 1)
        self.widget_chack_superposition = QtWidgets.QWidget(parent=suivi_fenetre)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_chack_superposition.sizePolicy().hasHeightForWidth())
        self.widget_chack_superposition.setSizePolicy(sizePolicy)
        self.widget_chack_superposition.setStyleSheet("background-color: #c5e8ed;")
        self.widget_chack_superposition.setObjectName("widget_chack_superposition")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_chack_superposition)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_2 = QtWidgets.QCheckBox(parent=self.widget_chack_superposition)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 4, 0, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(parent=self.widget_chack_superposition)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout.addWidget(self.checkBox_4, 5, 0, 1, 1)
        self.checkBox_1 = QtWidgets.QCheckBox(parent=self.widget_chack_superposition)
        self.checkBox_1.setObjectName("checkBox_1")
        self.gridLayout.addWidget(self.checkBox_1, 2, 0, 1, 1)
        self.Titre_superposition = QtWidgets.QLineEdit(parent=self.widget_chack_superposition)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Titre_superposition.setFont(font)
        self.Titre_superposition.setStyleSheet("background-color: #c5e8ed;")
        self.Titre_superposition.setInputMask("")
        self.Titre_superposition.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Titre_superposition.setReadOnly(True)
        self.Titre_superposition.setObjectName("Titre_superposition")
        self.gridLayout.addWidget(self.Titre_superposition, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget_chack_superposition, 1, 2, 1, 1)
        self.graphique5_superposition = QtWidgets.QWidget(parent=suivi_fenetre)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphique5_superposition.sizePolicy().hasHeightForWidth())
        self.graphique5_superposition.setSizePolicy(sizePolicy)
        self.graphique5_superposition.setObjectName("graphique5_superposition")
        self.lineEdit_graph5_superposes = QtWidgets.QLineEdit(parent=self.graphique5_superposition)
        self.lineEdit_graph5_superposes.setGeometry(QtCore.QRect(50, 10, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        font.setItalic(False)
        self.lineEdit_graph5_superposes.setFont(font)
        self.lineEdit_graph5_superposes.setStyleSheet("background-color: #c5e8ed;")
        self.lineEdit_graph5_superposes.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_graph5_superposes.setReadOnly(True)
        self.lineEdit_graph5_superposes.setObjectName("lineEdit_graph5_superposes")
        self.gridLayout_2.addWidget(self.graphique5_superposition, 1, 1, 1, 1)
        self.graphique3 = QtWidgets.QWidget(parent=suivi_fenetre)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphique3.sizePolicy().hasHeightForWidth())
        self.graphique3.setSizePolicy(sizePolicy)
        self.graphique3.setStyleSheet("")
        self.graphique3.setObjectName("graphique3")
        self.lineEdit_graph2 = QtWidgets.QLineEdit(parent=self.graphique3)
        self.lineEdit_graph2.setGeometry(QtCore.QRect(50, 10, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        font.setItalic(False)
        self.lineEdit_graph2.setFont(font)
        self.lineEdit_graph2.setStyleSheet("background-color: #c5e8ed;")
        self.lineEdit_graph2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_graph2.setReadOnly(True)
        self.lineEdit_graph2.setObjectName("lineEdit_graph2")
        self.gridLayout_2.addWidget(self.graphique3, 0, 1, 1, 1)
        self.widget = QtWidgets.QWidget(parent=suivi_fenetre)
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Titre_resultat_MLD = QtWidgets.QLineEdit(parent=self.widget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Titre_resultat_MLD.setFont(font)
        self.Titre_resultat_MLD.setStyleSheet("background-color: #c5e8ed;")
        self.Titre_resultat_MLD.setInputMask("")
        self.Titre_resultat_MLD.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Titre_resultat_MLD.setReadOnly(True)
        self.Titre_resultat_MLD.setObjectName("Titre_resultat_MLD")
        self.Titre_resultat_MLD.setFixedHeight(50)
        self.gridLayout_3.addWidget(self.Titre_resultat_MLD, 0, 0, 1, 1)
        self.label_reponse_MLD = QtWidgets.QLabel(parent=self.widget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(10)
        self.label_reponse_MLD.setFont(font)
        self.label_reponse_MLD.setText("")
        self.label_reponse_MLD.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_reponse_MLD.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.NoTextInteraction)
        self.label_reponse_MLD.setObjectName("label_reponse_MLD")
        self.gridLayout_3.addWidget(self.label_reponse_MLD, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget, 0, 2, 1, 1)

        self.graphique1.setMinimumSize(300, 200)
        self.graphique2.setMinimumSize(300, 200)
        self.graphique3.setMinimumSize(300, 200)
        self.graphique5_superposition.setMinimumSize(400, 300)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        for widget in [self.graphique1, self.graphique2, self.graphique3, self.graphique5_superposition]:
            widget.setSizePolicy(size_policy)
        suivi_fenetre.updateGeometry()

        self.retranslateUi(suivi_fenetre)
        QtCore.QMetaObject.connectSlotsByName(suivi_fenetre)
        self._connect_checkboxes()

    def retranslateUi(self, suivi_fenetre):
        _translate = QtCore.QCoreApplication.translate
        suivi_fenetre.setWindowTitle(_translate("suivi_fenetre", "Form"))
        self.lineEdit_graph3.setText(_translate("suivi_fenetre", "Graphique 3"))
        self.lineEdit_graph1.setText(_translate("suivi_fenetre", "Graphique 1"))
        self.checkBox_2.setText(_translate("suivi_fenetre", "Graphique 2"))
        self.checkBox_4.setText(_translate("suivi_fenetre", "Graphique 3"))
        self.checkBox_1.setText(_translate("suivi_fenetre", "Graphique 1"))
        self.Titre_superposition.setText(_translate("suivi_fenetre", "Superposition des graphiques"))
        self.lineEdit_graph5_superposes.setText(_translate("suivi_fenetre", "Graphiques superposés"))
        self.lineEdit_graph2.setText(_translate("suivi_fenetre", "Graphique 2"))
        self.Titre_resultat_MLD.setText(_translate("suivi_fenetre", "Résultat sur le traitement"))

    def _add_graphs(self):
        funcs = [self.get_sphericite_graphique,
                 self.get_evolution_taille_tumeur,
                 self.get_evolution_surface_tumeur]
        widgets = [self.graphique1, self.graphique2, self.graphique3]
        for widget, fn in zip(widgets, funcs):
            # Nettoyer toute ancienne figure
            for ch in widget.children():
                if isinstance(ch, QtWidgets.QWidget) and not isinstance(ch, QtWidgets.QLineEdit):
                    ch.deleteLater()
            layout = QtWidgets.QVBoxLayout(widget)
            layout.setContentsMargins(0, 40, 0, 0)
            canvas = FigureCanvas(plt.Figure())
            layout.addWidget(canvas)
            fig = canvas.figure
            fig.subplots_adjust(
                left=0.15,  # Plus d'espace pour l'axe Y
                right=0.85,
                bottom=0.25,  # Plus d'espace pour l'axe X
                top=0.9
            )
            fig = canvas.figure
            ax = fig.add_subplot(111)
            layout = QtWidgets.QVBoxLayout(widget)
            layout.setContentsMargins(20, 50, 20, 20)
            # Appel de la fonction de tracé sur ax
            fn(self.file_to_process, self.niss_patient, fig=fig, ax=ax)
            canvas.draw()

    def _connect_checkboxes(self):
        #Connecte les checkboxes à la mise à jour
        checkboxes = [self.checkBox_1, self.checkBox_2, self.checkBox_4]
        for cb in checkboxes:
            cb.stateChanged.connect(self._update_superposition)

    
    def _update_superposition(self):
        widget = self.graphique5_superposition
        # Supprimer anciens FigureCanvas
        for child in widget.children():
            if isinstance(child, FigureCanvas):
                child.deleteLater()
        # Créer (ou récupérer) layout
        if widget.layout():
            layout = widget.layout()
        else:
            layout = QtWidgets.QVBoxLayout(widget)
            layout.setContentsMargins(0, 40, 0, 0)
        # Nouvel canvas
        canvas = FigureCanvas(plt.Figure())
        layout.addWidget(canvas)
        fig = canvas.figure
        ax = fig.add_subplot(111)
        fig.subplots_adjust(left=0.15, right=0.85)  # Plus d'espace à gauche
        ax.set_ylabel("Superposition", fontsize=10)
        # Replot selon checkboxes
        mapping = [
            (self.checkBox_1, self.get_sphericite_graphique),
            (self.checkBox_2, self.get_evolution_surface_tumeur),
            (self.checkBox_4, self.get_evolution_taille_tumeur)
        ]
        for cb, fn in mapping:
            if cb.isChecked():
                fn(self.file_to_process, self.niss_patient, fig=fig, ax=ax)
        ax.set_title("Superposition des graphiques")
        ax.legend(fontsize=6)
        ax.grid(True, linestyle='--', alpha=0.5)
        fig.autofmt_xdate()
        canvas.draw()

    def get_direct_download_url(self,gdrive_url):  # Extraction des ID de fichier Google Drive et construction d'une URL de téléchargement directe
        match = re.search(r"/d/([\w-]+)", gdrive_url)
        if not match:
            raise ValueError(f"Impossible d'extraire l'ID depuis: {gdrive_url}")
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    def cleanup_temp(self,dir_path):
        if os.path.exists(dir_path):
            for f in os.listdir(dir_path):
                os.remove(os.path.join(dir_path, f))
            os.rmdir(dir_path)
        else:
            print(f"Dossier {dir_path} non trouvé.")


    def check_patient_has_multiple_irms(self, niss_patient):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Chemin_csv 
                FROM Caracteristiques_IRM 
                WHERE NISS = %s 
            """, (niss_patient,))
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            print(f"Erreur vérification IRMs : {str(e)}")
            return False


    def get_sphericite_graphique(self, todos_fichier_csv_path, niss_patient, fig=None, ax=None):
        # Chargement et preprocessing inchangés...
        df = pd.read_csv(todos_fichier_csv_path)
        df['Date_IRM'] = pd.to_datetime(df['Date_IRM'])
        df_sph = df[df['Feature'].str.contains('Sphericity', case=False, na=False)]

        # Crée fig/ax si non fournis :
        if fig is None or ax is None:
            """
            fig = plt.Figure(figsize=(6, 4))
            ax  = fig.add_subplot(111)"""
            fig, ax = plt.subplots()

            # Trace chaque patient sur ax au lieu de plt :
        colors = sns.color_palette("Set2", len(df_sph['Patient_ID'].unique()))
        for i, (pid, grp) in enumerate(df_sph.groupby('Patient_ID')):
            g = grp.sort_values('Date_IRM')
            ax.plot(g['Date_IRM'], g['Value'], marker='o', linestyle='-', markersize=4,
                    label=f"Patient {pid}", color=colors[i], alpha=0.8)
            for x, y in zip(g['Date_IRM'], g['Value']):
                ax.text(x, y, f"{y:.2f}", fontsize=7, va='bottom', ha='right')

        # Moyenne + IC 95% sur ax :
        summary = df_sph.groupby('Date_IRM')['Value'].agg(['mean', 'count', 'std']).reset_index()
        summary['sem'] = summary['std'] / summary['count']**0.5
        summary['ci95_lo'] = summary['mean'] - 1.96 * summary['sem']
        summary['ci95_hi'] = summary['mean'] + 1.96 * summary['sem']
        ax.plot(summary['Date_IRM'], summary['mean'], linewidth=2, label='Moyenne', zorder=5)
        ax.fill_between(summary['Date_IRM'], summary['ci95_lo'], summary['ci95_hi'], alpha=0.3)

        # Titres, legendes et format date :
        ax.set_title("Évolution sphéricité", fontsize=12)
        ax.set_xlabel("Date", fontsize=12, labelpad=10)
        ax.set_ylabel("Sphericité", fontsize=12, labelpad=15)
        fig.autofmt_xdate()
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(fontsize=6)
        ax.tick_params(axis='y', labelsize=10)
        ax.tick_params(axis='x', labelsize=10, rotation=45)
        fig.subplots_adjust(bottom=0.25)
        return fig, ax

    def get_evolution_taille_tumeur(self, tous_fichier_csv_path, niss_patient, fig=None, ax=None):
        df = pd.read_csv(tous_fichier_csv_path)
        df['Date_IRM'] = pd.to_datetime(df['Date_IRM'])
        df_axis = df[df['Feature'].str.contains('Elongation', case=False, na=False)]
        # Conversion des valeurs de Elongation de pixels à centimètres
        conversion_factor = 0.0703125  # 1 pixel = 0.0703125 cm
        df_axis['Value_cm'] = df_axis['Value'] * conversion_factor  # Conversion en cm
        df_axis['Value_cm'] = df_axis['Value'] * 0.0703125

        if fig is None or ax is None:
            fig, ax = plt.subplots()
        colors = sns.color_palette("Set2", len(df_axis['Patient_ID'].unique()))
        for i, (pid, grp) in enumerate(df_axis.groupby('Patient_ID')):
            g = grp.sort_values('Date_IRM')
            ax.plot(g['Date_IRM'], g['Value_cm'], marker='o', linestyle='-', markersize=4,
                    label=f"Patient {pid}", color=colors[i], alpha=0.8)
            for x, y in zip(g['Date_IRM'], g['Value_cm']):
                ax.text(x, y, f"{y:.1f}", fontsize=7, va='bottom', ha='right')
        summary = df_axis.groupby('Date_IRM')['Value_cm'].agg(['mean','count','std']).reset_index()
        summary['sem'] = summary['std'] / summary['count']**0.5
        summary['ci95_lo'] = summary['mean'] - 1.96 * summary['sem']
        summary['ci95_hi'] = summary['mean'] + 1.96 * summary['sem']
        ax.plot(summary['Date_IRM'], summary['mean'], linewidth=2)
        ax.fill_between(summary['Date_IRM'], summary['ci95_lo'], summary['ci95_hi'], alpha=0.3)
        ax.set_title("Taille tumeur (cm)")
        ax.set_xlabel("Date", fontsize=12, labelpad=10)
        ax.set_ylabel("Longueur axe principal (cm)")
        fig.autofmt_xdate()
        ax.tick_params(axis='x', labelsize=10, rotation=45)
        fig.subplots_adjust(bottom=0.25)
        ax.grid(True)
        return fig, ax

    def get_evolution_surface_tumeur(self, tous_fichier_csv_path, niss_patient, fig=None, ax=None):
        df = pd.read_csv(tous_fichier_csv_path)
        df['Date_IRM'] = pd.to_datetime(df['Date_IRM'])
        df_surface = df[df['Feature'].str.contains('PixelSurface', case=False, na=False)]
        df_surface['Value_cm2'] = df_surface['Value'] * 0.0049305

        if fig is None or ax is None:
            fig, ax = plt.subplots()
        colors = sns.color_palette("Set2", len(df_surface['Patient_ID'].unique()))
        for i, (pid, grp) in enumerate(df_surface.groupby('Patient_ID')):
            g = grp.sort_values('Date_IRM')
            ax.plot(g['Date_IRM'], g['Value_cm2'], marker='o', linestyle='-', markersize=4,
                    label=f"Patient {pid}", color=colors[i], alpha=0.8)
            for x, y in zip(g['Date_IRM'], g['Value_cm2']):
                ax.text(x, y, f"{y:.1f}", fontsize=7, va='bottom', ha='right')
        summary = df_surface.groupby('Date_IRM')['Value_cm2'].agg(['mean','count','std']).reset_index()
        summary['sem'] = summary['std'] / summary['count']**0.5
        summary['ci95_lo'] = summary['mean'] - 1.96 * summary['sem']
        summary['ci95_hi'] = summary['mean'] + 1.96 * summary['sem']
        ax.plot(summary['Date_IRM'], summary['mean'], linewidth=2)
        ax.fill_between(summary['Date_IRM'], summary['ci95_lo'], summary['ci95_hi'], alpha=0.3)
        ax.set_title("Surface tumeur (cm²)")
        ax.set_xlabel("Date", fontsize=12, labelpad=10)
        ax.set_ylabel("Surface (cm²)")
        fig.autofmt_xdate()
        ax.grid(True)
        ax.tick_params(axis='x', labelsize=10, rotation=45)
        fig.subplots_adjust(bottom=0.25)
        return fig, ax

    def merge_all_csv(self,niss_patient):
        gdrive_links = self.check_patient_has_multiple_irms(niss_patient)
        if not gdrive_links:
            print("Aucun fichier CSV trouvé pour ce patient.")
            return
        download_dir = 'temp_csvs'
        os.makedirs(download_dir, exist_ok=True)
        dataframes = []
        downloaded_paths = []
        for idx, url in enumerate(gdrive_links, start=1):
            try:
                direct_url = self.get_direct_download_url(url)
                output_path = os.path.join(download_dir, f"file_{idx}.csv")
                print(f"Téléchargement de {url} -> {output_path}")
                gdown.download(direct_url, output_path, quiet=False)
                df = pd.read_csv(output_path)
                dataframes.append(df)
                downloaded_paths.append(output_path)
            except Exception as e:
                print(f"Erreur lors du traitement de {url}: {e}")
        # Choisir le fichier à traiter (fusionné ou unique)
        if len(dataframes) >= 1:
            if len(dataframes)>1:
                merged_df = pd.concat(dataframes, axis=0, ignore_index=True, sort=False)
                output_file = 'merged_output.csv'
                merged_df.to_csv(output_file, index=False)
                file_to_process = output_file
                print(f"Fichier fusionné enregistré sous: {output_file}")
            else:
                file_to_process = downloaded_paths[0]
                print(f"Un seul fichier trouvé, utilisation de : {file_to_process}")
        else:
            print("Aucun CSV valide pour générer les graphiques")
            self.label_reponse_MLD.setText("Données insuffisantes")
            return
        # Génération des graphiques
        self.get_sphericite_graphique(file_to_process, niss_patient)
        self.get_evolution_taille_tumeur(file_to_process, niss_patient)
        self.get_evolution_surface_tumeur(file_to_process, niss_patient)
        self.file_to_process = file_to_process

    def set_patient_data(self, niss_patient):
        self.niss_patient = niss_patient
        self.merge_all_csv(niss_patient)  # Appel de la fusion des CSV
        self._add_graphs()
        self.get_result_mlp()

    def get_result_mlp(self):
        model = QStandardItemModel()
        model.setColumnCount(1)  # nombre de colonnes
        model.setHorizontalHeaderLabels(['Prédiction sur l\'efficacité du modèle'])
        niss_patient = self.niss_patient
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT Résultat_Suivi FROM Patient WHERE NISS = %s",
                (niss_patient,)
            )
            row = cursor.fetchone()
            resultat_suivi = row[0]
            if resultat_suivi == -1:
                self.label_reponse_MLD.setText("Pas assez de date pour avoir un résultat sur le traitement")
            elif resultat_suivi == 0:
                self.label_reponse_MLD.setText("La patiente réagit négativement au traitement")
            else :
                self.label_reponse_MLD.setText("La patiente réagit positivement au traitement")
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(None,"Erreur DB",f"Erreur lors du chargement du résultat suivi pour le patient : {e}")






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    suivi_fenetre = QtWidgets.QWidget()
    ui = Ui_suivi_fenetre()
    ui.setupUi(suivi_fenetre)
    suivi_fenetre.show()
    sys.exit(app.exec())
