from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, Qt

from sxtools.ui.scenelistmodel import SceneDataRole


class SceneSortFilter(QSortFilterProxyModel):

    def __init__(self, parent = None) -> None:
        '''
        '''
        super().__init__(parent)

        self.setSortCaseSensitivity(
            Qt.CaseInsensitive)
        self.setFilterRole(
            SceneDataRole.PerformersRole)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def lessThan(self, l: QModelIndex, r: QModelIndex) -> bool:
        '''
        '''
        a, b = l.data(self.sortRole()), r.data(self.sortRole())
        if self.sortCaseSensitivity() == Qt.CaseInsensitive:
            if type(a) == str:
                a = a.lower()
                b = b.lower()
        return a < b # compare two objects together, strings almost
