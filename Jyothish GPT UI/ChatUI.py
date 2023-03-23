import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
import requests

class ChatGPT(QWidget):
    def __init__(self):
        super().__init__()

        # Create the UI elements
        self.question_label = QLabel("Enter your question:")
        self.question_input = QLineEdit()
        self.answer_label = QLabel("Answer:")
        self.answer_output = QTextEdit(readOnly=True)
        self.submit_button = QPushButton("Submit")

        # Create the layout
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        hbox1.addWidget(self.question_label)
        hbox1.addWidget(self.question_input)
        hbox2.addWidget(self.answer_label)
        hbox2.addWidget(self.answer_output)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.submit_button)

        self.setLayout(vbox)

        # Connect the button to the function that handles the API request
        self.submit_button.clicked.connect(self.get_answer)

    def get_answer(self):
        # Get the question from the input box
        question = self.question_input.text()

        # Send the question to the API
        response = requests.get('https://api.example.com/answer', params={'question': question})

        # Get the answer from the response and display it in the output box
        answer = response.json()['answer']
        self.answer_output.setText(answer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_gpt = ChatGPT()
    chat_gpt.show()
    sys.exit(app.exec_())