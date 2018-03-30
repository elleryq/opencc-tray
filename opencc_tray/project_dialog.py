# -*- coding: utf-8 -*-
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QWidget,
        QDialog, QLabel, QFrame, QFileDialog, QGridLayout,
        QPushButton, QLineEdit, QDialogButtonBox, QVBoxLayout)


logger = logging.getLogger(__name__)


class ProjectDialog(QDialog):

    def __init__(self, parent=None):
        """Constructor."""
        super(ProjectDialog, self).__init__(parent)
        self._name = None
        self._directory = None

        self.initUI()

    def initUI(self):
        """Initialize UI."""
        self.setMinimumSize(200, 100)
        self.setWindowTitle(self.tr("Add project"))

        frameStyle = QFrame.Sunken | QFrame.Panel

        self.directoryLabel = QLabel()
        self.directoryLabel.setFrameStyle(frameStyle)
        self.directoryButton = QPushButton(self.tr("Open Project directory"))
        self.directoryButton.clicked.connect(self.setExistingDirectory)
        self.projectNameLabel = QLabel()
        self.projectNameLabel.setText(self.tr("Project name"))
        self.projectNameLabel.setFrameStyle(frameStyle)
        self.projectNameLineEdit = QLineEdit()
        self.projectNameLineEdit.textChanged.connect(self.setName)

        layout = QVBoxLayout()

        widget = QWidget()
        gridlayout = QGridLayout()
        gridlayout.setColumnStretch(1, 1)
        gridlayout.setColumnMinimumWidth(1, 250)

        gridlayout.addWidget(self.directoryButton, 0, 0)
        gridlayout.addWidget(self.directoryLabel, 0, 1)
        gridlayout.addWidget(self.projectNameLabel, 1, 0)
        gridlayout.addWidget(self.projectNameLineEdit, 1, 1)
        widget.setLayout(gridlayout)

        layout.addWidget(widget)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def setExistingDirectory(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,
                self.tr("Open project directory"),
                self.directoryLabel.text(), options=options)
        if directory:
            self.directoryLabel.setText(directory)
            self._directory = directory

    @property
    def directory(self):
        return self._directory

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def setName(self, name):
        self._name = name

    @staticmethod
    def getProjectNameAndDirectory(parent=None):
        dialog = ProjectDialog(parent)
        result = dialog.exec_()

        return (dialog.name, dialog.directory, result == QDialog.Accepted)