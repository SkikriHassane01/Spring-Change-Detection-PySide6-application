from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QGridLayout, QScrollArea, QSizePolicy, QApplication
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from utils.app_state import AppState
from data_processing import generate_results_df
from gui.components.metric_card import MetricCard
from gui.styling import AppStyles

class MatplotlibCanvas(FigureCanvas):
    """A canvas for displaying matplotlib charts."""
    
    def __init__(self, width=5, height=4, dpi=100):
        # Create figure with dark background
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=AppStyles.DARK_CARD_BG)
        self.axes = self.fig.add_subplot(111)
        
        # Style improvements for dark mode
        self.axes.set_facecolor(AppStyles.DARK_CARD_BG)
        self.axes.spines['bottom'].set_color(AppStyles.DARK_BORDER)
        self.axes.spines['top'].set_color(AppStyles.DARK_BORDER)
        self.axes.spines['left'].set_color(AppStyles.DARK_BORDER)
        self.axes.spines['right'].set_color(AppStyles.DARK_BORDER)
        self.axes.tick_params(colors=AppStyles.TEXT_COLOR)
        self.axes.xaxis.label.set_color(AppStyles.TEXT_COLOR)
        self.axes.yaxis.label.set_color(AppStyles.TEXT_COLOR)
        self.axes.title.set_color(AppStyles.TEXT_COLOR)
        
        # Style improvements
        self.fig.set_tight_layout(True)
        
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(300)  # Ensure minimum height for visibility


class AnalysisWidget(QWidget):
    """Widget for the analysis step."""
    
    analysis_completed = Signal()
    
    def __init__(self, state: AppState, parent=None):
        super().__init__(parent)
        self.state = state
        self.init_ui()
        
        # Run analysis automatically if data is available and analysis wasn't completed
        if not self.state.analysis_completed and self.state.old_df is not None and self.state.new_df is not None:
            # Using a small delay to allow the UI to fully load first
            from PySide6.QtCore import QTimer
            QTimer.singleShot(100, self.run_analysis)

    def init_ui(self):
        """Initialize the user interface."""
        # Apply dark mode style
        self.setStyleSheet(AppStyles.DARK_MODE_STYLE)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header - White text on primary color
        header_label = QLabel("🔍 Step 2: Data Analysis")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setStyleSheet(f"color: white; background-color: {AppStyles.PRIMARY_COLOR}; padding: 8px; border-radius: 4px;")
        layout.addWidget(header_label)
        
        # Scroll area for analysis content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)  # Add more space between sections
        
        # Analysis Overview section
        overview_label = QLabel("📊 Analysis Overview")
        overview_label.setStyleSheet(AppStyles.SECTION_HEADER_STYLE)
        scroll_layout.addWidget(overview_label)
        
        # Metrics section
        metrics_frame = QFrame()
        metrics_layout = QGridLayout(metrics_frame)
        metrics_layout.setContentsMargins(0, 10, 0, 10)
        metrics_layout.setSpacing(10)  # Add space between metrics

        # Will be populated when analysis runs
        self.metrics_layout = metrics_layout
        scroll_layout.addWidget(metrics_frame)

        self.change_type_label = QLabel("🔄 Change Type Distribution")
        self.change_type_label.setStyleSheet(AppStyles.SECTION_HEADER_STYLE)
        scroll_layout.addWidget(self.change_type_label)

        self.change_type_container = QFrame()
        self.change_type_container.setMinimumHeight(350)
        self.change_type_layout = QVBoxLayout(self.change_type_container)
        scroll_layout.addWidget(self.change_type_container)
        
        # Add Moteur list section
        self.moteur_label = QLabel("🔧 Unique Motors List")
        self.moteur_label.setStyleSheet(AppStyles.SECTION_HEADER_STYLE)
        scroll_layout.addWidget(self.moteur_label)
        
        self.moteur_container = QFrame()
        self.moteur_container.setMinimumHeight(200)
        self.moteur_layout = QVBoxLayout(self.moteur_container)
        scroll_layout.addWidget(self.moteur_container)
        
        # Set the scroll content
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        # Button section - Changed button text and functionality
        button_layout = QHBoxLayout()
        
        # Changed from "Run Analysis" to "Proceed to Results"
        self.analyze_button = QPushButton("📊 Proceed to Results")
        self.analyze_button.setMinimumHeight(40)
        self.analyze_button.setStyleSheet(AppStyles.ACTIVE_BUTTON_STYLE)
        self.analyze_button.clicked.connect(self.view_results)
        button_layout.addWidget(self.analyze_button)
        
        layout.addLayout(button_layout)
        
        # Check if analysis has already been completed
        if self.state.analysis_completed and self.state.results_df is not None:
            self.update_ui_with_results()
            self.analyze_button.setEnabled(True)
            self.analyze_button.setStyleSheet(AppStyles.COMPLETED_BUTTON_STYLE)
    
    def run_analysis(self):
        """Perform data analysis and update the UI."""
        try:
            # Clear previous results
            self.clear_ui_elements()
            
            # Check if we have the required data
            if self.state.old_df is None or self.state.new_df is None:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Missing Data", "Both old and new PTA files are required for analysis")
                return
            
            # Process the cursor
            QApplication.setOverrideCursor(Qt.WaitCursor)
            
            # Generate results
            result_df = generate_results_df(
                self.state.old_df,
                self.state.new_df,
                self.state.pta_type
            )
            
            # Store results in state
            self.state.results_df = result_df
            self.state.analysis_completed = True
            
            # Update UI with results
            self.update_ui_with_results()
            
            # Enable results button
            self.analyze_button.setEnabled(True)
            self.analyze_button.setStyleSheet(AppStyles.COMPLETED_BUTTON_STYLE)
            
            # Emit completion signal
            self.analysis_completed.emit()
            
            # Process the cursor
            QApplication.restoreOverrideCursor()
            
        except Exception as e:
            # Handle errors
            QApplication.restoreOverrideCursor()
            
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Analysis Error", f"Error during analysis: {str(e)}")
            
            error_label = QLabel(f"❌ Error during analysis: {str(e)}")
            error_label.setStyleSheet("color: #FF5733;")
            self.stats_layout.addWidget(error_label)
    
    def update_ui_with_results(self):
        """Update UI with analysis results."""
        result_df = self.state.results_df
        if result_df is None or result_df.empty:
            return

        # Overview metrics
        self.add_metrics(result_df)

        # Change type chart
        self.add_change_type_chart(result_df)
        
        # Add Moteur list display
        self.add_moteur_list()
    
    def add_metrics(self, result_df):
        """Add metrics cards to the grid layout."""
        # Clear existing items
        for i in reversed(range(self.metrics_layout.count())):
            item = self.metrics_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        # Calculate metrics
        total_cars = len(result_df)
        # Add total cars in old file
        total_old_cars = len(self.state.old_df) if self.state.old_df is not None else 0
        total_new = (result_df["Change Type"] == "New").sum()
        total_spring = (result_df["Change Type"] == "Spring Changed").sum()
        total_unchanged = (result_df["Change Type"] == "Unchanged").sum()

        # Add metrics to grid
        metrics = [
            MetricCard("🚙 Total Cars in Old File", total_old_cars),
            MetricCard("🚗 Total Cars in New File", total_cars),
            MetricCard("🟥 New Cars", total_new,
                      help_text="Cars that did not exist in the old PTA file"),
            MetricCard("🔁 Spring Changed Cars", total_spring,
                      f"{(total_spring / total_cars) * 100:.1f} %"),
            MetricCard("✅ Unchanged Cars", total_unchanged),
        ]

        # Add metrics to grid (first row: new, old, new cars; second row: spring changed, unchanged)
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]

        for i, (metric, pos) in enumerate(zip(metrics, positions)):
            self.metrics_layout.addWidget(metric, pos[0], pos[1])

    def add_change_type_chart(self, result_df):
        """Add bar chart of change type distribution."""
        for i in reversed(range(self.change_type_layout.count())):
            self.change_type_layout.itemAt(i).widget().setParent(None)
        
        canvas = MatplotlibCanvas(width=6, height=4)
        
        # Create bar chart
        if "Change Type" in result_df.columns:
            counts = result_df["Change Type"].value_counts()
            
            # Color mapping for consistency - Updated colors
            colors = {
                'New': '#FF5733',           # Red 
                'Spring Changed': '#CDA000', # Custom yellow
                'Unchanged': '#003366'       # Custom blue
            }
            chart_colors = [colors.get(status, '#9E9E9E') for status in counts.index]
            
            # Create the bar chart
            bars = canvas.axes.bar(counts.index, counts.values, color=chart_colors)
            
            # Add labels
            for bar in bars:
                height = bar.get_height()
                canvas.axes.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'{int(height)}',
                    ha='center', va='bottom',
                    fontweight='bold'
                )
            
            canvas.axes.set_title("Car Change Classification", fontsize=14, fontweight='bold')
            canvas.axes.set_xlabel("Change Type")
            canvas.axes.set_ylabel("Count")
            
            # Improve appearance
            canvas.axes.spines['top'].set_visible(False)
            canvas.axes.spines['right'].set_visible(False)
            canvas.axes.grid(axis='y', linestyle='--', alpha=0.7)
            
            self.change_type_layout.addWidget(canvas)
        else:
            label = QLabel("No data available for change type analysis.")
            self.change_type_layout.addWidget(label)

    def add_moteur_list(self):
        """Add a list display of unique motor types."""
        # Clear previous content
        for i in reversed(range(self.moteur_layout.count())):
            self.moteur_layout.itemAt(i).widget().setParent(None)
            
        moteurs = []
        
        # Check new file
        if self.state.new_df is not None and "Moteur" in self.state.new_df.columns:
            moteurs.extend(self.state.new_df["Moteur"].dropna().unique())
            
        # Check old file 
        if self.state.old_df is not None and "Moteur" in self.state.old_df.columns:
            moteurs.extend(self.state.old_df["Moteur"].dropna().unique())
            
        # Get sorted unique motors (remove duplicates)
        unique_moteurs = sorted(set(moteurs))
        
        if not unique_moteurs:
            label = QLabel("No motor data available in uploaded files")
            label.setStyleSheet("color: #CCCCCC; font-style: italic;")
            self.moteur_layout.addWidget(label)
            return
            
        # Display count
        count_label = QLabel(f"Found {len(unique_moteurs)} unique motor types")
        count_label.setStyleSheet("color: #CCCCCC; font-style: italic; margin-bottom: 10px;")
        self.moteur_layout.addWidget(count_label)
        
        # Create scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"background-color: {AppStyles.DARK_CARD_BG}; border: 1px solid {AppStyles.DARK_BORDER};")
        
        moteur_widget = QWidget()
        grid_layout = QGridLayout(moteur_widget)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(5)
        
        # Calculate number of columns based on typical length of motor names
        num_columns = 3  # Adjust based on typical width
        
        # Add motors to grid
        for i, moteur in enumerate(unique_moteurs):
            if moteur and str(moteur).strip():  # Skip empty values
                row = i // num_columns
                col = i % num_columns
                
                moteur_label = QLabel(f"• {moteur}")
                moteur_label.setStyleSheet("color: #CCCCCC; font-size: 13px; padding: 2px;")
                grid_layout.addWidget(moteur_label, row, col)
                
        scroll.setWidget(moteur_widget)
        self.moteur_layout.addWidget(scroll)

    def clear_ui_elements(self):
        """Clear all UI elements containing results."""
        # Clear metrics
        for i in reversed(range(self.metrics_layout.count())):
            item = self.metrics_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
                
        for i in reversed(range(self.change_type_layout.count())):
            item = self.change_type_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
        
        # Clear moteur list
        for i in reversed(range(self.moteur_layout.count())):
            item = self.moteur_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
    
    def view_results(self):
        """Navigate to the results page."""
        if self.parent() and hasattr(self.parent(), "navigate_to_step"):
            self.parent().navigate_to_step(2)  # Navigate to results step
