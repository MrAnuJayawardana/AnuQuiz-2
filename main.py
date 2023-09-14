from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton,QLabel,QFileDialog,QMessageBox,QInputDialog, QSpinBox,QRadioButton
from PyQt5 import uic
import os
import pickle

class IncorrectQuestion:
    def __init__(self,question,answer,guess):
        self.question = question
        self.answer = answer
        self.guess = guess

class QuizItem:
    def __init__(self,question,answerNumber,a1,a2,a3,a4):
        self.question = question
        self.answerNumber = answerNumber
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show_menu()
        self.creator = False

    def update_ui_creator(self):
        self.questionIndex.setText(f"AnuQuiz Creator - Question {self.question_index + 1} out of {len(self.questions)}")
        self.questionLabel.setText(self.questions[self.question_index].question)
        
        self.a1Label.setText(self.questions[self.question_index].a1)
        self.a2Label.setText(self.questions[self.question_index].a2)
        self.a3Label.setText(self.questions[self.question_index].a3)
        self.a4Label.setText(self.questions[self.question_index].a4)

        self.exportButton.setEnabled(self.question_index == len(self.questions) - 1)
        self.nextButton.setEnabled(self.question_index < len(self.questions) - 1)
        self.backButton.setEnabled(self.question_index > 0)
        self.deleteButton.setEnabled(len(self.questions) > 1)
        self.answerSpinbox.setValue(self.questions[self.question_index].answerNumber)

    def update_ui_student(self):
        self.questionIndex.setText(f"AnuQuiz Creator - Question {self.question_index + 1} out of {len(self.questions)}")
        self.questionLabel.setText(self.questions[self.question_index].question)
        
        self.a1Button.setText(self.questions[self.question_index].a1)
        self.a2Button.setText(self.questions[self.question_index].a2)
        self.a3Button.setText(self.questions[self.question_index].a3)
        self.a4Button.setText(self.questions[self.question_index].a4)

        self.nextButton.setEnabled(self.question_index < len(self.questions) - 1)
        self.backButton.setEnabled(self.question_index > 0)
        
        self.a1Button.setChecked(False)
        self.a2Button.setChecked(False)
        self.a3Button.setChecked(False)
        self.a4Button.setChecked(False)

    def export_quiz(self):
        self.questions[len(self.questions) - 1].answerNumber = int(self.answerSpinbox.text())
        dictionary = {}
        for question in self.questions:
            dictionary[question.question] = [question.answerNumber,question.a1,question.a2,question.a3,question.a4]

        filedialog = QFileDialog.getSaveFileName(parent=self,caption="Export Quiz",directory=os.getcwd(),filter="AnuQuiz Files (*.anuquiz)")
        try:
            if len(filedialog[0]) > 0:
                with open(filedialog[0],"wb") as file:
                    pickle.dump(dictionary,file)
        except Exception as e:
            mb = QMessageBox(parent=self)
            mb.setWindowTitle("Error Occured")
            mb.setText(str(e))
            mb.setIcon(QMessageBox.Critical)
            mb.exec_()

    def new_question(self):
        self.questions.append(QuizItem("New Question",1,"Answer 1","Answer 2","Answer 3","Answer 4"))
        self.update_ui_creator()

    def delete_question(self):
        deleted_answer = self.question_index
        if self.question_index == len(self.questions) - 1:
            self.back_question()
        elif self.question_index == 0:
            self.next_question()
        self.questions.remove(self.questions[deleted_answer])
        self.update_ui_creator()

    def edit_question(self):
        new_title = self.get_user_string("Edit Question","Enter new Question",self.questionLabel.text());
        self.questionLabel.setText(new_title)
        self.questions[self.question_index].question = new_title;

    def get_user_string(self,title,caption,original_string) -> str:
        answer,ok = QInputDialog.getText(self,title,caption);
        if len(answer) > 0:
            return answer
        else:
            return original_string
    def register_answer(self,number):
        self.choices[self.question_index] = number
    def next_question(self):
        if self.creator:
            self.questions[self.question_index].answerNumber = int(self.answerSpinbox.text())
        self.question_index += 1
        if self.creator:
            self.update_ui_creator()
        else:
            self.update_ui_student()
    def back_question(self):
        self.question_index -= 1
        if self.creator:
            self.update_ui_creator()
        else:
            self.update_ui_student()
    def edit_a1(self):
        string = self.get_user_string("Edit Answer","Enter New Answer",self.a1Label.text());
        self.a1Label.setText(string)
        self.questions[self.question_index].a1 = string
    def edit_a2(self):
        string = self.get_user_string("Edit Answer","Enter New Answer",self.a2Label.text());
        self.a2Label.setText(string)
        self.questions[self.question_index].a2 = string
    def edit_a3(self):
        string = self.get_user_string("Edit Answer","Enter New Answer",self.a3Label.text());
        self.a3Label.setText(string)
        self.questions[self.question_index].a3 = string
    def edit_a4(self):
        string = self.get_user_string("Edit Answer","Enter New Answer",self.a4Label.text());
        self.a4Label.setText(string)
        self.questions[self.question_index].a4 = string
    def load_creator(self):
        self.creator = True
        uic.loadUi("data/creator.ui",self)
        self.questions = []
        self.question_index = 0
        self.questions.append(QuizItem("Demo Question",1,"Answer 1","Answer 2","Answer 3","Answer 4"))

        self.questionEdit = self.findChild(QPushButton,"questionEdit")

        self.questionIndex = self.findChild(QLabel,"questionIndex")
        self.questionLabel = self.findChild(QLabel,"questionLabel")
        self.a1Label = self.findChild(QLabel,"a1Label")
        self.a2Label = self.findChild(QLabel,"a2Label")
        self.a3Label = self.findChild(QLabel,"a3Label")
        self.a4Label = self.findChild(QLabel,"a4Label")

        self.a1Edit = self.findChild(QPushButton,"a1Edit")
        self.a2Edit = self.findChild(QPushButton,"a2Edit")
        self.a3Edit = self.findChild(QPushButton,"a3Edit")
        self.a4Edit = self.findChild(QPushButton,"a4Edit")      

        self.answerSpinbox = self.findChild(QSpinBox,"answerSpinbox")  

        self.newButton = self.findChild(QPushButton,"newButton")
        self.menuButton = self.findChild(QPushButton,"menuButton")
        self.exportButton = self.findChild(QPushButton,"exportButton")

        self.backButton = self.findChild(QPushButton,"backButton")
        self.nextButton = self.findChild(QPushButton,"nextButton")
        self.deleteButton = self.findChild(QPushButton,"deleteButton")

        self.questionEdit.clicked.connect(self.edit_question)
        self.a1Edit.clicked.connect(self.edit_a1);
        self.a2Edit.clicked.connect(self.edit_a2);
        self.a3Edit.clicked.connect(self.edit_a3);
        self.a4Edit.clicked.connect(self.edit_a4);

        self.menuButton.clicked.connect(self.show_menu)
        self.newButton.clicked.connect(self.new_question)
        self.deleteButton.clicked.connect(self.delete_question)
        self.exportButton.clicked.connect(self.export_quiz)
        self.nextButton.clicked.connect(self.next_question)
        self.backButton.clicked.connect(self.back_question)

        self.update_ui_creator()
        
    def load_student(self):
        self.creator = False
        self.questions = []
        self.question_index = 0
        self.choices = []
        self.question_index = 0

        filedialog = QFileDialog.getOpenFileName(parent=self,caption="Open Quiz",directory=os.getcwd(),filter="AnuQuiz (*.anuquiz)")
        if len(filedialog[0]) <= 0:
            self.show_menu()

        dictionary = {}
        try:
            with open(filedialog[0],"rb") as file:
                dictionary = pickle.load(file)
            values = []
            keys = []
            for k in dictionary.keys():
                keys.append(k)
            for val in dictionary.values():
                values.append(val)
            for i in range(len(keys)):
                question = keys[i]
                answerNumber = values[i][0]
                a1 = values[i][1]
                a2 = values[i][2]
                a3 = values[i][3]
                a4 = values[i][4]
                q = QuizItem(question,answerNumber,a1,a2,a3,a4)
                self.questions.append(q)
                self.choices.append(1)
        except Exception as e:
            mb = QMessageBox(parent=self)
            mb.setWindowTitle("Error Occured")
            mb.setText(str(e))
            mb.setIcon(QMessageBox.Critical)
            mb.exec_()
            return

        uic.loadUi("data/student.ui",self)
        self.backButton = self.findChild(QPushButton,"backButton")
        self.nextButton = self.findChild(QPushButton,"nextButton")
        self.submitButton = self.findChild(QPushButton,"submitButton")
        self.menuButton = self.findChild(QPushButton,"menuButton")

        self.a1Button = self.findChild(QRadioButton,"a1Button")
        self.a2Button = self.findChild(QRadioButton,"a2Button")
        self.a3Button = self.findChild(QRadioButton,"a3Button")
        self.a4Button = self.findChild(QRadioButton,"a4Button")

        self.a1Button.clicked.connect(lambda : self.register_answer(1))
        self.a2Button.clicked.connect(lambda : self.register_answer(2))
        self.a3Button.clicked.connect(lambda : self.register_answer(3))
        self.a4Button.clicked.connect(lambda : self.register_answer(4))

        self.nextButton.clicked.connect(self.next_question)
        self.backButton.clicked.connect(self.back_question)
        self.submitButton.clicked.connect(self.submit_quiz)
        self.menuButton.clicked.connect(self.show_menu)

        self.update_ui_student()

    def choose_question_by_number(self,q,n):
        if(n == 1): return q.a1
        if(n == 2): return q.a2
        if(n == 3): return q.a3
        if(n == 4): return q.a4
    
    def submit_quiz(self):
        score = 0
        incorrect = []
        for i in range(len(self.questions)):
            if self.questions[i].answerNumber == self.choices[i]:
                score += 1
            else:
                incorrect.append(IncorrectQuestion(self.questions[i].question,self.choose_question_by_number(self.questions[i],self.questions[i].answerNumber),self.choose_question_by_number(self.questions[i],self.choices[i])))
        percentage = int((score/len(self.questions)) * 100)
        uic.loadUi("data/results.ui",self)
        self.scoreText = self.findChild(QLabel,"scoreText")
        self.correctionLabel = self.findChild(QLabel,"correctionLabel")
        self.okButton = self.findChild(QPushButton,"okButton")
        self.scoreText.setText(f"You scored {percentage}%")
        
        if len(incorrect) == 0:
            self.correctionLabel.setText("Incorrect Questions : None")
        else:
            string = "Incorrect Questions:\n"
            for inc in incorrect:
                string += f"- For question '{inc.question}', got '{inc.guess}' instead of '{inc.answer}'"
            self.correctionLabel.setText(string)
        self.okButton.clicked.connect(self.show_menu)

    def show_menu(self):
        uic.loadUi("data/gui.ui",self)

        self.createButton = self.findChild(QPushButton,"createQuizButton")
        self.answerButton = self.findChild(QPushButton,"answerQuizButton")
        self.quitButton = self.findChild(QPushButton,"quitButton")

        self.createButton.clicked.connect(self.load_creator)
        self.answerButton.clicked.connect(self.load_student)
        self.quitButton.clicked.connect(self.close)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()