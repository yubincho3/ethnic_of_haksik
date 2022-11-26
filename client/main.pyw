# --- PyQt5 모듈 --- #
from PyQt5.QtWidgets import QApplication

# --- 시스템 모듈 --- #
import sys

# --- 메인 윈도우 모듈 --- #
from mainWindow import EthnicOfHaksik

if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = EthnicOfHaksik()
    application.show()
    sys.exit(app.exec_())
