from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,
    QRadioButton, QButtonGroup, QFrame, QTableView, QHeaderView,
    QMessageBox, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from utils.app_state import AppState
from utils.file_handler import FileHandler
from gui.components.excel_table_model import DataFrameModel
from gui.styling import AppStyles

class FileUploadFrame(QFrame):
    """Frame for uploading a single file (either old or new)."""
    
    file_uploaded = Signal(bool, str, object)  # success, message, dataframe
    
    def __init__(self, title, file_type):
        super().__init__()
        self.title = title
        self.file_type = file_type  # "old" or "new"
        self.df = None
        self._last_file_path = None  # Store the actual file path
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {AppStyles.DARK_CARD_BG};
                border: 1px solid {AppStyles.DARK_BORDER};
                border-radius: 4px;
                padding: 15px;
            }}
            QLabel {{
                color: {AppStyles.TEXT_COLOR};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Single line compact layout for file selection
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        file_info = QLabel(f"{self.title}:")
        file_info.setFont(QFont("Arial", 11))
        file_info.setStyleSheet("color: white;")
        header_layout.addWidget(file_info)
        
        self.status_label = QLabel("No file selected")
        self.status_label.setStyleSheet("color: #888888; font-style: italic; font-size: 11px;")
        header_layout.addWidget(self.status_label, 1)  # Give more space to status
        
        self.upload_button = QPushButton("📂 Browse")
        self.upload_button.setFixedWidth(80)
        self.upload_button.setFixedHeight(30)
        self.upload_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #388E3C;
            }}
        """)
        self.upload_button.clicked.connect(self.on_upload_clicked)
        header_layout.addWidget(self.upload_button)
        
        layout.addLayout(header_layout)
        
        # Larger preview section
        self.table_view = QTableView()
        self.table_view.setMinimumHeight(400)  # Increased minimum height
        self.table_view.setMaximumHeight(500)  # Increased maximum height
        self.table_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.table_view.setStyleSheet(AppStyles.TABLE_STYLE)
        self.table_view.horizontalHeader().setVisible(False)  # Hide column headers
        self.table_view.verticalHeader().setVisible(False)   # Hide row numbers
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table_view.setVisible(False)
        layout.addWidget(self.table_view)
        
        layout.addStretch()
    
    def on_upload_clicked(self):
        """Handle file upload button click."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select PTA Excel File", 
            "", 
            "Excel Files (*.xlsx *.xls)"
        )
        
        if not file_path:
            return
        
        # Store the file path
        self._last_file_path = file_path
        
        # Process the file
        try:
            is_valid, comment, df = FileHandler.validate_excel_file(file_path, self.file_type)
            
            if is_valid:
                # Update status
                self.status_label.setText(f"✅ File loaded: {file_path.split('/')[-1]}")
                self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
                
                # Show preview
                self.df = df
                self.update_preview()
                
                # Emit signal
                self.file_uploaded.emit(True, "File uploaded successfully", df)
            else:
                self.status_label.setText(f"❌ {comment}")
                self.status_label.setStyleSheet("color: #FF5733; font-weight: bold;")
                self.table_view.setVisible(False)
                self.file_uploaded.emit(False, comment, None)
                
        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
            self.status_label.setStyleSheet("color: #FF5733; font-weight: bold;")
            self.table_view.setVisible(False)
            self.file_uploaded.emit(False, str(e), None)
    
    def update_preview(self):
        """Update the preview table with the loaded DataFrame."""
        if self.df is not None:
            model = DataFrameModel(self.df)
            self.table_view.setModel(model)
            
            # Set uniform column width for better readability
            for col in range(model.columnCount()):
                self.table_view.setColumnWidth(col, 180)  # Uniform width
            
            # Set first row (header) height slightly bigger
            self.table_view.setRowHeight(0, 35)  # Header row
            
            # Set data rows height
            for row in range(1, model.rowCount()):
                self.table_view.setRowHeight(row, 30)
            
            # Set first row (headers) to be bold using Qt's font mechanism
            self.table_view.setSortingEnabled(False)  # Disable sorting since headers are in data
            self.table_view.setVisible(True)
            
            # Make first row bold using custom delegate
            from PySide6.QtWidgets import QStyledItemDelegate
            class HeaderRowDelegate(QStyledItemDelegate):
                def initStyleOption(self, option, index):
                    super().initStyleOption(option, index)
                    if index.row() == 0:  # First row (headers)
                        font = option.font
                        font.setBold(True)
                        option.font = font
            
            self.table_view.setItemDelegate(HeaderRowDelegate())


class UploadWidget(QWidget):
    """Widget for the file upload step."""
    
    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
        self.state = state
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        # Apply dark mode style
        self.setStyleSheet(AppStyles.DARK_MODE_STYLE)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with container
        header_container = QFrame()
        header_container.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {AppStyles.PRIMARY_COLOR}, 
                    stop:0.5 #2E7D32,
                    stop:1 #1B5E20);
                border-radius: 12px;
                margin: 5px 2px 25px 2px;
        """)
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        header_label = QLabel("📁 Step 1: Upload Your Excel Files")
        header_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header_label.setStyleSheet("""
            color: white;
            padding: 20px;
            letter-spacing: 1px;
        """)
        header_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(header_label)
        
        layout.addWidget(header_container)

        # PTA Type selection with enhanced styling
        pta_type_frame = QFrame()
        pta_type_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppStyles.DARK_CARD_BG};
                border: 1px solid {AppStyles.DARK_BORDER};
                border-radius: 4px;
                padding: 10px;
            }}
            QRadioButton {{
                color: white;
                font-size: 14px;
                padding: 5px;
            }}
            QRadioButton:checked {{
                color: #4CAF50;
                font-weight: bold;
            }}
        """)
        pta_type_layout = QVBoxLayout(pta_type_frame)
        
        pta_type_label = QLabel("🚗 Select PTA Type:")
        pta_type_label.setFont(QFont("Arial", 12, QFont.Bold))
        pta_type_label.setStyleSheet("color: white; margin-bottom: 5px;")
        pta_type_layout.addWidget(pta_type_label)
        
        radio_layout = QHBoxLayout()
        
        self.vp_radio = QRadioButton("VP (Véhicules Particuliers)")
        self.vu_radio = QRadioButton("VU (Véhicules Utilitaires)")
        
        # Set default based on state
        if self.state.pta_type == "VP":
            self.vp_radio.setChecked(True)
        else:
            self.vu_radio.setChecked(True)
        
        pta_type_group = QButtonGroup(self)
        pta_type_group.addButton(self.vp_radio)
        pta_type_group.addButton(self.vu_radio)
        
        radio_layout.addWidget(self.vp_radio)
        radio_layout.addWidget(self.vu_radio)
        radio_layout.addStretch()
        
        pta_type_layout.addLayout(radio_layout)
        layout.addWidget(pta_type_frame)
        
        # Connect radio button signals
        self.vp_radio.toggled.connect(self.on_pta_type_changed)
        
        # Add spacing
        layout.addSpacing(10)
        
        # Add tabs for file upload
        from PySide6.QtWidgets import QTabWidget
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {AppStyles.DARK_BORDER};
                border-radius: 4px;
                background-color: {AppStyles.DARK_CARD_BG};
                padding: 10px;
            }}
            QTabBar::tab {{
                background-color: {AppStyles.DARK_HIGHLIGHT};
                color: {AppStyles.TEXT_COLOR};
                border: 1px solid {AppStyles.DARK_BORDER};
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {AppStyles.PRIMARY_COLOR};
                color: white;
                border-color: #388E3C;
                font-weight: bold;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: #3D3D3D;
            }}
        """)
        
        # Create file upload frames in tabs
        self.old_file_frame = FileUploadFrame("Select Old PTA File", "old")
        self.new_file_frame = FileUploadFrame("Select New PTA File", "new")
        
        self.tabs.addTab(self.old_file_frame, "📑 Old PTA File")
        self.tabs.addTab(self.new_file_frame, "📄 New PTA File")
        
        layout.addWidget(self.tabs)
        
        # Connect signals
        self.old_file_frame.file_uploaded.connect(self.on_old_file_uploaded)
        self.new_file_frame.file_uploaded.connect(self.on_new_file_uploaded)
        
        # Status and proceed section with enhanced styling
        self.status_frame = QFrame()
        self.status_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppStyles.DARK_CARD_BG};
                border: 1px solid {AppStyles.DARK_BORDER};
                border-radius: 4px;
                padding: 15px;
            }}
        """)
        status_layout = QVBoxLayout(self.status_frame)
        status_layout.setSpacing(15)
        
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setVisible(False)
        self.status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_label)
        
        self.proceed_button = QPushButton("🔍 Proceed to Analysis")
        self.proceed_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {AppStyles.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: #388E3C;
            }}
            QPushButton:pressed {{
                background-color: #1B5E20;
            }}
        """)
        self.proceed_button.setVisible(False)
        self.proceed_button.clicked.connect(self.on_proceed_clicked)
        status_layout.addWidget(self.proceed_button)
        
        layout.addWidget(self.status_frame)
        layout.addStretch()
        
        # Check if files are already loaded
        self.update_status()
    
    def on_pta_type_changed(self):
        """Handle PTA type radio button changes."""
        if self.vp_radio.isChecked():
            self.state.pta_type = "VP"
        else:
            self.state.pta_type = "VU"
    
    def on_old_file_uploaded(self, success, message, df):
        """Handle old file upload completion."""
        if success:
            self.state.old_df = df
            # Store the actual file path, not button text
            file_path = getattr(self.old_file_frame, '_last_file_path', None)
            self.state.old_file_path = file_path
        else:
            self.state.old_df = None
            self.state.old_file_path = None
            QMessageBox.warning(self, "Upload Error", message)
        
        self.update_status()
    
    def on_new_file_uploaded(self, success, message, df):
        """Handle new file upload completion."""
        if success:
            self.state.new_df = df
            # Store the actual file path, not button text
            file_path = getattr(self.new_file_frame, '_last_file_path', None)
            self.state.new_file_path = file_path
        else:
            self.state.new_df = None
            self.state.new_file_path = None
            QMessageBox.warning(self, "Upload Error", message)
        
        self.update_status()
    
    def update_status(self):
        """Update status message and proceed button visibility."""
        if self.state.old_df is not None and self.state.new_df is not None:
            self.status_label.setText("✅ Both files uploaded successfully! You can now proceed to analysis.")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            self.status_label.setVisible(True)
            self.proceed_button.setVisible(True)
        elif self.state.old_df is not None or self.state.new_df is not None:
            self.status_label.setText("📋 Please upload both files to proceed.")
            self.status_label.setStyleSheet("color: #FFC107;")
            self.status_label.setVisible(True)
            self.proceed_button.setVisible(False)
        else:
            self.status_label.setVisible(False)
            self.proceed_button.setVisible(False)
    
    def on_proceed_clicked(self):
        """Handle proceed button click."""
        # Direct parent navigation to avoid navigation issues
        if self.parent() and hasattr(self.parent(), "navigate_to_step"):
            self.parent().navigate_to_step(1)  # Navigate to analysis step
        else:
            # Direct approach if parent navigation isn't available
            if self.state.old_df is not None and self.state.new_df is not None:
                self.state.current_step = 1
                # Emit a signal that can be caught by parent
                if hasattr(self, 'parent') and hasattr(self.parent(), 'update_workflow_buttons'):
                    self.parent().update_workflow_buttons(1)
