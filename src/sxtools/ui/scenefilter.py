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

    def filterAcceptsRow(self, row: int, parent: QModelIndex) -> bool:
        '''
        '''
        ft, fu = self.parent().ui.actionFilterTagged.isChecked(), self.parent().ui.actionFilterUntagged.isChecked()
        index = self.sourceModel().index(row, 0, parent)
        state = self.sourceModel().data(index, SceneDataRole.PerformersRole)
        if (ft and state) or (fu and not state):
            return False
        else:
            return super().filterAcceptsRow(row, parent)

    def lessThan(self, l: QModelIndex, r: QModelIndex) -> bool:
        '''
        '''
        a, b = l.data(self.sortRole()), r.data(self.sortRole())
        if self.sortCaseSensitivity() == Qt.CaseInsensitive:
            if type(a) == str:
                a = a.lower()
                b = b.lower()
        return a < b # compare two objects together, strings almost
