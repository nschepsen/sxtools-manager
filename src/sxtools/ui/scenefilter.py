from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, Qt
from sxtools.ui.scenemodel import SceneDataRole


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

    def invalidateFilter(self) -> None:
        '''
        '''
        super().invalidateFilter()
        # update the label "Found"
        self.parent().ui.filtredValue.setText(str(self.rowCount()))

    def filterAcceptsRow(self, row: int, parent: QModelIndex) -> bool:
        '''
        '''
        ft = self.parent().ui.aFilterModeT.isChecked()
        fu = self.parent().ui.aFilterModeU.isChecked()
        model = self.sourceModel()
        idx = model.index(row, 0, parent)
        tagged = model.data(idx, SceneDataRole.SceneRole).is_valid()
        if (ft and tagged) or (fu and not tagged):
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

    def remove(self, index: QModelIndex) -> None: self.sourceModel().remove(self.mapToSource(index))
