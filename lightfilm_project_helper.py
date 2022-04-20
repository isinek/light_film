import sys
from os.path import exists

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QFileDialog
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QPushButton, QAction, QListWidget, QListWidgetItem
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
        self.helper = None
        self.tabs = QTabWidget()
        self.ui = {
            'project_structure': {},
            'move_project': {},
            'config': {}
        }
        self.config_path = './main.cfg'
        self.config = {
            'project_type': {'label': 'Project type:',   'options': []},
            'asset_type':   {'label': 'Asset type:',     'options': []}
        }

        self.setWindowTitle(self.title)
        self.setCentralWidget(self.tabs)

        # Init UI
        self.initProjectStructureUI()
        self.initMoveProjectUI()
        self.initConfigUI()

        # Load config
        self.loadConfigFile()

    def loadConfigFile(self):
        # Check if config file exists
        if not exists(self.config_path):
            with open(self.config_path, 'w') as config_file:
                config_file.write("project_type:" + ','.join(['Social_Media', 'TV']) + "\n")
                config_file.write("asset_type:" + ','.join(['1x1_Newsfeed', '4x5_Newsfeed', '9x16_Vertical']) + "\n")
        with open(self.config_path, 'r') as config_file:
            for line in config_file:
                line = line.replace("\n", '')
                id, options = line.split(':')
                self.config[id]['options'] = sorted(options.split(','))
        self.refreshLists()

    def saveConfigFile(self):
        with open(self.config_path, 'w') as config_file:
            for c in self.config:
                config_file.write(f"{c}:{','.join(self.config[c]['options'])}\n")

    def openFileDialog(self):
        directory = QFileDialog.getExistingDirectory(self, 'Project root', '')
        if directory:
            self.ui['move_project']['project_root_dir'].setText(directory)

    def initMoveProjectUI(self):
        # Set layout
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        # Label
        label = QLabel()
        label.setText('Project root path:')
        top_layout.addWidget(label)

        # Textbox with root path value
        textbox = QLineEdit()
        top_layout.addWidget(textbox)
        self.ui['move_project']['project_root_dir'] = textbox

        # File dialog button
        button = QPushButton('Search...')
        button.clicked.connect(self.openFileDialog)
        top_layout.addWidget(button)

        layout.addLayout(top_layout)
        layout.addStretch()

        # Add new tab
        widget = QWidget()
        widget.setLayout(layout)
        self.tabs.addTab(widget, 'Move Project')

    def refreshLists(self):
        # Clear and fill again all combo boxes and lists
        for c in self.config:
            for tab in self.ui:
                if c in self.ui[tab] and isinstance(self.ui[tab][c], QComboBox):
                    self.ui[tab][c].clear()
                    self.ui[tab][c].addItems(self.config[c]['options'])
                elif c in self.ui[tab] and isinstance(self.ui[tab][c], QListWidget):
                    self.ui[tab][c].clear()
                    for item in self.config[c]['options']:
                        self.ui[tab][c].addItem(QListWidgetItem(item))

    def initConfigUI(self):
        # Set layout
        layout = QGridLayout()

        for i, item in enumerate(self.config):
            # Label
            label = QLabel()
            label.setText(self.config[item]['label'])
            label.setAlignment(Qt.AlignTop)
            layout.addWidget(label, i, 0)

            # Empty list
            options = QListWidget()
            layout.addWidget(options, i, 1)
            self.ui['config'][item] = options

            input_layout = QVBoxLayout()

            # Textbox for adding options
            inp = QLineEdit()
            input_layout.addWidget(inp)
            self.ui['config'][item + '_textbox'] = inp

            # Add option button
            add = QPushButton('Add item')
            add.clicked.connect(self.addListItem)
            input_layout.addWidget(add)
            self.ui['config'][item + '_add_button'] = add

            # Remove selected option
            remove = QPushButton('Remove item')
            remove.clicked.connect(self.removeListItem)
            input_layout.addWidget(remove)
            self.ui['config'][item + '_remove_button'] = remove

            # Add stretch to bottom to move everything to top
            input_layout.addStretch()
            layout.addLayout(input_layout, i, 2)

        # Save configuration button
        save = QPushButton('Save configuration')
        save.clicked.connect(self.saveConfigFile)
        layout.addWidget(save, len(self.config), 2)

        # Add new tab
        widget = QWidget()
        widget.setLayout(layout)
        self.tabs.addTab(widget, 'Configuration')

    def addListItem(self):
        for btn_id in self.ui['config']:
            # Find clicked button
            if not self.ui['config'][btn_id] is self.sender():
                continue
            textbox_id = btn_id.replace('add_button', 'textbox')
            list_id = btn_id.replace('_add_button', '')
            if len(self.ui['config'][textbox_id].text()):
                # Add new item to config
                self.config[list_id]['options'] = sorted(self.config[list_id]['options'] + [self.ui['config'][textbox_id].text()])
            break
        self.refreshLists()

    def removeListItem(self):
        for btn_id in self.ui['config']:
            # Find clicked button
            if not self.ui['config'][btn_id] is self.sender():
                continue
            textbox_id = btn_id.replace('remove_button', 'textbox')
            list_id = btn_id.replace('_remove_button', '')
            selected = self.ui['config'][list_id].selectedItems()
            for item in selected:
                # Set textbox value to removed item
                self.ui['config'][textbox_id].setText(item.text())
                # Remove selected item
                self.config[list_id]['options'].remove(item.text())
            break
        self.refreshLists()

    def initProjectStructureUI(self):
        # Set layout
        layout = QHBoxLayout()
        left_layout = QGridLayout()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(5, 10, 5, 10)

        # Define all input fields
        inputs = [
            {'label': 'Project name:',  'id': 'project_name',   'widget': QLineEdit},
            {'label': 'Project code:',  'id': 'project_code',   'widget': QLineEdit},
            {'label': 'Project type:',  'id': 'project_type',   'widget': QComboBox},
            {'label': 'Asset name:',    'id': 'asset_name',     'widget': QLineEdit},
            {'label': 'Asset type:',    'id': 'asset_type',     'widget': QComboBox},
            {'label': 'Dimensions/video length:', 'id': 'dimensions_length', 'widget': QLineEdit},
            {'label': 'Variation:',     'id': 'variation',      'widget': QLineEdit},
            {'label': 'Market and language:', 'id': 'market_language', 'widget': QLineEdit, 'default': 'OV-en-OV'},
            {'label': 'Resolution:',    'id': 'resolution',     'widget': QLineEdit},
            {'label': 'Frame rate:',    'id': 'frame_rate',     'widget': QLineEdit}
        ]

        for i, item in enumerate(inputs):
            # label
            label = QLabel()
            label.setText(item['label'])
            left_layout.addWidget(label, i, 0)

            # Textbox or combo box
            inp = item['widget']()
            if item['widget'] is QLineEdit and 'default' in item:
                inp.setText(item['default'])
            self.ui['project_structure'][item['id']] = inp
            left_layout.addWidget(inp, i, 1)

        # Generate filenames button
        button = QPushButton('Generate filenames')
        button.setDefault(True)
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

    def validateProjectStructureFields(self):
        for item in self.ui['project_structure']:
            # If any textbox is empty return False
            if isinstance(self.ui['project_structure'][item], QLineEdit) and \
                        not len(self.ui['project_structure'][item].text()):
                return False
        return True

    def getProjectStructure(self):
        if not self.validateProjectStructureFields():
            return

        self.helper = ProjectHelper(self)
        self.helper.getStructure()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ProjectHelperApp()
    window.show()
    window.raise_()

    sys.exit(app.exec_())

