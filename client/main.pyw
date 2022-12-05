from PyQt5.QtWidgets import QApplication
from mainWindow import EthnicOfHaksik

import asyncio
import qasync

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    application = EthnicOfHaksik()
    application.show()

    sys.exit(loop.run_forever())
