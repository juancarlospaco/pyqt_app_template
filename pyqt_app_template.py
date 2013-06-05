#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PEP8:OK, LINT:OK, PY3:OK


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
'App_Template'
__version__ = ' 0.1 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ' https://github.com/juancarlospaco '
__date__ = ' 31/02/2015 '
__prj__ = ' apptemplate '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = 'http://opensource.org/licenses/gpl-3.0.html'


# snakes fight
try:  # py2
    str, range, input = unicode, xrange, raw_input  # lint:ok
except NameError:  # py3
    buffer, long = memoryview, int  # lint:ok


# imports
import sys
from os import (path, linesep, sep, geteuid, environ, mkdir, getcwd, chdir)
from datetime import datetime
from subprocess import call
from random import randint
from webbrowser import open_new_tab
from shutil import make_archive
from subprocess import check_output as getoutput
from getpass import getuser
try:
    from urllib.request import urlopen  # py3
except ImportError:
    from urllib2 import urlopen  # lint:ok

from sip import setapi
try:
    from PyQt4.QtGui import (QIcon, QLabel, QFileDialog, QWidget, QVBoxLayout,
        QHBoxLayout, QComboBox, QCursor, QLineEdit, QCheckBox, QPushButton,
        QGroupBox, QMessageBox, QCompleter, QDirModel, QLCDNumber, QAction,
        QFont, QTabWidget, QDockWidget, QToolBar, QSizePolicy, QColorDialog,
        QPalette, QPen, QPainter, QColor, QPixmap, QMenu, QDialog, QScrollArea,
        QDesktopWidget, QProgressBar, QDialogButtonBox, QDial, QTabBar,
        QTreeWidget, QTreeWidgetItem, QColumnView, QGraphicsDropShadowEffect,
        QSystemTrayIcon)

    from PyQt4.QtCore import (Qt, QDir, QSize, QUrl, QTimer, QFileInfo, QFile,
        QIODevice, QProcess, QEvent)

    from PyQt4.QtNetwork import (QNetworkProxy, QHttp)
    from PyQt4.phonon import Phonon
except ImportError:
    print(" ERROR: No Qt4 avaliable! \n ( sudo apt-get install python-qt4 ) ")
    exit()

try:
    from PyKDE4.kdeui import (KAboutApplicationDialog, KColorDialog, KHelpMenu,
                              KFontDialog)
    from PyKDE4.kdeui import KTextEdit as QPlainTextEdit
    from PyKDE4.kdeui import KDatePicker as QCalendarWidget
    from PyKDE4.kdeui import KApplication as QApplication
    from PyKDE4.kdeui import KMainWindow as QMainWindow
    from PyKDE4.solid import Solid
    from PyKDE4.nepomuk import Nepomuk
    from PyKDE4.kdecore import (KCmdLineArgs, KAboutData, ki18n, KUrl)
    aboutData = KAboutData(__doc__, "", ki18n(__doc__), __version__,
        ki18n(__doc__), KAboutData.License_GPL, ki18n(__author__),
        ki18n(" This Smart App uses KDE if present, else Qt only if present "),
        __url__, __email__)
    KDE = True
except ImportError:
    from PyQt4.QtGui import (QPlainTextEdit, QCalendarWidget,  # lint:ok
                            QFontDialog, QMainWindow, QApplication)  # lint:ok
    KDE = False


# API 2
(setapi(a, 2) for a in ("QDate", "QDateTime", "QString", "QTime", "QUrl",
                        "QTextStream", "QVariant"))


# constants
HOME = path.abspath(path.expanduser("~"))


# root check
if geteuid() == 0:
    exit(" ERROR: Do NOT Run as root!, NO ejecutar como root!\n bye noob...\n")
else:
    pass


print(('#' * 80))
print((''.join((__doc__, ',v.', __version__, __license__, ' by ', __author__))))


###############################################################################


class TabBar(QTabBar):
    ' custom tab bar '
    def __init__(self, parent):
        ' init class custom tab bar '
        QTabBar.__init__(self, parent)
        self._editor = QLineEdit(self)
        self._editor.setToolTip(' Type a Tab Name ')
        self._editor.setWindowFlags(Qt.Popup)
        self._editor.setFocusProxy(self)
        self._editor.editingFinished.connect(self.handleEditingFinished)
        self._editor.installEventFilter(self)

    def eventFilter(self, widget, event):
        ' filter mouse, esc key,  events '
        if ((event.type() == QEvent.MouseButtonPress and
             not self._editor.geometry().contains(event.globalPos())) or
            (event.type() == QEvent.KeyPress and
             event.key() == Qt.Key_Escape)):
            self._editor.hide()
            return True
        return QTabBar.eventFilter(self, widget, event)

    def mouseDoubleClickEvent(self, event):
        ' handle double click '
        index = self.tabAt(event.pos())
        if index >= 0:
            self.editTab(index)

    def editTab(self, index):
        ' handle the editor '
        rect = self.tabRect(index)
        self._editor.setFixedSize(rect.size())
        self._editor.move(self.parent().mapToGlobal(rect.topLeft()))
        self._editor.setText(self.tabText(index))
        if not self._editor.isVisible():
            self._editor.show()

    def handleEditingFinished(self):
        ' set text when editing has finished '
        index = self.currentIndex()
        if index >= 0:
            self._editor.hide()
            self.setTabText(index, self._editor.text())


###############################################################################


class MyMainWindow(QMainWindow):
    ' Main Window '
    def __init__(self, parent=None):
        ' Initialize QWidget inside MyMainWindow '
        super(MyMainWindow, self).__init__(parent)
        QWidget.__init__(self)
        self.statusBar().showMessage('               {}'.format(__doc__))
        self.setStyleSheet('QStatusBar{color:grey;}')
        self.setWindowTitle(__doc__)
        self.setWindowIcon(QIcon.fromTheme("face-monkey"))
        self.setFont(QFont('Ubuntu Light', 10))
        self.setMaximumSize(QDesktopWidget().screenGeometry().width(),
                            QDesktopWidget().screenGeometry().height())

        # directory auto completer
        self.completer = QCompleter(self)
        self.dirs = QDirModel(self)
        self.dirs.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.completer.setModel(self.dirs)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)

        # Proxy support, by reading http_proxy os env variable
        proxy_url = QUrl(environ.get('http_proxy', ''))
        QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy
            if str(proxy_url.scheme()).startswith('http')
            else QNetworkProxy.Socks5Proxy, proxy_url.host(), proxy_url.port(),
                 proxy_url.userName(), proxy_url.password())) \
            if 'http_proxy' in environ else None
        print((' INFO: Proxy Auto-Config as ' + str(proxy_url)))

        # basic widgets layouts and set up
        self.mainwidget = QTabWidget()
        self.mainwidget.setToolTip(__doc__)
        self.mainwidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mainwidget.tabCloseRequested.connect(lambda:
            self.mainwidget.setTabPosition(randint(0, 3)))
            # if self.mainwidget.tabPosition() == 0
            # else self.mainwidget.setTabPosition(0))
        self.mainwidget.setStyleSheet('QTabBar{color:white;font-weight:bold;}')
        self.mainwidget.setTabBar(TabBar(self))
        self.mainwidget.setMovable(True)
        self.mainwidget.setTabsClosable(True)
        self.mainwidget.setTabShape(QTabWidget.Triangular)
        self.setCentralWidget(self.mainwidget)
        self.dock1 = QDockWidget()
        self.dock2 = QDockWidget()
        self.dock3 = QDockWidget()
        for a in (self.dock1, self.dock2, self.dock3):
            a.setWindowModality(Qt.NonModal)
            a.setWindowOpacity(0.9)
            a.setWindowTitle(__doc__
                             if a.windowTitle() == '' else a.windowTitle())
            a.setStyleSheet(' QDockWidget::title{text-align:center;}')
            self.mainwidget.addTab(a, QIcon.fromTheme("face-smile"),
                                   'Double Click Me')

        # Paleta de colores para pintar transparente
        self.palette().setBrush(QPalette.Base, Qt.transparent)
        self.setPalette(self.palette())
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)

        # toolbar and basic actions
        self.toolbar = QToolBar(self)
        self.toolbar.setIconSize(QSize(24, 24))
        # spacer widget for left
        self.left_spacer = QWidget(self)
        self.left_spacer.setSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding)
        # spacer widget for right
        self.right_spacer = QWidget(self)
        self.right_spacer.setSizePolicy(QSizePolicy.Expanding,
                                        QSizePolicy.Expanding)
        qaqq = QAction(QIcon.fromTheme("application-exit"), 'Quit', self)
        qaqq.setShortcut('Ctrl+Q')
        qaqq.triggered.connect(exit)
        qamin = QAction(QIcon.fromTheme("go-down"), 'Minimize', self)
        qamin.triggered.connect(lambda: self.showMinimized())
        qamax = QAction(QIcon.fromTheme("go-up"), 'Maximize', self)
        qanor = QAction(QIcon.fromTheme("view-fullscreen"),
                                        'AutoCenter AutoResize', self)
        qanor.triggered.connect(self.center)
        qatim = QAction(QIcon.fromTheme("mail-signed-verified"),
                                        'View Date and Time', self)
        qatim.triggered.connect(self.timedate)
        qabug = QAction(QIcon.fromTheme("help-about"), 'Report a Problem', self)
        qabug.triggered.connect(lambda: qabug.setDisabled(True) if not call(
            'xdg-open mailto:' + 'whnapneybfcnpb@hohagh.pbz'.decode('rot13'),
            shell=True) else ' ERROR ')
        qamax.triggered.connect(lambda: self.showMaximized())
        qaqt = QAction(QIcon.fromTheme("help-about"), 'About Qt', self)
        qaqt.triggered.connect(lambda: QMessageBox.aboutQt(self))
        qakde = QAction(QIcon.fromTheme("help-about"), 'About KDE', self)
        if KDE:
            qakde.triggered.connect(KHelpMenu(self, "", False).aboutKDE)
        qaslf = QAction(QIcon.fromTheme("help-about"), 'About Self', self)
        if KDE:
            qaslf.triggered.connect(
                                KAboutApplicationDialog(aboutData, self).exec_)
        else:
            qaslf.triggered.connect(lambda: QMessageBox.about(self.mainwidget,
            __doc__, ''.join((__doc__, linesep, 'version ', __version__, ', (',
            __license__, '), by ', __author__, ', ( ', __email__, ' )', linesep
            ))))
        qafnt = QAction(QIcon.fromTheme("tools-check-spelling"),
                                        'Set GUI Font', self)
        if KDE:
            font = QFont()
            qafnt.triggered.connect(lambda:
            self.setStyleSheet(''.join((
                '*{font-family:', str(font.toString()), '}'))
                if KFontDialog.getFont(font)[0] == QDialog.Accepted else ''))
        else:
            qafnt.triggered.connect(lambda:
                self.setStyleSheet(''.join(('*{font-family:',
                            str(QFontDialog.getFont()[0].toString()), '}'))))
        qasrc = QAction(QIcon.fromTheme("applications-development"),
                        'View Source Code', self)
        qasrc.triggered.connect(lambda: call('xdg-open {}'.format(__file__), 1))
        qakb = QAction(QIcon.fromTheme("input-keyboard"),
                       'Keyboard Shortcuts', self)
        qakb.triggered.connect(lambda: QMessageBox.information(self.mainwidget,
                               'Keyboard Shortcuts', ' Ctrl+Q = Quit '))
        qapic = QAction(QIcon.fromTheme("camera-photo"),
                        'Take a Screenshot', self)
        qapic.triggered.connect(lambda: QPixmap.grabWindow(
            QApplication.desktop().winId()).save(QFileDialog.getSaveFileName(
            self.mainwidget, " Save Screenshot As ...", path.expanduser("~"),
            ';;(*.png) PNG', 'png')))
        qatb = QAction(QIcon.fromTheme("go-top"), 'Toggle ToolBar', self)
        qatb.triggered.connect(lambda: self.toolbar.hide()
                if self.toolbar.isVisible() is True else self.toolbar.show())
        qati = QAction(QIcon.fromTheme("help-browser"),
                       'Switch ToolBar Icon Size', self)
        qati.triggered.connect(lambda:
            self.toolbar.setIconSize(self.toolbar.iconSize() * 4)
            if self.toolbar.iconSize().width() * 4 == 24
            else self.toolbar.setIconSize(self.toolbar.iconSize() / 4))
        qasb = QAction(QIcon.fromTheme("zoom-in"), 'Toggle Tabs Bar', self)
        qasb.triggered.connect(lambda: self.mainwidget.tabBar().hide()
                               if self.mainwidget.tabBar().isVisible() is True
                               else self.mainwidget.tabBar().show())
        qadoc = QAction(QIcon.fromTheme("help-browser"), 'On-line Docs', self)
        qadoc.triggered.connect(lambda: open_new_tab(__url__))
        qapy = QAction(QIcon.fromTheme("help-about"), 'About Python', self)
        qapy.triggered.connect(lambda: open_new_tab('http://python.org/about'))
        qali = QAction(QIcon.fromTheme("help-browser"), 'Read Licence', self)
        qali.triggered.connect(lambda: open_new_tab(__full_licence__))
        qacol = QAction(QIcon.fromTheme("preferences-system"), 'Set GUI Colors',
                        self)
        if KDE:
            color = QColor()
            qacol.triggered.connect(lambda:
                self.setStyleSheet(''.join(('* { background-color: ',
                                            str(color.name()), '}')))
                if KColorDialog.getColor(color, self) else '')
        else:
            qacol.triggered.connect(lambda: self.setStyleSheet(''.join((
                ' * { background-color: ', str(QColorDialog.getColor().name()),
                ' } '))))
        qatit = QAction(QIcon.fromTheme("preferences-system"),
                        'Set the App Window Title', self)
        qatit.triggered.connect(self.seTitle)
        self.toolbar.addWidget(self.left_spacer)
        self.toolbar.addSeparator()
        for b in (qaqq, qamin, qanor, qamax, qasrc, qakb, qacol, qatim, qatb,
            qafnt, qati, qasb, qatit, qapic, qadoc, qali, qaslf, qaqt, qakde,
            qapy, qabug):
            self.toolbar.addAction(b)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.right_spacer)
        # define the menu
        menu = self.menuBar()
        # File menu items
        menu.addMenu('&File').addActions((qaqq, ))
        menu.addMenu('&Window').addActions((qamax, qanor, qamin))
        # Settings menu
        menu.addMenu('&Settings').addActions((qasrc, qacol, qafnt, qatim,
                                              qatb, qati, qasb, qapic))
        # Help menu items
        menu.addMenu('&Help').addActions((qadoc, qakb, qabug, qali,
                                          qaqt, qakde, qapy, qaslf))
        # Tray Icon
        tray = QSystemTrayIcon(QIcon.fromTheme("face-devilish"), self)
        tray.setToolTip(__doc__)
        traymenu = QMenu()
        traymenu.addActions((qamax, qanor, qamin, qaqq))
        tray.setContextMenu(traymenu)
        tray.show()

        def contextMenuRequested(point):
            ' quick and dirty custom context menu '
            menu = QMenu()
            menu.addActions((qaqq, qamin, qanor, qamax, qasrc, qakb, qacol,
                qafnt, qati, qasb, qatb, qatim, qatit, qapic, qadoc, qali,
                qaslf, qaqt, qakde, qapy, qabug))
            menu.exec_(self.mapToGlobal(point))
        self.mainwidget.customContextMenuRequested.connect(contextMenuRequested)

        def must_be_checked(widget_list):
            ' widget tuple passed as argument should be checked as ON '
            for each_widget in widget_list:
                try:
                    each_widget.setChecked(True)
                except:
                    pass

        def must_have_tooltip(widget_list):
            ' widget tuple passed as argument should have tooltips '
            for each_widget in widget_list:
                try:
                    each_widget.setToolTip(each_widget.text())
                except:
                    each_widget.setToolTip(each_widget.currentText())
                finally:
                    each_widget.setCursor(QCursor(Qt.PointingHandCursor))

        def must_autofillbackground(widget_list):
            ' widget tuple passed as argument should have filled background '
            for each_widget in widget_list:
                try:
                    each_widget.setAutoFillBackground(True)
                except:
                    pass

        def must_glow(widget_list):
            ' apply an glow effect to the widget '
            for glow, each_widget in enumerate(widget_list):
                try:
                    if each_widget.graphicsEffect() is None:
                        glow = QGraphicsDropShadowEffect(self)
                        glow.setOffset(0)
                        glow.setBlurRadius(99)
                        glow.setColor(QColor(99, 255, 255))
                        each_widget.setGraphicsEffect(glow)
                        # glow.setEnabled(False)
                        try:
                            each_widget.clicked.connect(lambda:
                            each_widget.graphicsEffect().setEnabled(True)
                            if each_widget.graphicsEffect().isEnabled() is False
                            else each_widget.graphicsEffect().setEnabled(False))
                        except:
                            each_widget.sliderPressed.connect(lambda:
                            each_widget.graphicsEffect().setEnabled(True)
                            if each_widget.graphicsEffect().isEnabled() is False
                            else each_widget.graphicsEffect().setEnabled(False))
                except:
                    pass

        #######################################################################

        self.group1 = QGroupBox()
        self.group1.setTitle(__doc__)
        self.frmt = QComboBox(self.group1)
        self.frmt.addItems(['blah ', 'blah blah', 'blah blah blah'])
        self.file1 = QLineEdit()
        self.file1.setPlaceholderText('/full/path/to/one_file.py')
        self.file1.setCompleter(self.completer)
        self.borig = QPushButton(QIcon.fromTheme("folder-open"), 'Open')
        vboxg1 = QVBoxLayout(self.group1)
        for each_widget in (QLabel('<b style="color:white;">some comment'),
            self.file1, self.borig,
            QLabel('<b style="color:white;">Lorem Impsum'), self.frmt):
            vboxg1.addWidget(each_widget)

        self.group2 = QGroupBox()
        self.group2.setTitle(__doc__)
        self.nwfl = QCheckBox('Be Awesome')
        self.smll = QCheckBox('Solve the Squaring of the Circle')
        self.lrgf = QCheckBox('Im just a QCheckBox')
        self.case = QCheckBox('Use Quantum Processing')
        vboxg2 = QVBoxLayout(self.group2)
        for each_widget in (self.nwfl, self.smll, self.lrgf, self.case):
            vboxg2.addWidget(each_widget)

        group3 = QGroupBox()
        group3.setTitle(__doc__)
        self.plai = QCheckBox('May the Force be with You')
        self.nocr = QCheckBox('Im just a Place Holder')
        self.ridt = QCheckBox('Lorem Impsum')
        self.nocm = QCheckBox('Divide by Zero')
        vboxg3 = QVBoxLayout(group3)
        for each_widget in (self.plai, self.nocr, self.ridt, self.nocm):
            vboxg3.addWidget(each_widget)
        container = QWidget()
        hbox = QHBoxLayout(container)
        for each_widget in (self.group2, self.group1, group3):
            hbox.addWidget(each_widget)
        self.dock1.setWidget(container)

        # dock 2
        self.dock2.setWidget(QPlainTextEdit())

        # dock 3
        self.dock3.setWidget(QCalendarWidget())

        # configure some widget settings
        must_be_checked((self.nwfl, self.smll, self.lrgf, self.plai))
        must_have_tooltip((self.plai, self.nocr, self.ridt, self.nocm,
                           self.nwfl, self.smll, self.lrgf, self.case))
        must_autofillbackground((self.plai, self.nocr, self.ridt, self.nocm,
                                 self.nwfl, self.smll, self.lrgf, self.case))
        must_glow((self.plai, self.nocr, self.ridt, self.nocm, self.nwfl, ))

    def run(self):
        ' run forest run '
        print((' INFO: Working at {}'.format(str(datetime.datetime.now()))))

    ###########################################################################

    def paintEvent(self, event):
        'Paint semi-transparent background, animated pattern, background text'
        # because we are on 2012 !, its time to showcase how Qt we are !
        QWidget.paintEvent(self, event)
        # make a painter
        p = QPainter(self)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        # fill a rectangle with transparent painting
        p.fillRect(event.rect(), Qt.transparent)
        # animated random dots background pattern
        for i in range(4096):
            x = randint(9, self.size().width() - 9)
            y = randint(9, self.size().height() - 9)
            p.setPen(QPen(QColor(randint(9, 255), randint(9, 255), 255), 1))
            p.drawPoint(x, y)
        # set pen to use white color
        p.setPen(QPen(QColor(randint(9, 255), randint(9, 255), 255), 1))
        # Rotate painter 45 Degree
        p.rotate(30)
        # Set painter Font for text
        p.setFont(QFont('Ubuntu', 200))
        # draw the background text, with antialiasing
        if KDE:
            p.drawText(99, 99, "PyKDE")
        else:
            p.drawText(99, 99, "PyQt")
        # Rotate -45 the QPen back !
        p.rotate(-30)
        # set the pen to no pen
        p.setPen(Qt.NoPen)
        # Background Color
        p.setBrush(QColor(0, 0, 0))
        # Background Opacity
        p.setOpacity(0.75)
        # Background Rounded Borders
        p.drawRoundedRect(self.rect(), 50, 50)
        # finalize the painter
        p.end()

    def seTitle(self):
        ' set the title of the main window '
        dialog = QDialog(self)
        textEditInput = QLineEdit(' Type Title Here ')
        ok = QPushButton(' O K ')
        ok.clicked.connect(lambda: self.setWindowTitle(textEditInput.text()))
        ly = QVBoxLayout()
        [ly.addWidget(wdgt) for wdgt in (QLabel('Title:'), textEditInput, ok)]
        dialog.setLayout(ly)
        dialog.exec_()

    def timedate(self):
        ' get the time and date '
        dialog = QDialog(self)
        clock = QLCDNumber()
        clock.setNumDigits(24)
        timer = QTimer()
        timer.timeout.connect(lambda: clock.display(
            datetime.now().strftime("%d-%m-%Y %H:%M:%S %p")))
        timer.start(1000)
        clock.setToolTip(datetime.now().strftime("%c %x"))
        ok = QPushButton(' O K ')
        ok.clicked.connect(dialog.close)
        ly = QVBoxLayout()
        [ly.addWidget(wdgt) for wdgt in (QCalendarWidget(), clock, ok)]
        dialog.setLayout(ly)
        dialog.exec_()

    def closeEvent(self, event):
        ' Ask to Quit '
        if QMessageBox.question(self, ' Close ', ' Quit ? ',
           QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        ' Center and resize the window '
        self.showNormal()
        self.resize(QDesktopWidget().screenGeometry().width() // 1.25,
                    QDesktopWidget().screenGeometry().height() // 1.25)
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

    def nepomuk_set(self, file_tag=None, __tag='', _label='', _description=''):
        ' Quick and Easy Nepomuk Taggify for Files '
        print((''' INFO: Semantic Desktop Experience is Tagging Files :
              {}, {}, {}, {})'''.format(file_tag, __tag, _label, _description)))
        if Nepomuk.ResourceManager.instance().init() is 0:
            fle = Nepomuk.Resource(KUrl(QFileInfo(file_tag).absoluteFilePath()))
            _tag = Nepomuk.Tag(__tag)
            _tag.setLabel(_label)
            fle.addTag(_tag)
            fle.setDescription(_description)
            print(([str(a.label()) for a in fle.tags()], fle.description()))
            return ([str(a.label()) for a in fle.tags()], fle.description())
        else:
            print(" ERROR: FAIL: Nepomuk is not running ! ")
            return

    def nepomuk_get(self, query_to_search):
        ' Quick and Easy Nepomuk Query for Files '
        print((''' INFO: Semantic Desktop Experience is Quering Files :
              {} '''.format(query_to_search)))
        results = []
        nepo = Nepomuk.Query.QueryServiceClient()
        nepo.desktopQuery("hasTag:{}".format(query_to_search))

        def _query(data):
            ''' ('filename.ext', 'file description', ['list', 'of', 'tags']) '''
            results.append(([str(a.resource().genericLabel()) for a in data][0],
                            [str(a.resource().description()) for a in data][0],
            [str(a.label()) for a in iter([a.resource().tags() for a in data][0]
            )]))
        nepo.newEntries.connect(_query)

        def _end():
            '''
            [  ('filename.ext', 'file description', ['list', 'of', 'tags']),
               ('filename.ext', 'file description', ['list', 'of', 'tags']),
               ('filename.ext', 'file description', ['list', 'of', 'tags'])  ]
            '''
            nepo.newEntries.disconnect
            print(results)
            return results
        nepo.finishedListing.connect(_end)


###############################################################################


def main():
    ' Main Loop '
    from getopt import getopt
    OPAQUE = True
    BORDER = True
    try:
        opts, args = getopt(sys.argv[1:], 'hvob',
                                   ['version', 'help', 'opaque', 'borderless'])
        pass
    except:
        pass
    for o, v in opts:
        if o in ('-h', '--help'):
            print('''
            Usage:
                  -h, --help        Show help informations and exit.
                  -v, --version     Show version information and exit.
                  -o, --opaque      Use Opaque GUI.
                  -b, --borderless  No WM Borders.
                  Run without parameters and arguments to use the GUI.
            ''')
            return sys.exit(1)
        elif o in ('-v', '--version'):
            print(__version__)
            return sys.exit(1)
        elif o in ('-o', '--opaque'):
                OPAQUE = False
        elif o in ('-b', '--borderless'):
                BORDER = False
    # define our App
    try:
        app = QApplication(sys.argv)
        app.setApplicationName(__doc__)
        app.setOrganizationName(__author__)
        app.setOrganizationDomain(__author__)
        app.setStyle('Plastique')
        app.setStyle('Oxygen')
    except TypeError:
        aboutData = KAboutData(__doc__, '', ki18n(__doc__), __version__,
            ki18n(__doc__), KAboutData.License_GPL, ki18n(__author__),
            ki18n("none"), __url__, __email__)
        KCmdLineArgs.init(sys.argv, aboutData)
        app = QApplication()
        app.lastWindowClosed.connect(app.quit)
    # w is gonna be the mymainwindow class
    w = MyMainWindow()
    # set the class with the attribute of translucent background as true
    if OPAQUE is True:
        w.setAttribute(Qt.WA_TranslucentBackground, True)
    # WM Borders
    if BORDER is False:
        w.setWindowFlags(w.windowFlags() | Qt.FramelessWindowHint)
    # run the class
    w.show()
    # if exiting the loop take down the app
    sys.exit(app.exec_())


if __name__ == '__main__':
    ' Do NOT add anything here!, use main() function instead. '
    main()
