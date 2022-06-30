from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

from sxtools.core.videoscene import Scene
from sxtools.utils import human_readable


class SceneTableModel(QAbstractTableModel):

    def __init__(self, scenes: list[Scene]=[], parent=None) -> None:

        super(SceneTableModel, self).__init__(parent)
        self.scenes = scenes
        self.headerTitles = ['Released', 'Performers', 'Published by', 'Size', 'Title']

    def rowCount(self, parent=QModelIndex()) -> int:
        '''
        '''
        return len(self.scenes)

    def columnCount(self, parent=QModelIndex()) -> int:
        '''
        '''
        return len(self.headerTitles)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):

        if role == Qt.TextAlignmentRole:
            return Qt.AlignHCenter + Qt.AlignVCenter
        elif role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                return f'{section + 1}'
            elif orientation == Qt.Horizontal:
                return self.headerTitles[section]
        return None # return QVariant()

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return None
        row, column = index.row(), index.column()
        if role == Qt.DisplayRole:
            if column == 0: # released date
                return self.scenes[row].released
            elif column == 1: # performers
                return self.scenes[row].perfs_as_string()
                # return '\n'.join(
                #     self.scenes[row].performers)
            elif column == 2: # published by
                return self.scenes[row].paysite
            elif column == 3: # size in MiB & GiB
                return human_readable(self.scenes[row].size)
            elif column == 4: # scene title
                return self.scenes[row].title
        elif role == Qt.TextAlignmentRole:
            if index.column() != 4:
                return Qt.AlignHCenter + Qt.AlignVCenter
        return None # return QVariant() -> Emergency Exit
