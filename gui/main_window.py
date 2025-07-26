from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QSplitter, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QFont

from gui.upload_widget import UploadWidget
from gui.analysis_widget import AnalysisWidget
from gui.results_widget import ResultsWidget
from gui.guide_widget import GuideWidget
from utils.app_state import AppState
from gui.styling import AppStyles

class MainWindow(QMainWindow):
    """Main application window for the Spring Change Detection app."""
    
    def __init__(self, state: AppState):
        super().__init__()
        
        # Store the application state
        self.state = state
        
        # Setup UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle("Spring Change Detection")
        self.setWindowIcon(QIcon("resources/icons/car_icon.png"))
        self.setMinimumSize(1200, 800)
        
        # Apply dark mode style
        self.setStyleSheet(AppStyles.DARK_MODE_STYLE)
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for sidebar and content
        splitter = QSplitter(Qt.Horizontal)
        
        # Create sidebar
        sidebar_frame = QFrame()
        sidebar_frame.setFrameShape(QFrame.StyledPanel)
        sidebar_frame.setStyleSheet(AppStyles.SIDEBAR_STYLE)
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(15)
        
        # Add title to sidebar
        sidebar_title = QLabel("🚗 Spring Change Detection")
        sidebar_title.setFont(QFont("Arial", 14, QFont.Bold))
        sidebar_title.setStyleSheet(AppStyles.SIDEBAR_TITLE_STYLE)
        sidebar_layout.addWidget(sidebar_title)
        
        # Add workflow section
        workflow_label = QLabel("🚀 Project Workflow")
        workflow_label.setFont(QFont("Arial", 12, QFont.Bold))
        workflow_label.setStyleSheet(AppStyles.SIDEBAR_TITLE_STYLE)
        sidebar_layout.addWidget(workflow_label)
        
        # Create workflow buttons
        self.guide_button = self.create_workflow_button("📖 Guide", -1)
        self.upload_button = self.create_workflow_button("📁 Upload Files", 0)
        self.analysis_button = self.create_workflow_button("🔍 Analysis", 1)
        self.results_button = self.create_workflow_button("📊 Results", 2)
        
        sidebar_layout.addWidget(self.guide_button)
        sidebar_layout.addWidget(self.upload_button)
        sidebar_layout.addWidget(self.analysis_button)
        sidebar_layout.addWidget(self.results_button)
        
        # Add spacer
        sidebar_layout.addStretch()
        
        # Add about section
        about_label = QLabel("ℹ️ About Project")
        about_label.setFont(QFont("Arial", 12, QFont.Bold))
        about_label.setStyleSheet(AppStyles.SIDEBAR_TITLE_STYLE)
        sidebar_layout.addWidget(about_label)
        
        about_text = QLabel(
            "This application compares two PTA Excel files to detect vehicle spring changes:\n\n"
            "• 📊 Statistical Analysis\n"
            "• 🔍 Change Detection\n"  
            "• 📈 Data Visualization\n"
            "• 📋 Results Dashboard\n"
            "• 📥 Excel Export\n\n"
            "Supported Files:\n"
            "• Old PTA Excel file\n"
            "• New PTA Excel file"
        )
        about_text.setWordWrap(True)
        about_text.setStyleSheet(AppStyles.SIDEBAR_TEXT_STYLE)
        sidebar_layout.addWidget(about_text)
        
        # Create main content area with stacked widget
        self.content_widget = QStackedWidget()
        
        # Create pages
        self.guide_widget = GuideWidget(self)
        self.upload_widget = UploadWidget(self.state, self)
        self.analysis_widget = AnalysisWidget(self.state, self)
        self.results_widget = ResultsWidget(self.state, self)
        
        # Add pages to stack
        self.content_widget.addWidget(self.guide_widget)
        self.content_widget.addWidget(self.upload_widget)
        self.content_widget.addWidget(self.analysis_widget)
        self.content_widget.addWidget(self.results_widget)
        
        # Add widgets to splitter
        splitter.addWidget(sidebar_frame)
        splitter.addWidget(self.content_widget)
        
        # Set initial sizes
        splitter.setSizes([250, 950])  # Sidebar: 250px, Content: remaining space
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Set central widget
        self.setCentralWidget(central_widget)
        
        # Set initial page to guide
        self.content_widget.setCurrentIndex(0)  # Show guide first
        self.update_workflow_buttons(-1)  # Highlight guide button
    
    def create_workflow_button(self, text, index):
        """Create a styled workflow button."""
        button = QPushButton(text)
        button.setMinimumHeight(40)
        button.setCheckable(True)
        button.clicked.connect(lambda: self.on_workflow_button_clicked(index))
        return button
    
    def on_workflow_button_clicked(self, index):
        """Handle workflow button clicks."""
        # Special case for guide page
        if index == -1:
            self.content_widget.setCurrentIndex(0)  # Show guide page
            self.update_workflow_buttons(index)
            return
            
        # Check if we can navigate to the selected page
        if index == 1:  # Analysis
            if self.state.old_df is None or self.state.new_df is None:
                QMessageBox.warning(
                    self,
                    "Missing Files",
                    "Please upload both old and new PTA files before proceeding to analysis."
                )
                return  # Can't go to analysis without files
            
            # When navigating to analysis, automatically run the analysis
            if hasattr(self.content_widget.widget(index+1), 'run_analysis'):  # +1 because guide is at index 0
                self.content_widget.widget(index+1).run_analysis()
        
        if index == 2:  # Results
            if not self.state.analysis_completed:
                QMessageBox.warning(
                    self,
                    "Analysis Required",
                    "Please complete the analysis before viewing results."
                )
                return  # Can't go to results without analysis
        
        
        # Update current step
        self.state.current_step = index
        
        # Update UI - Add 1 to account for guide page
        self.content_widget.setCurrentIndex(index+1)
        self.update_workflow_buttons(index)
    
    def update_workflow_buttons(self, active_index):
        """Update the appearance of workflow buttons based on current state."""
        buttons = [self.guide_button, self.upload_button, self.analysis_button, self.results_button]
        indices = [-1, 0, 1, 2]
        
        for i, (button, idx) in enumerate(zip(buttons, indices)):
            if idx == active_index:
                button.setStyleSheet(AppStyles.ACTIVE_BUTTON_STYLE)
                button.setChecked(True)
            elif idx == -1:  # Guide button is always "completed"
                button.setStyleSheet(AppStyles.COMPLETED_BUTTON_STYLE)
                button.setChecked(False)
            elif self.is_step_completed(idx):
                button.setStyleSheet(AppStyles.COMPLETED_BUTTON_STYLE)
                button.setChecked(False)
            else:
                button.setStyleSheet(AppStyles.INACTIVE_BUTTON_STYLE)
                button.setChecked(False)
    
    def is_step_completed(self, step_index):
        """Check if a workflow step is completed."""
        if step_index == 0:  # Upload
            return self.state.old_df is not None and self.state.new_df is not None
        elif step_index == 1:  # Analysis
            return self.state.analysis_completed
        return False
    
    def navigate_to_step(self, step_index):
        """Programmatically navigate to a workflow step."""
        print(f"Navigating to step: {step_index}")  # Debug print
        
        try:
            # Special case for guide page
            if step_index == -1:  # Guide
                self.content_widget.setCurrentIndex(0)
                self.update_workflow_buttons(step_index)
                return
                
            # Handle step restrictions
            if step_index == 1:  # Analysis
                if self.state.old_df is None or self.state.new_df is None:
                    QMessageBox.warning(
                        self,
                        "Missing Files",
                        "Please upload both old and new PTA files before proceeding to analysis."
                    )
                    return
                
                # Run analysis on the analysis widget
                analysis_widget = self.content_widget.widget(step_index + 1)
                if hasattr(analysis_widget, 'run_analysis'):
                    analysis_widget.run_analysis()
                    
            elif step_index == 2:  # Results
                if not self.state.analysis_completed:
                    QMessageBox.warning(
                        self,
                        "Analysis Required",
                        "Please complete the analysis before viewing results."
                    )
                    return
                    
            
            # Update state
            self.state.current_step = step_index
            
            # Set visible widget (+1 because guide is at index 0)
            self.content_widget.setCurrentIndex(step_index + 1)
            
            # Update buttons
            self.update_workflow_buttons(step_index)
            
        except Exception as e:
            print(f"Error in navigation: {str(e)}")
            QMessageBox.critical(self, "Navigation Error", f"An error occurred while navigating: {str(e)}")
