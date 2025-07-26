import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from gui.main_window import MainWindow
from utils.app_state import AppState
from gui.styling import AppStyles

def setup_resource_paths():
    """Setup resource paths for PyInstaller compatibility"""
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        os.environ['RESOURCE_PATH'] = sys._MEIPASS
    else:
        # Running in development
        os.environ['RESOURCE_PATH'] = os.path.dirname(os.path.abspath(__file__))
        
def main():
    """
    Main entry point for the Spring Change Detection Application.
    """
    setup_resource_paths()
    # 1) Bootstrap QApplication
    app = QApplication(sys.argv)

    # 2) Determine where resources live
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running in your IDE / as a normal script
        base_path = os.path.dirname(os.path.abspath(__file__))

    # 3) Build the full path to your .ico
    icon_path = os.path.join(base_path, "resources", "icons", "app_icon.ico")
    app_icon = QIcon(icon_path)
    if app_icon.isNull():
        print(f"⚠️  Warning: Failed to load icon at {icon_path}")
    else:
        # 4) Apply it globally (taskbar, dialogs, etc.)
        app.setWindowIcon(app_icon)

    # 5) Style
    app.setStyle("Fusion")
    app.setStyleSheet(AppStyles.DARK_MODE_STYLE)

    # 6) Your application state
    state = AppState()

    # 7) Instantiate and show main window
    window = MainWindow(state)
    if not app_icon.isNull():
        window.setWindowIcon(app_icon)
    window.show()

    # 8) Enter the Qt main loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
