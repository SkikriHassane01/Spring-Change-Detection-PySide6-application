from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from gui.styling import AppStyles

class MetricCard(QFrame):
    """
    A card-like widget to display a metric with a title, value and optional delta indicator.
    Similar to Streamlit's st.metric component.
    """
    
    def __init__(self, title, value, delta=None, help_text=None):
        super().__init__()
        
        self.title = title
        self.value = value
        self.delta = delta
        self.help_text = help_text
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components."""
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(AppStyles.METRIC_CARD_STYLE)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumHeight(100)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet(AppStyles.METRIC_TITLE_STYLE)
        layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(str(self.value))
        value_label.setFont(QFont("Arial", 18, QFont.Bold))
        value_label.setStyleSheet(AppStyles.METRIC_VALUE_STYLE)
        layout.addWidget(value_label)
        
        # Delta (if provided)
        if self.delta:
            delta_text = f"△ {self.delta}"
            delta_label = QLabel(delta_text)
            
            # Style based on positive/negative
            if isinstance(self.delta, str) and '-' in self.delta:
                delta_label.setStyleSheet(AppStyles.METRIC_DELTA_NEGATIVE_STYLE)
            else:
                delta_label.setStyleSheet(AppStyles.METRIC_DELTA_STYLE)
                
            layout.addWidget(delta_label)
        
        # Help text (if provided)
        if self.help_text:
            help_label = QLabel(self.help_text)
            help_label.setWordWrap(True)
            help_label.setStyleSheet("color: #666; font-size: 10px;")
            help_label.setAlignment(Qt.AlignLeft)
            layout.addWidget(help_label)
        
        layout.addStretch()
