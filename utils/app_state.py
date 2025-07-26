import pandas as pd
from typing import Optional, Dict, Any

class AppState:
    """
    Manages application state for the Spring Change Detection app.
    Replaces Streamlit's session_state functionality.
    """
    
    def __init__(self):
        """Initialize application state with default values."""
        # Data state
        self.old_df: Optional[pd.DataFrame] = None
        self.new_df: Optional[pd.DataFrame] = None
        self.results_df: Optional[pd.DataFrame] = None
        self.old_file_path: Optional[str] = None
        self.new_file_path: Optional[str] = None
        
        # PTA type
        self.pta_type: str = "VP"  # Default to VP
        
        # Workflow state
        self.current_step: int = 0  # 0: upload, 1: analysis, 2: results
        self.analysis_completed: bool = False
        
        # Cache for Excel sheets data
        self.excel_sheets_data: Dict[str, Any] = {}
        self.excel_graphs_data: Dict[str, Any] = {}
    
    def reset_data(self):
        """Reset all data-related state."""
        self.old_df = None
        self.new_df = None
        self.results_df = None
        self.old_file_path = None
        self.new_file_path = None
        self.excel_sheets_data = {}
        self.excel_graphs_data = {}
        self.analysis_completed = False
        self.current_step = 0  # Reset to upload step
    
    def reset_workflow(self):
        """Reset workflow to the initial upload step."""
        self.current_step = 0
        self.analysis_completed = False
