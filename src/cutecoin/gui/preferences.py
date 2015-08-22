"""
Created on 11 mai 2015

@author: inso
"""

from PyQt5.QtCore import QCoreApplication

from ..core.account import Account
from . import toast
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon

from ..gen_resources.preferences_uic import Ui_PreferencesDialog
import icons_rc


class PreferencesDialog(QDialog, Ui_PreferencesDialog):

    """
    A dialog to get password.
    """

    def __init__(self, app):
        """
        Constructor
        """
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.combo_account.addItem("")
        for account_name in self.app.accounts.keys():
            self.combo_account.addItem(account_name)
        self.combo_account.setCurrentText(self.app.preferences['account'])
        for ref in Account.referentials:
            self.combo_referential.addItem(QCoreApplication.translate('Account', ref[4]))
        self.combo_referential.setCurrentIndex(self.app.preferences['ref'])
        for lang in ('en_GB', 'fr_FR'):
            self.combo_language.addItem(lang)
        self.combo_language.setCurrentText(self.app.preferences.get('lang', 'en_US'))
        self.checkbox_expertmode.setChecked(self.app.preferences.get('expert_mode', False))
        self.checkbox_maximize.setChecked(self.app.preferences.get('maximized', False))
        self.checkbox_notifications.setChecked(self.app.preferences.get('notifications', True))
        self.spinbox_digits_comma.setValue(self.app.preferences.get('digits_after_comma', 2))
        self.spinbox_digits_comma.setMaximum(12)
        self.spinbox_digits_comma.setMinimum(1)
        self.button_app.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.button_display.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.button_network.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.spinbox_data_validation.setValue(self.app.preferences.get('data_validation', 2))
        self.spinbox_data_validation.setMinimum(0)
        self.spinbox_data_validation.setMaximum(100)

        self.checkbox_proxy.setChecked(self.app.preferences.get('enable_proxy', False))
        self.spinbox_proxy_port.setEnabled(self.checkbox_proxy.isChecked())
        self.edit_proxy_address.setEnabled(self.checkbox_proxy.isChecked())
        self.checkbox_proxy.stateChanged.connect(self.handle_proxy_change)

        self.spinbox_proxy_port.setValue(self.app.preferences.get('proxy_port', 8080))
        self.spinbox_proxy_port.setMinimum(0)
        self.spinbox_proxy_port.setMaximum(55636)
        self.combox_proxytype.setCurrentText(self.app.preferences.get('proxy_type', "HTTP"))
        self.edit_proxy_address.setText(self.app.preferences.get('proxy_address', ""))

    def handle_proxy_change(self):
        self.spinbox_proxy_port.setEnabled(self.checkbox_proxy.isChecked())
        self.edit_proxy_address.setEnabled(self.checkbox_proxy.isChecked())

    def accept(self):
        pref = {'account': self.combo_account.currentText(),
                'lang': self.combo_language.currentText(),
                'ref': self.combo_referential.currentIndex(),
                'expert_mode': self.checkbox_expertmode.isChecked(),
                'maximized': self.checkbox_maximize.isChecked(),
                'digits_after_comma': self.spinbox_digits_comma.value(),
                'notifications': self.checkbox_notifications.isChecked(),
                'enable_proxy': self.checkbox_proxy.isChecked(),
                'proxy_type': self.combox_proxytype.currentText(),
                'proxy_address': self.edit_proxy_address.text(),
                'proxy_port': self.spinbox_proxy_port.value(),
                'data_validation': self.spinbox_data_validation.value()}
        self.app.save_preferences(pref)
        toast.display(self.tr("Preferences"),
                      self.tr("A restart is needed to apply your new preferences."))
        super().accept()

    def reject(self):
        super().reject()


