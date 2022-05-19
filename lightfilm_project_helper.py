import sys
from datetime import datetime
from os import mkdir, rename, replace
from os.path import exists
from glob import glob
from re import match, search
from distutils.log import ERROR, INFO, WARN
import pickle

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt


class ProjectHelper():
    def __init__(self, app):
        self.app = app
        self.config_path = './main.cfg'
        self.config = {
            'project_type': {'label': 'Project type:',  'options': []},
            'asset_type':   {'label': 'Asset type:',    'options': []},
            'dimensions_length': {'label': 'Dimensions/video length:',    'options': []},
            'variation':    {'label': 'Variation:',     'options': []},
            'resolution':   {'label': 'Resolution:',    'options': []},
            'frame_rate':   {'label': 'Frame rate:',    'options': []}
        }

        self.default_project_data = {
            'finals_dir': 'FINALS',
            'audio_splits_dir': 'Audio_splits',
            'dia_scripts_dir': 'Dia_scripts',
            'gfx_project_dir': 'GFX_Project',
            'ref_file_dir': 'Ref_File'
        }

        self.project_structure = {
            "{project_name}": {
                "{finals_dir}": {
                    "{project_code}_{dimensions_length}": {
                        "{project_code}_{dimensions_length}_{asset_name}": {
                            "{project_code}_{project_type}_{dimensions_length}_{asset_name}": {
                                "{project_code}_{asset_type}_{dimensions_length}_{asset_name}": {
                                    "{frame_rate}fps": [
                                        "{project_code}_{asset_type}_{asset_name}_{dimensions_length}_{variation}_{market_language}-TXTD_{resolution}_{frame_rate_short}_ProRes.mov",
                                        "{project_code}_{asset_type}_{asset_name}_{dimensions_length}_{variation}_{market_language}-TXTL_{resolution}_{frame_rate_short}_ProRes.mov"
                                    ],
                                    "{audio_splits_dir}": [
                                        "{project_code}_{asset_type}_{asset_name}_{dimensions_length}_{market_language}_{frame_rate_short}_ST_Dials-1dBTP.wav",
                                        "{project_code}_{asset_type}_{asset_name}_{dimensions_length}_{market_language}_{frame_rate_short}_ST_FX-1dBTP.wav",
                                        "{project_code}_{asset_type}_{asset_name}_{dimensions_length}_{market_language}_{frame_rate_short}_ST_Mix-1dBTP.wav",
                                        "{project_code}_{asset_type}_{asset_name}_{dimensions_length}_{market_language}_{frame_rate_short}_ST_Music-1dBTP.wav",
                                        "{project_code}_{asset_type}_{asset_name}_{dimensions_length}_{market_language}_{frame_rate_short}_ST_Narr-1dBTP.wav"
                                    ],
                                    "{dia_scripts_dir}": [
                                        "{project_code}_{asset_type}_{asset_name}_{dimensions_length}_Dia_Script.doc"
                                    ],
                                    "{gfx_project_dir}": [],
                                    "{ref_file_dir}": [
                                        "{project_code}_{asset_type}_{asset_name}_{dimensions_length}_{variation}_{market_language}-TXTD_{resolution}_{frame_rate_short}_H264.mp4"
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }

        self.log_path = './log.log'

    def log(self, msg, log_level):
        log_level_str = 'INFO'
        if log_level == ERROR:
            log_level_str = 'ERROR'
        if log_level == WARN:
            log_level_str = 'WARNING'

        timestamp = 'T'.join(str(datetime.now()).split(' '))
        with open(self.log_path, 'a') as log_file:
            log_file.write(f"[{timestamp}] {log_level_str}: {msg}\n")

    def loadConfigFile(self):
        # Create config file if it does not exist
        if not exists(self.config_path):
            with open(self.config_path, 'wb') as config_file:
                pickle.dump(self.config, config_file)

        with open(self.config_path, 'rb') as config_file:
            self.config = pickle.load(config_file)

    def saveConfigFile(self):
        with open(self.config_path, 'wb') as config_file:
            pickle.dump(self.config, config_file)

    def loadExternalConfigFile(self):
        cfg_path = QFileDialog.getOpenFileName(self.app, 'Load config file', '', 'Config file (*.cfg)')

        if exists(cfg_path[0]):
            with open(cfg_path[0], 'rb') as config_file:
                self.config = pickle.load(config_file)
        self.app.refreshLists()

    def exportConfigFile(self):
        cfg_path = QFileDialog.getSaveFileName(self.app, 'Save config file', 'lightfilm_project_helper.cfg', 'Config file (*.cfg)')

        if len(cfg_path[0]):
            with open(cfg_path[0], 'wb') as config_file:
                pickle.dump(self.config, config_file)

    def getStructureFromUI(self):
        data = self.default_project_data.copy()
        data_fields =  [
            'project_name',
            'project_code',
            'project_type',
            'asset_name',
            'asset_type',
            'dimensions_length',
            'variation',
            'market_language',
            'resolution',
            'frame_rate',
            'frame_rate_short'
        ]
        # Get data from all textboxes and combo boxes
        for field in data_fields:
            if field + '_tb' in self.app.ui['project_structure']:
                data[field] = self.app.ui['project_structure'][field + '_tb'].text()
            elif field + '_cb' in self.app.ui['project_structure']:
                data[field] = self.app.ui['project_structure'][field + '_cb'].currentText()
            if field == 'frame_rate':
                data['frame_rate_short'] = data['frame_rate'].replace('.', '')

        # Convert project structure to filenames
        new_struct = {}
        q = [(self.project_structure, new_struct)]
        while len(q):
            curr_struct, new_curr_struct = q.pop(0)

            if type(curr_struct) is dict:
                # If current directory contains directories, add them to queue
                sorted_lbls = sorted([x for x in curr_struct], reverse=True)
                for lbl_format in sorted_lbls:
                    lbl = lbl_format.format(**data)
                    if not lbl in new_curr_struct:
                        if type(curr_struct[lbl_format]) is dict:
                            new_curr_struct[lbl] = {}
                        else:
                            new_curr_struct[lbl] = []
                    q = [(curr_struct[lbl_format], new_curr_struct[lbl])] + q
            else:
                # If current directory contains files, add them as sorted list
                new_curr_struct += [x.format(**data) for x in curr_struct if not x in new_curr_struct]
                new_curr_struct.sort()

        return new_struct

    def parseFilename(self, filename):
        data = self.default_project_data.copy()

        # Get project code if exists
        if not match(r"[\w]{3}_.*", filename):
            return None
        data['project_code'] = filename[:3]
        filename = filename[4:]

        # Get asset type
        asset_type_options_regex = "|".join([o[0] for o in self.config['asset_type']['options']])
        if not match("^(" + asset_type_options_regex + ").*", filename):
            return None
        data['asset_type'] = search("(" + asset_type_options_regex + ")", filename).group(1)
        filename = filename[len(data['asset_type']) + 1:]

        # Find project type from asset type
        for at, pt in self.config['asset_type']['options']:
            if at == data['asset_type']:
                data['project_type'] = pt
                break
        if not 'project_type' in data:
            return None

        # Get asset name and dimension/video length
        filename_parts = filename.split('_')
        data['asset_name'] = filename_parts[0]
        data['dimensions_length'] = filename_parts[1]

        if (filename_parts[2] + filename_parts[3]).startswith('DiaScript'):
            data['file_type'] = 'dia_script'
            return data
        elif filename_parts[2] in self.config['variation']['options']:
            data['variation'] = filename_parts[2]
            data['market_language'] = filename_parts[3][:-5]
            data['resolution'] = filename_parts[4]
            data['frame_rate_short']  = data['frame_rate'] = filename_parts[5]
            if data['frame_rate_short'] == '2398':
                data['frame_rate'] = '23.98'
            data['file_type'] = 'mov_' + filename_parts[3][-4:].lower() + '_' + filename_parts[6].split('.')[0].lower()
        else:
            data['market_language'] = filename_parts[2]
            data['frame_rate_short']  = data['frame_rate'] = filename_parts[3]
            if data['frame_rate_short'] == '2398':
                data['frame_rate'] = '23.98'
            data['file_type'] = 'audio_' + filename_parts[5].split('-')[0].lower()

        return data

    def moveFilesFromExportDir(self, export_dir, destination_dir):
        messages = []
        if not exists(export_dir):
            messages += [('Export directory does not exist!', ERROR)]
            self.log(messages[-1][0], messages[-1][1])
        if not exists(destination_dir):
            messages += [('Destination directory does not exist!', ERROR)]
            self.log(messages[-1][0], messages[-1][1])
        if len(messages):
            return messages

        # Get all files that need to be moved
        export_files = sorted(glob(export_dir + '/*'), key=lambda x: -len(x))
        export_filenames = []
        paths = []
        for export_file in export_files:
            # Parse filename
            export_filename = export_file.split('/')[-1]
            export_filenames += [export_filename]
            parsed_data = self.parseFilename(export_filename)
            if parsed_data is None:
                messages += [('Could not parse filename ' + export_filename, ERROR)]
                self.log(messages[-1][0], messages[-1][1])
                continue

            # If file type is mov, it should contain all data, so use it
            # to create project structure and directories
            if parsed_data['file_type'].startswith('mov'):
                q = [(self.project_structure['{project_name}'], destination_dir)]
                while len(q):
                    curr, p = q.pop(0)

                    for lbl_format in curr:
                        curr_path = f"{p}/{lbl_format.format(**parsed_data)}"
                        if not exists(curr_path):
                            mkdir(curr_path)
                            messages += [('New directory created: ' + curr_path, INFO)]
                            self.log(messages[-1][0], messages[-1][1])

                        if type(curr[lbl_format]) is dict:
                            q = [(curr[lbl_format], curr_path)] + q
                        else:
                            for filename_format in curr[lbl_format]:
                                file_path = f"{curr_path}/{filename_format.format(**parsed_data)}"
                                if not file_path in paths:
                                    paths += [file_path]

            path = None
            for p in paths:
                if export_filename == p.split('/')[-1]:
                    path = p
                    break

            if path is None:
                messages += [(f"Can't find a project for file {export_file}!", WARN)]
                continue

            overwrite_file = None
            # If file exists in destination directory, ask if it should be overwriten
            if exists(path):
                qm = QMessageBox()
                overwrite_file = qm.question(self.app, '', f"File {path} already exist!\n Do you want to overwrite it?", qm.Yes | qm.No)

            # Move file or print message
            if not exists(path):
                rename(export_file, path)
                messages += [(f"File {export_filename} moved to {path}", INFO)]
                self.log(messages[-1][0], messages[-1][1])
            elif exists(path) and overwrite_file == qm.Yes:
                replace(export_file, path)
                messages += [(f"File {export_filename} overwrited {path}", INFO)]
                self.log(messages[-1][0], messages[-1][1])
            else:
                messages += [(f"File {export_filename} was not moved!", ERROR)]
                self.log(messages[-1][0], messages[-1][1])

        for p in paths:
            curr_file = p.split('/')[-1]
            if not curr_file in export_filenames:
                messages += [(f"File {curr_file} is part of the project, but was not exported.", WARN)]
                self.log(messages[-1][0], messages[-1][1])

        return messages


class Projectapp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'LightFilm Project Helper'
        self.helper = None
        self.tabs = QTabWidget()
        self.ui = {
            'project_structure': {
                'data': {}
            },
            'move_project': {},
            'config': {}
        }
        self.helper = ProjectHelper(self)

        self.setWindowTitle(self.title)
        self.setMinimumWidth(800)
        self.setCentralWidget(self.tabs)

        # Init UI
        self.initProjectStructureUI()
        self.initMoveProjectUI()
        self.initConfigUI()

        self.helper.loadConfigFile()
        self.refreshLists()

    def refreshLists(self):
        # Clear and fill again all combo boxes and lists
        for x in self.helper.config:
            for tab in self.ui:
                cb = x + '_cb'
                lst = x + '_list'
                if cb  in self.ui[tab] and isinstance(self.ui[tab][cb], QComboBox):
                    selected = self.ui[tab][cb].currentIndex()
                    self.ui[tab][cb].clear()
                    if x in ['asset_type', 'resolution']:
                        self.ui[tab][cb].addItems([item[0] for item in self.helper.config[x]['options']])
                    else:
                        self.ui[tab][cb].addItems(self.helper.config[x]['options'])
                    if 0 <= selected < len(self.helper.config[x]['options']):
                        self.ui[tab][cb].setCurrentIndex(selected)
                    else:
                        self.ui[tab][cb].setCurrentIndex(0)
                if lst in self.ui[tab] and isinstance(self.ui[tab][lst], QListWidget):
                    self.ui[tab][lst].clear()
                    for item in self.helper.config[x]['options']:
                        if x in ['asset_type', 'resolution']:
                            self.ui[tab][lst].addItem(QListWidgetItem(f"{item[0]} ({item[1]})"))
                        else:
                            self.ui[tab][lst].addItem(QListWidgetItem(item))

        if self.ui['project_structure']['project_type_cb'].count():
            self.projectTypeSelectionChanged(self.ui['project_structure']['project_type_cb'].currentText())
        elif self.ui['project_structure']['asset_type_cb'].count():
            self.assetTypeSelectionChanged(self.ui['project_structure']['asset_type_cb'].currentText())

    #########################
    # Project Structure tab #
    #########################
    def initProjectStructureUI(self):
        # Set layout
        layout = QHBoxLayout()
        left_layout = QGridLayout()
        right_scroll_area = QScrollArea()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(15, 10, 15, 10)
        right_layout.addStretch()
        self.ui['project_structure']['right_layout'] = right_layout

        # Define all input fields
        inputs = [
            {'label': 'Project name:',  'id': 'project_name_tb',    'widget': QLineEdit},
            {'label': 'Project code:',  'id': 'project_code_tb',    'widget': QLineEdit},
            {'label': 'Project type:',  'id': 'project_type_cb',    'widget': QComboBox,    'action': self.projectTypeSelectionChanged},
            {'label': 'Asset name:',    'id': 'asset_name_tb',      'widget': QLineEdit},
            {'label': 'Asset type:',    'id': 'asset_type_cb',      'widget': QComboBox,    'action': self.assetTypeSelectionChanged},
            {'label': 'Dimensions/video length:', 'id': 'dimensions_length_cb', 'widget': QComboBox},
            {'label': 'Variation:',     'id': 'variation_cb',       'widget': QComboBox},
            {'label': 'Market and language:', 'id': 'market_language_tb',       'widget': QLineEdit, 'default': 'OV-en-OV'},
            {'label': 'Resolution:',    'id': 'resolution_cb',      'widget': QComboBox},
            {'label': 'Frame rate:',    'id': 'frame_rate_cb',      'widget': QComboBox}
        ]

        for i, item in enumerate(inputs):
            # label
            label = QLabel()
            label.setText(item['label'])
            label.setMaximumWidth(175)
            left_layout.addWidget(label, i, 0)

            # Textbox or combo box
            inp = item['widget']()
            if item['widget'] is QComboBox and 'action' in item:
                inp.currentTextChanged.connect(item['action'])
            elif item['widget'] is QLineEdit and 'default' in item:
                inp.setText(item['default'])
            inp.setMaximumWidth(175)
            self.ui['project_structure'][item['id']] = inp
            left_layout.addWidget(inp, i, 1)

        # Add project button
        button = QPushButton('Add project')
        button.setDefault(True)
        button.clicked.connect(self.addToProjectStructure)
        left_layout.addWidget(button, len(inputs), 0, 1, 2)

        # Clear projects button
        button = QPushButton('Clear projects')
        button.setDefault(True)
        button.clicked.connect(self.clearProjectStructure)
        left_layout.addWidget(button, len(inputs) + 1, 0, 1, 2)

        left_layout.setRowStretch(left_layout.rowCount(), 1)
        layout.addLayout(left_layout)

        # Making right layout scrollable
        widget = QWidget()
        widget.setLayout(right_layout)
        right_scroll_area.setWidget(widget)
        right_scroll_area.setWidgetResizable(True)
        layout.addWidget(right_scroll_area)

        # Adding tab to main window
        widget = QWidget()
        widget.setLayout(layout)
        self.tabs.addTab(widget, 'Project Structure')

    def projectTypeSelectionChanged(self, value):
        self.ui['project_structure']['asset_type_cb'].clear()
        self.ui['project_structure']['asset_type_cb'].addItems([x[0] for x in self.helper.config['asset_type']['options'] if x[1] == value])

    def assetTypeSelectionChanged(self, value):
        self.ui['project_structure']['resolution_cb'].clear()
        self.ui['project_structure']['resolution_cb'].addItems([x[0] for x in self.helper.config['resolution']['options'] if x[1] == value])

    def validateProjectStructureFields(self):
        for item in self.ui['project_structure']:
            # If any textbox is empty return False
            if isinstance(self.ui['project_structure'][item], QLineEdit) and \
                        not len(self.ui['project_structure'][item].text()):
                return False
        return True

    def addToProjectStructure(self):
        if not self.validateProjectStructureFields():
            return

        structure = self.helper.getStructureFromUI()
        q = [(structure, self.ui['project_structure']['data'])]
        while len(q):
            curr_struct, new_curr_struct = q.pop(0)

            if type(curr_struct) is dict:
                # If current directory contains directories, add them to queue
                sorted_lbls = sorted([x for x in curr_struct], reverse=True)
                for lbl in sorted_lbls:
                    if not lbl in new_curr_struct:
                        if type(curr_struct[lbl]) is dict:
                            new_curr_struct[lbl] = {}
                        else:
                            new_curr_struct[lbl] = []
                    q = [(curr_struct[lbl], new_curr_struct[lbl])] + q
            else:
                # If current directory contains files, add them as sorted list
                new_curr_struct += [x for x in curr_struct if not x in new_curr_struct]
                new_curr_struct.sort()

        self.refreshProjectStructure()

    def clearProjectStructure(self):
        self.ui['project_structure']['data'] = {}

        self.refreshProjectStructure()

    def refreshProjectStructure(self):
        right_layout = self.ui['project_structure']['right_layout']
        space_size = 20

        # Clear right layout
        n_widgets = right_layout.count() - 1
        for i in range(n_widgets - 1, -1, -1):
            right_layout.itemAt(i).widget().deleteLater()

        # Add a label for each direcotry/file
        q = [(self.ui['project_structure']['data'], None, -1)]
        while len(q):
            curr, lbl_text, space = q.pop(0)
            if not lbl_text is None:
                # Add directory label
                label = QLabel(lbl_text)
                label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                label.setStyleSheet('margin-left: ' + str(space*space_size) + 'px')
                right_layout.insertWidget(right_layout.count() - 1, label)

            if type(curr) is dict:
                # If current directory contains directories, add them to queue
                sorted_lbls = sorted([x for x in curr], reverse=True)
                for lbl in sorted_lbls:
                    q = [(curr[lbl], lbl, space + 1)] + q
            else:
                # If current directory contains files, add labels
                for x in curr:
                    label = QLabel(x)
                    label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                    label.setStyleSheet('margin-left: ' + str((space + 1)*space_size) + 'px')
                    right_layout.insertWidget(right_layout.count() - 1, label)

    ####################
    # Move Project tab #
    ####################
    def initMoveProjectUI(self):
        # Set layout
        layout = QVBoxLayout()
        input_layout = QGridLayout()

        inputs = [
            {'label': 'Export directory:',  'id': 'export_directory',   'widget': QLineEdit},
            {'label': 'Project root:',  'id': 'project_root',   'widget': QLineEdit}
        ]

        for i, item in enumerate(inputs):
            # label
            label = QLabel()
            label.setText(item['label'])
            input_layout.addWidget(label, i, 0)

            # Textbox
            inp = item['widget']()
            if item['widget'] is QLineEdit and 'default' in item:
                inp.setText(item['default'])
            input_layout.addWidget(inp, i, 1)
            self.ui['move_project'][item['id'] + '_tb'] = inp

            # File dialog button
            btn = QPushButton('Search...')
            btn.clicked.connect(self.openFileDialog)
            input_layout.addWidget(btn, i, 2)
            self.ui['move_project'][item['id'] + '_btn'] = btn

        # Move files button
        btn = QPushButton('Move files')
        btn.clicked.connect(self.moveProject)
        input_layout.addWidget(btn, len(inputs), 2)

        layout.addLayout(input_layout)

        # Message box
        scroll_area = QScrollArea()
        messages_layout = QVBoxLayout()
        messages_layout.addStretch()
        widget = QWidget()
        widget.setLayout(messages_layout)
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        self.ui['move_project']['messages'] = messages_layout

        # Add new tab
        widget = QWidget()
        widget.setLayout(layout)
        self.tabs.addTab(widget, 'Move Project')

    def openFileDialog(self):
        directory = QFileDialog.getExistingDirectory(self, 'Find directory', '')

        if directory:
            for btn_id in self.ui['move_project']:
                # Find clicked button
                if not self.ui['move_project'][btn_id] is self.sender():
                    continue

                textbox_id = btn_id.replace('_btn', '_tb')
                self.ui['move_project'][textbox_id].setText(directory)
                break

    def moveProject(self):
        export_dir = self.ui['move_project']['export_directory_tb'].text()
        project_root = self.ui['move_project']['project_root_tb'].text()

        if export_dir == '' or project_root == '':
            return

        # Move files
        messages = self.helper.moveFilesFromExportDir(export_dir, project_root)

        # Write messages to message box after clearing
        message_box = self.ui['move_project']['messages']
        for message in messages:
            label = QLabel(message[0])
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            if message[1] == ERROR:
                label.setStyleSheet('color: red')
            elif message[1] == WARN:
                label.setStyleSheet('color: orange')
            message_box.insertWidget(message_box.count() - 1, label)

    ##############
    # Config tab #
    ##############
    def initConfigUI(self):
        # Set layout
        layout = QGridLayout()
        layout.setVerticalSpacing(10)

        for i, item in enumerate(self.helper.config):
            # Label
            label = QLabel()
            label.setText(self.helper.config[item]['label'])
            label.setAlignment(Qt.AlignTop)
            layout.addWidget(label, i, 0)

            # Empty list
            options = QListWidget()
            layout.addWidget(options, i, 1)
            self.ui['config'][item + '_list'] = options

            input_layout = QVBoxLayout()

            # Textbox for adding options
            inp = QLineEdit()
            input_layout.addWidget(inp)
            self.ui['config'][item + '_tb'] = inp

            if item == 'asset_type':
                # Add combo box for asset type parent (project type)
                cb = QComboBox()
                input_layout.addWidget(cb)
                self.ui['config']['project_type_cb'] = cb
            elif item == 'resolution':
                # Add combo box for asset type parent (project type)
                cb = QComboBox()
                input_layout.addWidget(cb)
                self.ui['config']['asset_type_cb'] = cb

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
        btn = QPushButton('Save configuration')
        btn.clicked.connect(self.helper.saveConfigFile)
        layout.addWidget(btn, layout.count(), 2)

        # Load configuration button
        btn = QPushButton('Load configuration file')
        btn.clicked.connect(self.helper.loadExternalConfigFile)
        layout.addWidget(btn, layout.count(), 2)

        # Export configuration button
        btn = QPushButton('Export configuration file')
        btn.clicked.connect(self.helper.exportConfigFile)
        layout.addWidget(btn, layout.count(), 2)

        # Add new tab
        widget = QWidget()
        widget.setLayout(layout)
        self.tabs.addTab(widget, 'Configuration')

    def addListItem(self):
        for btn_id in self.ui['config']:
            # Find clicked button
            if not self.ui['config'][btn_id] is self.sender():
                continue

            conf_id = btn_id.replace('_add_button', '')
            textbox_id = conf_id + '_tb'
            if len(self.ui['config'][textbox_id].text()):
                # Add new item to config
                options = []
                if conf_id == 'asset_type':
                    options = self.helper.config[conf_id]['options'] + [(self.ui['config'][textbox_id].text(), self.ui['config']['project_type_cb'].currentText())]
                elif conf_id == 'resolution':
                    options = self.helper.config[conf_id]['options'] + [(self.ui['config'][textbox_id].text(), self.ui['config']['asset_type_cb'].currentText())]
                else:
                    options = self.helper.config[conf_id]['options'] + [self.ui['config'][textbox_id].text()]
                self.helper.config[conf_id]['options'] = sorted(options)
            break
        self.refreshLists()

    def removeListItem(self):
        for btn_id in self.ui['config']:
            # Find clicked button
            if not self.ui['config'][btn_id] is self.sender():
                continue

            conf_id = btn_id.replace('_remove_button', '')
            textbox_id = conf_id + '_tb'
            list_id = conf_id + '_list'
            selected = self.ui['config'][list_id].selectedItems()
            for item in selected:
                # Set textbox value to removed item
                if conf_id in ['asset_type', 'resolution']:
                    it = item.text().split(' (')
                    it[1] = it[1][:-1]
                    self.helper.config[conf_id]['options'].remove(tuple(it))
                    self.ui['config'][textbox_id].setText(it[0])
                else:
                    self.helper.config[conf_id]['options'].remove(item.text())
                    self.ui['config'][textbox_id].setText(item.text())
            break
        self.refreshLists()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Projectapp()
    window.show()
    window.raise_()

    sys.exit(app.exec_())
