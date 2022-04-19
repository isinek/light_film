import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QPushButton, QAction
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt


class ProjectHelper():
    def __init__(self, helperApp):
        self.helperApp = helperApp
        self.data = {}
        self.data['project_name'] = helperApp.ui['project_structure']['project_name'].text()
        self.data['project_code'] = helperApp.ui['project_structure']['project_code'].text().upper()
        self.data['project_type'] = helperApp.ui['project_structure']['project_type'].currentText()
        self.data['asset_name'] = helperApp.ui['project_structure']['asset_name'].text()
        self.data['asset_type'] = helperApp.ui['project_structure']['asset_type'].currentText()
        self.data['dimensions_length'] = helperApp.ui['project_structure']['dimensions_length'].text()
        self.data['variation'] = helperApp.ui['project_structure']['variation'].text()
        self.data['market_language'] = helperApp.ui['project_structure']['market_language'].text()
        self.data['resolution'] = helperApp.ui['project_structure']['resolution'].text()
        self.data['frame_rate'] = helperApp.ui['project_structure']['frame_rate'].text()

    def getStructure(self):
        spacer = "   "
        frame_rate = self.data['frame_rate'].replace('.', '')
        names = [
            self.data['project_name'].upper(),
            'FINALS',
            f"{self.data['project_code']}_{self.data['dimensions_length']}",
            f"{self.data['project_code']}_{self.data['dimensions_length']}_{self.data['asset_name']}",
            f"{self.data['project_code']}_{self.data['project_type']}_{self.data['dimensions_length']}_{self.data['asset_name']}",
            f"{self.data['project_code']}_{self.data['asset_type']}_{self.data['dimensions_length']}_{self.data['asset_name']}",

            # ProRes files
            f"{self.data['frame_rate']}fps",
            f"{self.data['project_code']}_{self.data['asset_type']}_{self.data['asset_name']}_{self.data['dimensions_length']}_{self.data['variation']}_{self.data['market_language']}-TXTD_{self.data['resolution']}_{frame_rate}_ProRes.mov",
            f"{self.data['project_code']}_{self.data['asset_type']}_{self.data['asset_name']}_{self.data['dimensions_length']}_{self.data['variation']}_{self.data['market_language']}-TXTL_{self.data['resolution']}_{frame_rate}_ProRes.mov",

            # Audio splits
            'Audio_Splits',
            f"{self.data['project_code']}_{self.data['asset_type']}_{self.data['asset_name']}_{self.data['dimensions_length']}_{self.data['market_language']}_{frame_rate}_ST_Dials-1dBTP.wav",
            f"{self.data['project_code']}_{self.data['asset_type']}_{self.data['asset_name']}_{self.data['dimensions_length']}_{self.data['market_language']}_{frame_rate}_ST_FX-1dBTP.wav",
            f"{self.data['project_code']}_{self.data['asset_type']}_{self.data['asset_name']}_{self.data['dimensions_length']}_{self.data['market_language']}_{frame_rate}_ST_Mix-1dBTP.wav",
            f"{self.data['project_code']}_{self.data['asset_type']}_{self.data['asset_name']}_{self.data['dimensions_length']}_{self.data['market_language']}_{frame_rate}_ST_Music-1dBTP.wav",
            f"{self.data['project_code']}_{self.data['asset_type']}_{self.data['asset_name']}_{self.data['dimensions_length']}_{self.data['market_language']}_{frame_rate}_ST_Narr-1dBTP.wav",

            # Dia script
            'Dia_Script',
            f"{self.data['project_code']}_{self.data['asset_type']}_{self.data['asset_name']}_{self.data['dimensions_length']}_Dia_Script.doc",

            # GFX_Project
            'GFX_Project',

            # Ref file
            'Ref_File',
            f"{self.data['project_code']}_{self.data['asset_type']}_{self.data['asset_name']}_{self.data['dimensions_length']}_{self.data['variation']}_{self.data['market_language']}-TXTD_{self.data['resolution']}_{frame_rate}_H264.mov"
        ]

        for i, name in enumerate(names):
            self.helperApp.proj_struct[i][0].setText(spacer*self.helperApp.proj_struct[i][1] + name)


class ProjectHelperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'LightFilm Project Helper'
        self.dimensions = {
            'window': {
                'top': 100,
                'left': 100,
                'height': 480,
                'width': 1200
            }, 'borders': {
                'top': 10,
                'label_top': 13,
                'left': 180,
                'label_left': 15
            }, 'row_height': 30
        }
        self.helper = None
        self.tabs = QTabWidget()
        self.ui = {
            'project_structure': {}
        }

        self.setWindowTitle(self.title)
        self.setCentralWidget(self.tabs)

        self.initProjectStructureUI()

    def initProjectStructureUI(self):
        # Set layout
        layout = QHBoxLayout()
        left_layout = QGridLayout()
        right_layout = QVBoxLayout()

        inputs = [
            {'label': 'Project name:',  'id': 'project_name',   'widget': QLineEdit},
            {'label': 'Project code:',  'id': 'project_code',   'widget': QLineEdit},
            {'label': 'Project type:',  'id': 'project_type',   'widget': QComboBox, 'options': ['Social_Media', 'TV']},
            {'label': 'Asset name:',    'id': 'asset_name',     'widget': QLineEdit},
            {'label': 'Asset type:',    'id': 'asset_type',     'widget': QComboBox, 'options': ['1x1_Newsfeed', '4x5_Newsfeed', '9x16_Vertical']},
            {'label': 'Dimensions/video length:', 'id': 'dimensions_length', 'widget': QLineEdit},
            {'label': 'Variation:',     'id': 'variation',      'widget': QLineEdit},
            {'label': 'Market and language:', 'id': 'market_language', 'widget': QLineEdit, 'default': 'OV-en-OV'},
            {'label': 'Resolution:',    'id': 'resolution',     'widget': QLineEdit},
            {'label': 'Frame rate:',    'id': 'frame_rate',     'widget': QLineEdit}
        ]

        for i, item in enumerate(inputs):
            label = QLabel()
            label.setText(item['label'])
            left_layout.addWidget(label, i, 0)

            inp = item['widget']()
            if item['widget'] is QLineEdit and 'default' in item:
                inp.setText(item['default'])
            elif item['widget'] is QComboBox:
                inp.addItems(item['options'])

            self.ui['project_structure'][item['id']] = inp
            left_layout.addWidget(inp, i, 1)

        # Generate filenames button
        button = QPushButton('Generate filenames')
        button.clicked.connect(self.getProjectStructure)
        left_layout.addWidget(button, len(inputs), 0, 1, 2)

        layout.addLayout(left_layout)

        # Project structure labels
        spacers = [0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 7, 7, 7, 7, 7, 6, 7, 6, 6, 7]
        self.proj_struct = []
        for i, s in enumerate(spacers):
            label = QLabel('')
            label.setFont(QFont('Monospace', 8))
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.proj_struct += [(label, s)]
            right_layout.addWidget(label)

        # Adding tab to main window
        layout.addLayout(right_layout)
        widget = QWidget()
        widget.setLayout(layout)
        self.tabs.addTab(widget, 'Project Structure')

    def getProjectStructure(self):
        self.helper = ProjectHelper(self)
        self.helper.getStructure()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ProjectHelperApp()
    window.show()
    window.raise_()

    sys.exit(app.exec_())

