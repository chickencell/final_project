import csv
from gui import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QIntValidator


class Logic(QMainWindow, Ui_MainWindow):
    """
    Handles all the functions of the file.
    """

    def __init__(self) -> None:
        """
        Sets up the user interface.
        """
        super().__init__()
        self.setupUi(self)

        # Private attribute with double underscores
        self.__label_message: QLabel = self.label_message
        self.__label_message.hide()

        # Connect the button to a private method with double underscores
        self.button_vote.clicked.connect(self.__vote)

    def __vote(self) -> None:
        """
        Handles the voting process, validates input, and updates the message label.
        """
        voter_id: str = self.box_ID.text()
        selected_vote: str = ""

        # Check if the voter_id length is exactly 9 characters
        if len(voter_id) != 9:
            self.__label_message.setText("ID must be exactly 9 characters.")
            self.__label_message.setStyleSheet("color: red; font-size: 18pt;")
            self.__label_message.show()
            return

        try:
            # Validate that voter_id is a number
            int(voter_id)

            if self.radio_jane.isChecked():
                selected_vote = "Jane"
            elif self.radio_john.isChecked():
                selected_vote = "John"

            if selected_vote:
                if not self.__has_already_voted(voter_id):
                    self.__save_vote(voter_id, selected_vote)
                    self.__label_message.setText("Vote recorded successfully.")
                    self.__label_message.setStyleSheet("color: green; font-size: 18pt;")
                    self.__label_message.show()
                else:
                    self.__label_message.setText("Already voted.")
                    self.__label_message.setStyleSheet("color: red; font-size: 18pt;")
                    self.__label_message.show()

            else:
                self.__label_message.setText("Please select a vote.")
                self.__label_message.setStyleSheet("color: red; font-size: 18pt;")
                self.__label_message.show()

        except ValueError:
            self.__label_message.setText("ID must be numerical without decimals.")
            self.__label_message.setStyleSheet("color: red; font-size: 18pt;")
            self.__label_message.show()

    def __has_already_voted(self, voter_id: str) -> bool:
        """
        Checks if a given voter ID has already voted.

        :param voter_id: The ID that was typed in.
        :return: Returns True if the ID has already voted, False otherwise.
        """
        try:
            with open('votes.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == voter_id:
                        return True
        except FileNotFoundError:
            return False
        return False

    def __save_vote(self, voter_id: str, selected_vote: str) -> None:
        """
        Saves the vote to the CSV file.

        :param voter_id: The ID that was typed in.
        :param selected_vote: The radio button selection.
        """
        with open('votes.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([voter_id, selected_vote])