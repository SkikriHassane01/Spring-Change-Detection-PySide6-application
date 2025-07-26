from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QFont
import pandas as pd
import numpy as np

class DataFrameModel(QAbstractTableModel):
    """Model for displaying pandas DataFrames in QTableView, complete with headers."""

    def __init__(self, data: pd.DataFrame = None, parent=None):
        super().__init__(parent)
        # Copy so we don't mutate the original
        if data is not None:
            # Reset index to make it a column and include column names as first row
            df = data.copy()
            # Convert index to column
            df.reset_index(inplace=True)
            # Prepare header row
            header_row = pd.DataFrame([df.columns], columns=df.columns)
            # Concatenate header row with data
            self.dataframe = pd.concat([header_row, df], ignore_index=True)
        else:
            self.dataframe = pd.DataFrame()

    def rowCount(self, parent=QModelIndex()):
        return self.dataframe.shape[0]

    def columnCount(self, parent=QModelIndex()):
        return self.dataframe.shape[1]

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        value = self.dataframe.iloc[index.row(), index.column()]

        if role == Qt.DisplayRole:
            # Blank for NaN
            if pd.isna(value):
                return ""
            # Floats: drop trailing .0, else two decimals
            if isinstance(value, (float, np.floating)):
                return str(int(value)) if value == int(value) else f"{value:.2f}"
            # Ints
            if isinstance(value, (int, np.integer)):
                return str(int(value))
            # Everything else
            return str(value)

        if role == Qt.TextAlignmentRole:
            # Numbers right‑aligned, text left‑aligned
            if isinstance(value, (int, float, np.number)):
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        if role == Qt.FontRole:
            # Bold any cell in a “Reference” column
            col_name = self.dataframe.columns[index.column()]
            if col_name.lower().endswith("reference") or "reference" in col_name.lower():
                font = QFont()
                font.setBold(True)
                return font

        return None

    def headerData(self,
                   section: int,
                   orientation: Qt.Orientation,
                   role=Qt.DisplayRole):
        """Provide both horizontal (column names) and vertical (row numbers) headers."""
        # Only care about display, font, and alignment here
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                # Column header text
                try:
                    return str(self.dataframe.columns[section])
                except IndexError:
                    return ""
            else:
                # 1‑based row numbers
                return str(section + 1)

        if role == Qt.FontRole:
            # Make all headers bold
            font = QFont()
            font.setBold(True)
            return font

        if role == Qt.TextAlignmentRole:
            # Center column headers, right‑align row numbers
            if orientation == Qt.Horizontal:
                return Qt.AlignCenter
            return Qt.AlignRight | Qt.AlignVCenter

        return None

    def flags(self, index: QModelIndex):
        # Default: items are selectable, enabled (but not editable)
        return super().flags(index)

    def update_dataframe(self, dataframe: pd.DataFrame):
        """Replace the underlying DataFrame (and refresh view)."""
        self.beginResetModel()
        if dataframe is not None:
            # Reset index to make it a column and include column names as first row
            df = dataframe.copy()
            # Convert index to column
            df.reset_index(inplace=True)
            # Prepare header row
            header_row = pd.DataFrame([df.columns], columns=df.columns)
            # Concatenate header row with data
            self.dataframe = pd.concat([header_row, df], ignore_index=True)
        else:
            self.dataframe = pd.DataFrame()
        self.endResetModel()
