from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt
import ChatGPT
from database import get_connection

class Ui_Discussion_chatgpt(object):
    def setupUi(self, Discussion_chatgpt):
        self.dialog = QtWidgets.QDialog()
        Discussion_chatgpt.setObjectName("Discussion_chatgpt")
        Discussion_chatgpt.resize(976, 651)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Discussion_chatgpt.sizePolicy().hasHeightForWidth())
        Discussion_chatgpt.setSizePolicy(sizePolicy)
        self.question_docteur_plainTextEdit = QtWidgets.QPlainTextEdit(parent=Discussion_chatgpt)
        self.question_docteur_plainTextEdit.setGeometry(QtCore.QRect(10, 540, 841, 87))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light Condensed")
        font.setPointSize(11)
        #Espace de libre pour écrire sa question :
        self.question_docteur_plainTextEdit.setFont(font)
        self.question_docteur_plainTextEdit.setTabChangesFocus(False)
        self.question_docteur_plainTextEdit.setPlainText("")
        self.question_docteur_plainTextEdit.setCenterOnScroll(True)
        self.question_docteur_plainTextEdit.setObjectName("question_docteur_plainTextEdit")
        #Tableau contenant les différentes conversations (docteur et chat) (style de discussion comme par message)
        self.conversation_tableView = QtWidgets.QTableView(parent=Discussion_chatgpt)
        self.conversation_tableView.setGeometry(QtCore.QRect(15, 21, 941, 501))
        self.conversation_tableView.setObjectName("conversation_tableView")
        self.tableau = QStandardItemModel()
        self.tableau.setColumnCount(1)
        self.conversation_tableView.verticalHeader().setVisible(False)  #Masque les numéros de ligne
        self.conversation_tableView.horizontalHeader().setVisible(False)  #Masque le numéro de colonne
        self.conversation_tableView.setShowGrid(False) #Masque les lignes de la grille
        self.conversation_tableView.setStyleSheet("""
                    QTableView {
                        font-size: 13pt;
                    }
                    QTableView::item {
                        padding-left: 40px;
                        padding-bottom : 20px;
                        padding-right: 40px;
                        border-bottom: 1px solid
                    }
                    QTableView::item:selected {
                        background: transparent;
                    }
                """)
        self.conversation_tableView.setWordWrap(True)  # Activation du retour à la ligne
        self.conversation_tableView.horizontalHeader().setStretchLastSection(True)  # Étirement de la colonne
        self.conversation_tableView.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents) # Ajustement automatique de la hauteur
        # Bouton envoyer pour envoyer le message
        self.envoyer_message_pushButton = QtWidgets.QPushButton(parent=Discussion_chatgpt)
        self.envoyer_message_pushButton.setGeometry(QtCore.QRect(860, 550, 93, 61))
        self.envoyer_message_pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../Downloads/message.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.envoyer_message_pushButton.setIcon(icon)
        self.envoyer_message_pushButton.setIconSize(QtCore.QSize(40, 40))
        self.envoyer_message_pushButton.setObjectName("envoyer_message_pushButton")
        self.envoyer_message_pushButton.clicked.connect(lambda: self.mettre_dans_tableau())
        self.conversation_tableView.setItemDelegate(QStyledItemDelegate(self.conversation_tableView))
        self.conversation_tableView.setWordWrap(True)
        self.conversation_tableView.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.retranslateUi(Discussion_chatgpt)
        QtCore.QMetaObject.connectSlotsByName(Discussion_chatgpt)

    def retranslateUi(self, Discussion_chatgpt):
        _translate = QtCore.QCoreApplication.translate
        Discussion_chatgpt.setWindowTitle(_translate("Discussion_chatgpt", "Discussion avec OpenAI"))
        self.question_docteur_plainTextEdit.setPlaceholderText(_translate("Discussion_chatgpt", "Veuillez poser une question de façon clair et précise, avec tous les détails recquis, afin de recevoir une réponse plus complète et précise....."))

    def mettre_dans_tableau(self):
        texte = self.question_docteur_plainTextEdit.toPlainText()
        if texte :
            item = QStandardItem(texte)
            item.setData(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, Qt.ItemDataRole.TextAlignmentRole)
            self.tableau.appendRow(item)
            self.conversation_tableView.setModel(self.tableau)
            self.conversation_tableView.resizeRowsToContents()
            self.question_docteur_plainTextEdit.clear()
            self.envoyer_message_pushButton.setEnabled(False)
            self.repondre_au_message(texte)

    def get_data_patient(self, niss_patient):
        self.niss = niss_patient

    def repondre_au_message(self,question):
        texte = ChatGPT.generate_faculty_response(question,self.niss)
        item = QStandardItem(texte)
        item.setData(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, Qt.ItemDataRole.TextAlignmentRole)
        self.tableau.appendRow(item)
        self.conversation_tableView.setModel(self.tableau)
        self.conversation_tableView.resizeRowsToContents()
        self.envoyer_message_pushButton.setEnabled(True)
        self.enregistrer_conversation(question,texte)

    def enregistrer_conversation(self,question, reponse):
        conn = None
        cursor = None
        contenu = f"Question : {question}\n Reponse : {reponse}"
        niss_patient = self.niss
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Utilisation du même nom de colonnes que dans le CREATE TABLE
            cursor.execute(
                "INSERT INTO Discussion (Contenu_discussion, NISS) VALUES (%s, %s)",
                (contenu, niss_patient)
            )
            conn.commit()

            # Message avec parent explicite
            QtWidgets.QMessageBox.information(
                self.dialog,
                "Success",
                "Conversation enregistrée avec succès!"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.dialog,
                "Erreur inattendue",
                f"Erreur : {str(e)}"
            )



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Discussion_chatgpt = QtWidgets.QWidget()
    ui = Ui_Discussion_chatgpt()
    ui.setupUi(Discussion_chatgpt)
    Discussion_chatgpt.show()
    sys.exit(app.exec())
