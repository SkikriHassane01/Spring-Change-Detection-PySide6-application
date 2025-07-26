class AppStyles:
    """
    Contains styles for the application to maintain consistent look and feel.
    Dark mode theme with blue/sky blue accent colors for better contrast and readability.
    """
    
    # Main colors
    PRIMARY_COLOR = "#4CB9E7"  # Sky blue
    SECONDARY_COLOR = "#3AA1D9"  # Slightly darker sky blue
    ERROR_COLOR = "#FF5733"  # Red
    WARNING_COLOR = "#CDA000"  # Custom yellow
    HIGHLIGHT_COLOR = "#4CB9E7"  # Sky blue
    
    # Dark mode colors
    DARK_BG = "#121212"  # Main dark background
    DARK_CARD_BG = "#1E1E1E"  # Slightly lighter for cards and sections
    DARK_HIGHLIGHT = "#2D2D2D"  # Highlight areas
    DARK_BORDER = "#333333"  # Borders
    
    # Text colors
    TEXT_COLOR = "#FFFFFF"  # White for normal text
    MUTED_TEXT_COLOR = "#E0E0E0"  # Slightly muted white
    
    # Background colors
    BACKGROUND_COLOR = DARK_BG
    SIDEBAR_COLOR = DARK_CARD_BG
    
    # Element styles
    SIDEBAR_STYLE = f"""
        background-color: {DARK_CARD_BG};
        border-right: 1px solid {DARK_BORDER};
        padding: 10px;
        color: {TEXT_COLOR};
    """
    
    SIDEBAR_TITLE_STYLE = f"""
        QLabel {{
            color: {PRIMARY_COLOR}; 
            font-weight: bold;
            font-size: 14px;
            padding: 5px 0;
            border-bottom: 1px solid {DARK_BORDER};
        }}
    """
    
    SIDEBAR_TEXT_STYLE = f"""
        QLabel {{
            color: {TEXT_COLOR};
            font-size: 13px;  /* Increased from 12px */
            font-weight: bold; /* Added bold */
        }}
    """
    
    ACTIVE_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px;
            text-align: left;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #3AA1D9;  /* Darker sky blue on hover */
        }}
        QPushButton:disabled {{
            background-color: #2B89BD;  /* Muted sky blue when disabled */
            color: #AAAAAA;
        }}
    """
    
    COMPLETED_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: #4CB9E7;  /* Sky blue for completed state */
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px;
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: #002244;  /* Darker blue on hover */
        }}
    """
    
    INACTIVE_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {DARK_HIGHLIGHT};
            color: {TEXT_COLOR};
            border: none;
            border-radius: 4px;
            padding: 8px;
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: #3D3D3D;
        }}
        QPushButton:disabled {{
            background-color: #252525;
            color: #666666;
        }}
    """
    
    HEADER_STYLE = f"""
        color: {TEXT_COLOR};
        font-weight: bold;
        background-color: {DARK_CARD_BG};
        padding: 8px;
        border-radius: 4px;
    """
    
    SECTION_HEADER_STYLE = f"""
        QLabel {{
            color: {PRIMARY_COLOR};
            font-size: 16px;
            font-weight: bold;
            padding: 8px 0;
        }}
    """
    
    LABEL_STYLE = f"""
        QLabel {{
            color: {TEXT_COLOR};
        }}
    """
    
    # For data highlighting in tables
    HIGHLIGHT_NEW_STYLE = "background-color: #FF5733; color: white;"
    HIGHLIGHT_CHANGED_STYLE = "background-color: #CDA000; color: white;"
    
    # Card styles
    METRIC_CARD_STYLE = f"""
        QFrame {{
            background-color: {DARK_CARD_BG};
            border: 1px solid {DARK_BORDER};
            border-radius: 4px;
            padding: 8px;
        }}
    """
    
    METRIC_TITLE_STYLE = f"""
        QLabel {{
            font-size: 12px;
            color: {MUTED_TEXT_COLOR};
        }}
    """
    
    METRIC_VALUE_STYLE = f"""
        QLabel {{
            font-size: 24px;
            font-weight: bold;
            color: {TEXT_COLOR};
        }}
    """
    
    METRIC_DELTA_STYLE = f"""
        QLabel {{
            font-size: 12px;
            color: {PRIMARY_COLOR};
        }}
    """
    
    METRIC_DELTA_NEGATIVE_STYLE = f"""
        QLabel {{
            font-size: 12px;
            color: {ERROR_COLOR};
        }}
    """
    
    # Table styles
    TABLE_STYLE = f"""
        QTableView {{
            background-color: {DARK_BG};
            color: {TEXT_COLOR};
            gridline-color: {DARK_BORDER};
            border: none;
        }}
        QHeaderView::section {{
            background-color: {DARK_BG};
            color: {TEXT_COLOR};
            padding: 8px;
            font-weight: bold;
            border: 1px solid {DARK_BORDER};
        }}
        QHeaderView::section:vertical {{
            background-color: {DARK_BG};
            color: {TEXT_COLOR};
            padding: 4px;
            font-weight: bold;
            border: 1px solid {DARK_BORDER};
        }}
        QTableView::item {{
            padding: 4px;
            font-weight: bold;
        }}
        QTableView QTableCornerButton::section {{
            background-color: {DARK_BG};
            border: 1px solid {DARK_BORDER};
        }}
    """
    
    # Statistical analysis table styles
    STATS_TABLE_STYLE = f"""
        QTableView {{
            background-color: {DARK_BG};
            gridline-color: {DARK_BORDER};
            color: {TEXT_COLOR};
            selection-background-color: #003366;
            selection-color: white;
            border: 1px solid {DARK_BORDER};
            alternate-background-color: {DARK_HIGHLIGHT};
        }}
        QHeaderView::section {{
            background-color: {SECONDARY_COLOR};
            color: white;
            padding: 12px;
            border: 1px solid #002244;
            font-weight: bold;
            font-size: 13px;
        }}
    """
    
    # Frame styles
    STATS_FRAME_STYLE = f"""
        QFrame {{
            background-color: {DARK_CARD_BG};
            border: 1px solid {DARK_BORDER};
            border-radius: 4px;
        }}
    """
    
    # App-wide dark mode style
    DARK_MODE_STYLE = f"""
        QWidget {{
            background-color: {DARK_BG};
            color: {TEXT_COLOR};
        }}
        QScrollArea {{
            background-color: {DARK_BG};
            border: none;
        }}
        QLabel {{
            color: {TEXT_COLOR};
        }}
        QPushButton {{
            background-color: {DARK_HIGHLIGHT};
            color: {TEXT_COLOR};
            border: none;
            border-radius: 4px;
            padding: 6px;
        }}
        QPushButton:hover {{
            background-color: #3D3D3D;
        }}
        QTabWidget::pane {{
            border: 1px solid {DARK_BORDER};
            background-color: {DARK_CARD_BG};
        }}
        QTabBar::tab {{
            background-color: {DARK_HIGHLIGHT};
            color: {TEXT_COLOR};
            border: 1px solid {DARK_BORDER};
            padding: 6px 12px;
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background-color: {PRIMARY_COLOR};
            color: white;
        }}
        QTabBar::tab:hover:!selected {{
            background-color: #3D3D3D;
        }}
        QHeaderView {{
            background-color: {DARK_CARD_BG};
            color: {TEXT_COLOR};
        }}
        QScrollBar:vertical {{
            background-color: {DARK_BG};
            width: 14px;
            margin: 15px 3px 15px 3px;
            border: 1px solid {DARK_BORDER};
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {DARK_HIGHLIGHT};
            min-height: 30px;
            border-radius: 3px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: #3D3D3D;
        }}
        QScrollBar:horizontal {{
            background-color: {DARK_BG};
            height: 14px;
            margin: 3px 15px 3px 15px;
            border: 1px solid {DARK_BORDER};
            border-radius: 4px;
        }}
        QScrollBar::handle:horizontal {{
            background-color: {DARK_HIGHLIGHT};
            min-width: 30px;
            border-radius: 3px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background-color: #3D3D3D;
        }}
    """
