from PyQt5.QtWidgets import QApplication
from mainWindow import EthnicOfHaksik

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = EthnicOfHaksik()
    application.show()
    sys.exit(app.exec_())
