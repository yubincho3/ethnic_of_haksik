from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout,
    QLineEdit, QTextEdit, QLabel, QPushButton
)
from PyQt5.QtCore import Qt

import json

from websocketClient import WebsocketClient

from weekday import *

TIME_BUTTON_SIZE = (95, 25)
SHOW_BUTTON_SIZE = (100, 40)
BUTTON_SIZE = (50, 20)

SERVER_IP = 'ws://127.0.0.1:26656'
# SERVER_IP = 'wss://ethnic-of-haksik.herokuapp.com/'

# 메인 윈도우 클래스
class EthnicOfHaksik(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__initializeUserInterface()
        self.server = WebsocketClient(SERVER_IP)

    # UI를 생성하고 초기화 합니다.
    def __initializeUserInterface(self):
        self.setWindowTitle('학식의 민족')

        # 시간표 테이블 구역 레이아웃
        tableLayout = QGridLayout()

        # 요일 추가
        for i in range(len(weekdays) - 1):
            box = QLineEdit()
            box.setReadOnly(True)
            box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            box.setText(weekdays[i].name)
            box.setFixedSize(*BUTTON_SIZE)
            tableLayout.addWidget(box, 0, i + 1)

        # 시간 추가
        self.buttons = [[] for _ in range(22)]
        for i in range(18, 39):
            start = f'{30 * i // 60}:{["00", "30"][i % 2]}'
            end = f'{30 * (i + 1) // 60}:{["00", "30"][(i + 1) % 2]}'
            timeText = f'{start}~{end}'

            box = QLineEdit()
            box.setReadOnly(True)
            box.setAlignment(Qt.AlignmentFlag.AlignRight)
            box.setText(timeText)
            box.setFixedSize(*TIME_BUTTON_SIZE)
            tableLayout.addWidget(box, i - 8, 0)

            # 토글 버튼 추가
            for j in range(6):
                button = QPushButton()
                button.setFixedSize(*BUTTON_SIZE)
                button.setCheckable(True)
                button.toggled.connect(self.slotToggle)
                button.toggle()
                self.buttons[i - 18].append(button)
                tableLayout.addWidget(button, i - 8, j + 1)

        # 결과창 구역 레이아웃
        resultLayout = QVBoxLayout()

        self.resultBox = QTextEdit(self)
        self.resultBox.setReadOnly(True)
        resultLayout.addWidget(self.resultBox)

        # Show 버튼 왼쪽에 공간을 만들기 위한 레이아웃
        showButtonLayout = QHBoxLayout()

        showButton = QPushButton("Show", self)
        showButton.setFixedSize(*SHOW_BUTTON_SIZE)
        showButton.clicked.connect(self.showClicked)

        showButtonLayout.addStretch(1)
        showButtonLayout.addWidget(showButton)
        resultLayout.addLayout(showButtonLayout)

        # 메인 레이아웃
        mainLayout = QGridLayout()

        tableLabel = QLabel('\n시간표를 입력해주세요!\n', self)
        foodLabel = QLabel('\n지금 먹을 수 있는 학식은...\n', self)

        mainLayout.addWidget(tableLabel, 0, 0)
        mainLayout.addWidget(foodLabel, 0, 1)
        mainLayout.addLayout(tableLayout, 1, 0)
        mainLayout.addLayout(resultLayout, 1, 1)

        self.setLayout(mainLayout)

    # 버튼이 눌릴 때마다 색을 변경합니다.
    def slotToggle(self, state: bool):
        button = self.sender()
        if isinstance(button, QPushButton):
            button.setStyleSheet(f"background-color: {['red', 'green'][state]}")

    # 시간표를 서버에 업로드하고 수신한 결과를 출력합니다.
    def showClicked(self):
        today = getTodayWeekday()
        unableTimes = []

        for i in range(18, 39):
            if self.buttons[i - 18][today.value].isChecked():
                continue

            unableTimes.append([30 * i // 60, 30 * (i % 2)])

        jsonString = json.dumps(unableTimes)
        self.server.sendString(jsonString)

        resultText = self.server.getString()
        self.resultBox.setMarkdown(resultText)
