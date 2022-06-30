from enum import IntEnum
from typing import Any

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtGui import QIcon, QImage
from sxtools.core.videoscene import Scene
from sxtools.utils import cache


class SceneModel(QAbstractListModel):

    class UserRoles(IntEnum):
        '''
        User defined Roles, Customizable
        '''
        Performers = Qt.UserRole
        Paysite = Qt.UserRole + 1
        Title = Qt.UserRole + 2
        Date = Qt.UserRole + 3
        Size = Qt.UserRole + 4
        Resolution = Qt.UserRole + 5
        Scene = Qt.UserRole + 8
        MimeType = Qt.UserRole + 9

    def __init__(self, s: Scene = None, parent = None) -> None:

        super(SceneModel, self).__init__(parent)
        self.scenelist = s or list() # init scenelist

    def clear(self) -> None:
        '''
        '''
        self.beginResetModel()
        self.scenelist.clear()
        self.endResetModel() # model cleared

    def rowCount(self, parent = QModelIndex()) -> int:
        '''
        :return: number of scenes
        '''
        return len(self.scenelist)

    def sync(self, sl: list[Scene]) -> None:
        '''
        sync the "scenelist" with the current data
        '''
        self.beginResetModel()
        self.scenelist = sl # aware of duplicates
        self.endResetModel()

    def data(self, index, role: int = Qt.DisplayRole):
        '''
        retrieve data according to its role
        '''
        s = self.scenelist[index.row()] # get item
        if role == SceneModel.UserRoles.Performers:
            return s.perfs_as_string() # or 'empty'
        elif role == SceneModel.UserRoles.Paysite:
            return s.paysite # or 'no information available'
        elif role == SceneModel.UserRoles.Title:
            return s.name() # or s.title
        elif role == SceneModel.UserRoles.Date:
            return f'{s.released or "not defined"}'
        elif role == SceneModel.UserRoles.MimeType:
            return s.mimetype()
        elif role == SceneModel.UserRoles.Size:
            return s.size # not humanreadable yet
        elif role == SceneModel.UserRoles.Resolution:
            return s.resolution()
        elif role == Qt.DecorationRole:
            thumbnail = cache(s.basename())
            if thumbnail:
                return QImage(thumbnail)
            else:
                return QIcon.fromTheme(s.mimetype()).pixmap(56, 56)
        return None # return QVariant() -> Emergency Exit

    def setData(self, index, value: Any, role: int) -> bool:
        '''
        '''
        return super().setData(index, value, role)

