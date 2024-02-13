import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QListWidget, QLineEdit, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal
from PyPDF2 import PdfReader, PdfWriter

class EditableListWidget(QListWidget):
    itemsChanged = pyqtSignal()  # Signal for item changes

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            selected_items = self.selectedItems()
            for item in selected_items:
                self.takeItem(self.row(item))
            self.itemsChanged.emit()  # Emit signal on change
        else:
            super().keyPressEvent(event)

class PDFTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.output_file_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Toolkit')
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon('ic.ico'))  # Ensure this path to your icon file is correct

        layout = QVBoxLayout()

        self.file_list = EditableListWidget(self)
        self.file_list.setDragDropMode(QListWidget.InternalMove)
        self.file_list.itemsChanged.connect(self.checkListAndReset)
        layout.addWidget(self.file_list)



        self.merge_button = QPushButton('Merge PDFs', self)
        self.style_button(self.merge_button)
        self.merge_button.clicked.connect(self.merge_pdfs)
        layout.addWidget(self.merge_button)

        self.split_button = QPushButton('Split PDF', self)
        self.style_button(self.split_button)
        self.split_button.clicked.connect(self.split_pdf)
        layout.addWidget(self.split_button)

        self.prefix_input = QLineEdit(self)
        self.prefix_input.setPlaceholderText("Enter prefix for split files")
        layout.addWidget(self.prefix_input)

        self.open_button = QPushButton('Open Merged PDF', self)
        self.style_button(self.open_button)
        self.open_button.clicked.connect(self.open_merged_pdf)
        self.open_button.setEnabled(False)
        layout.addWidget(self.open_button)

        developer_label = QLabel('Developed by Dr. Ali Hayajneh', self)
        developer_label.setStyleSheet("color: gray;")
        layout.addWidget(developer_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def style_button(self, button):
        button.setFont(QFont("Arial", 10))
        button.setStyleSheet("""
            QPushButton {
                color: #fff;
                background-color: #007bff;
                border-color: #007bff;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #0069d9;
                border-color: #0062cc;
            }
            QPushButton:pressed {
                background-color: #0056b3;
                border-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                border-color: #6c757d;
            }
        """)

    def merge_pdfs(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDFs to merge", "", "PDF Files (*.pdf)")
        if files:
            self.file_list.addItems(files)
            self.merge_button.setText("Confirm Merge")
            self.merge_button.clicked.disconnect()
            self.merge_button.clicked.connect(self.perform_merge)

    def perform_merge(self):
        output_file, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF Files (*.pdf)")
        if output_file:
            self.merge_files(output_file)
            self.output_file_path = output_file
            self.open_button.setEnabled(True)

    def merge_files(self, output):
        pdf_writer = PdfWriter()
        for index in range(self.file_list.count()):
            file_path = self.file_list.item(index).text()
            pdf_reader = PdfReader(file_path)
            for page in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page])
        with open(output, 'wb') as out:
            pdf_writer.write(out)
        QMessageBox.information(self, "Success", "PDFs Merged Successfully!")
        self.file_list.clear()
        self.resetMergeButton()

    def split_pdf(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select a PDF to split", "", "PDF Files (*.pdf)")
        if file:
            output_folder = str(QFileDialog.getExistingDirectory(self, "Select Output Folder"))
            if output_folder:
                self.split_file(file, output_folder)

    def split_file(self, file, output_folder):
        prefix = self.prefix_input.text()
        pdf_reader = PdfReader(file)
        for page in range(len(pdf_reader.pages)):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page])
            output_filename = f'{output_folder}/{prefix}page_{page + 1}.pdf'
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)
        QMessageBox.information(self, "Success", "PDF Split Successfully!")

    def open_merged_pdf(self):
        if self.output_file_path and os.path.exists(self.output_file_path):
            os.startfile(self.output_file_path)
        else:
            QMessageBox.warning(self, "Error", "File not found.")

    def checkListAndReset(self):
        """Check if the list is empty and reset merge button if it is."""
        if self.file_list.count() == 0:
            self.resetMergeButton()

    def resetMergeButton(self):
        """Reset merge button to initial state."""
        self.merge_button.setText("Merge PDFs")
        self.merge_button.clicked.disconnect()
        self.merge_button.clicked.connect(self.merge_pdfs)
        self.open_button.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    ex = PDFTool()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
