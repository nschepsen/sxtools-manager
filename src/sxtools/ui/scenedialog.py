from PySide6.QtWidgets import QDialog, QRadioButton
from PySide6.QtCore import QSize
from sxtools.ui.compiled.decisiondialog import Ui_DecisionDialog


class DecisionDialog(QDialog):
    '''
    A dialog that lets users select an item from an "options"-list
    '''
    def __init__(self, context: str, options: list, parent=None) -> None:

        super(DecisionDialog, self).__init__(parent)
        self.ui = Ui_DecisionDialog()
        self.ui.setupUi(self) # load UI elements
        self.ui.lblContext.setText(context)
        # create buttons dynamically & append 'em to the group box
        for o in options:
            btn = QRadioButton(self.ui.gbOptions)
            btn.setText(o)
            btn.setMinimumSize(QSize(0, 30))
            self.ui.bgOptions.addButton(btn)
            self.ui.loOptions.insertWidget(0, btn)
        if btn: btn.setChecked(True)
        # connect UI elements to the existing methods

    def decision(self) -> str:
        '''
        return a user's decision based on the given "option"-list
        '''
        if self.ui.rbOptionOther.isChecked():
            return self.ui.leOption.text()
        elif self.ui.rbOptionNone.isChecked():
            return 'title'
        return self.ui.bgOptions.checkedButton().text()
