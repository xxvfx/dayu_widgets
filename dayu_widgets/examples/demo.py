import importlib
import os

from dayu_widgets import MRadioGroup
from dayu_widgets.qt import *
from dayu_widgets import STATIC_FOLDERS
from dayu_widgets.MTheme import global_theme
from dayu_widgets.MSpinBox import qss
from dayu_widgets.MDockWidget import MDockWidget

qss_1 = '''


QScrollBar:horizontal {{
    border: 0 solid {border};
    height: 9px;
    margin: 0 32px 0 0;
    background-color: {border};
}}

QScrollBar::handle:horizontal {{
    background-color: {background_dark};
    min-width: 10px;
}}

QScrollBar::add-line:horizontal {{
    subcontrol-origin: margin;
    subcontrol-position: right center;
    background: {border};
    width: 15px;
}}

QScrollBar::sub-line:horizontal {{
    subcontrol-origin: margin;
    subcontrol-position: right center;
    background: {border};
    width: 15px;
    right: 16px;
}}

QScrollBar::left-arrow:horizontal {{
    width: 9px;
    height: 9px;
    position: relative;
    image: url(left_fill.svg)
}}

QScrollBar::right-arrow:horizontal {{
    width: 9px;
    height: 9px;
    position: relative;
    image: url(right_fill.svg)
}}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

QScrollBar:vertical {{
    border: 0 solid {border};
    width: 9px;
    margin: 0 0 32px 0 ;
    background-color: {border};
}}

QScrollBar::handle:vertical {{
    background-color: {background_dark};
    min-height: 10px;
}}

QScrollBar::add-line:vertical {{
    subcontrol-origin: margin;
    subcontrol-position: center bottom;
    background: {border};
    height: 15px;
}}

QScrollBar::sub-line:vertical {{
    subcontrol-origin: margin;
    subcontrol-position: center bottom;
    background: {border};
    height: 15px;
    bottom: 16px;
}}

QScrollBar::up-arrow:vertical {{
    width: 9px;
    height: 9px;
    position: relative;
    image: url(up_fill.svg)
}}

QScrollBar::down-arrow:vertical {{
    width: 9px;
    height: 9px;
    position: relative;
    image: url(down_fill.svg)
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QSplitter::handle {{
    background-color: {border};
    image: url(splitter.svg);
}}

QSplitter::handle:horizontal {{
    width: 2px;
}}

QSplitter::handle:vertical {{
    height: 2px;
}}

'''.format(**global_theme)
qss_1 = qss_1.replace('url(', 'url({}/'.format(STATIC_FOLDERS[0].replace('\\', '/')))

qss_1 += qss


def get_test_widget():
    result = []
    for index, i in enumerate(os.listdir('.')):
        if i.startswith('__') or (not i.endswith('.py')) or i == 'demo.py':
            continue
        name = i.split('.')[0]
        module_name = 'dayu_widgets.examples.{component}'.format(component=name)
        module = importlib.import_module(module_name, name)
        if hasattr(module, name):
            with open('./{}.py'.format(name)) as f:
                result.append((name, getattr(module, name), f.readlines()))
    return result


class MDemo(QMainWindow):
    def __init__(self, parent=None):
        super(MDemo, self).__init__(parent)
        self.setWindowTitle('Dayu Widgets Demo')
        self.setStyleSheet(qss_1)
        self._init_ui()

    def _init_ui(self):
        self.text_edit = QTextEdit()
        self.stacked_widget = QStackedWidget()
        list_widget = MRadioGroup(type='button', orientation=Qt.Vertical, parent=self)
        list_widget.sig_checked_changed.connect(self.slot_change_widget)
        data_list = []
        for name, cls, code in get_test_widget():
            data_list.append({'text': name, 'date': code})
            widget = cls()
            widget.setProperty('code', code)
            self.stacked_widget.addWidget(widget)
        list_widget.set_radio_list(data_list)
        list_widget.set_checked(0)

        left_widget = QWidget()
        left_lay = QVBoxLayout()
        left_widget.setLayout(left_lay)
        left_lay.addWidget(list_widget)
        left_lay.addStretch()

        test_widget = MDockWidget('Example List')
        test_widget.setWidget(left_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, test_widget)

        code_widget = MDockWidget('Example Code')
        code_widget.setWidget(self.text_edit)
        self.addDockWidget(Qt.RightDockWidgetArea, code_widget)
        self.setCentralWidget(self.stacked_widget)

    def slot_change_widget(self, index):
        self.stacked_widget.setCurrentIndex(index)
        widget = self.stacked_widget.widget(index)
        self.text_edit.setPlainText(''.join(widget.property('code')))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    test = MDemo()
    test.show()
    sys.exit(app.exec_())
