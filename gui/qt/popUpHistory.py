__author__ = 'zakariyah'
import sys, time, datetime, re, threading
from electrum.i18n import _, set_language
from electrum.util import print_error, print_msg
import os.path, json, ast, traceback
import shutil
import StringIO


try:
    import PyQt4
except Exception:
    sys.exit("Error: Could not import PyQt4 on Linux systems, you may try 'sudo apt-get install python-qt4'")

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import PyQt4.QtCore as QtCore

from electrum import transaction
from electrum.plugins import run_hook

from util import MyTreeWidget
from util import MONOSPACE_FONT

class PopDialog(QDialog):

    def __init__(self, items, parent):
        self.tx = items
        # tx_dict = tx.as_dict()
        self.parent = parent
        self.wallet = parent.wallet

        QDialog.__init__(self)
        self.setMinimumWidth(900)
        self.setWindowTitle(_("History"))
        self.setModal(1)

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        l = MyTreeWidget(self)
        l.setColumnCount(5)
        for i,width in enumerate(self.parent.column_widths['history']):
            l.setColumnWidth(i, width)
        l.setHeaderLabels( [ '', _('Date'), _('Description') , _('Amount'), _('Balance')] )
        itemData = []
        for itemHash in items:
            tx_hash, conf, is_mine, value, fee, balance, timestamp = itemHash
            time_str = _("unknown")
            if conf > 0:
                time_str = self.parent.format_time(timestamp)
            if conf == -1:
                time_str = 'unverified'
                icon = QIcon(":icons/unconfirmed.png")
            elif conf == 0:
                time_str = 'pending'
                icon = QIcon(":icons/unconfirmed.png")
            elif conf < 6:
                icon = QIcon(":icons/clock%d.png"%conf)
            else:
                icon = QIcon(":icons/confirmed.png")

            if value is not None:
                v_str = self.parent.format_amount(value, True, whitespaces=True)
            else:
                v_str = '--'

            balance_str = self.parent.format_amount(balance, whitespaces=True)

            if tx_hash:
                label, is_default_label = self.parent.wallet.get_label(tx_hash)
            else:
                label = _('Pruned transaction outputs')
                is_default_label = False

            item = QTreeWidgetItem( [ '', time_str, label, v_str, balance_str] )
            item.setFont(2, QFont(MONOSPACE_FONT))
            item.setFont(3, QFont(MONOSPACE_FONT))
            item.setFont(4, QFont(MONOSPACE_FONT))
            if value < 0:
                item.setForeground(3, QBrush(QColor("#BC1E1E")))
            if tx_hash:
                item.setData(0, Qt.UserRole, tx_hash)
                item.setToolTip(0, "%d %s\nTxId:%s" % (conf, _('Confirmations'), tx_hash) )
            if is_default_label:
                item.setForeground(2, QBrush(QColor('grey')))

            item.setIcon(0, icon)
            itemData.append(item)


        l.addTopLevelItems(itemData)
        vbox.addWidget(l)
