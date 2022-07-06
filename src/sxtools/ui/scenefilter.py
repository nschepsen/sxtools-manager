from PySide6.QtCore import QSortFilterProxyModel

class SceneFilter(QSortFilterProxyModel):
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

    def sync(self, dataset) -> None:
        '''
        '''
        self.sourceModel().sync(dataset)