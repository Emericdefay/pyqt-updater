import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton

class DumpApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create GUI elements
        self.text_edit = QTextEdit()
        self.dump_button = QPushButton('Dump')
        self.output_label = QLabel()
        self.output_label.setWordWrap(True)
        
        # Add elements to layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Enter text to dump:'))
        layout.addWidget(self.text_edit)
        layout.addWidget(self.dump_button)
        layout.addWidget(QLabel('Dumped text:'))
        layout.addWidget(self.output_label)
        
        # Set layout and connect button to function
        self.setLayout(layout)
        self.dump_button.clicked.connect(self.dump_text)
        
        # Set window properties
        self.setWindowTitle('Dump App')
        self.setGeometry(100, 100, 400, 300)
        
    def dump_text(self):
        # Get text from text edit and display in output label
        self.output_label.setText(self.text_edit.toPlainText())
        
if __name__ == '__main__':
    # Create application and show window
    app = QApplication(sys.argv)
    window = DumpApp()
    window.show()
    sys.exit(app.exec_())