from datetime import date
from enum import IntEnum, Enum  # , auto

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtGui import QIcon, QImage
from sxtools.core.videoscene import Scene
from sxtools.utils import cache  # check thumbnails existence

# class SceneRole(Enum):
#     '''
#     Extend Qt.ItemDataRole with User defined Roles
#     '''
#     Performers = Qt.UserRole
#     Paysite    = auto()
#     Title      = auto()
#     Date       = auto()
#     Size       = auto()
#     Resolution = auto()
#     Path       = auto()
#     Scene      = auto()
#     MimeType   = auto()

SceneDataRole = IntEnum(
    'SceneDataRole',
    'PerformersRole PaysiteRole TitleRole DateRole SizeRole SceneRole',
    start=Qt.UserRole)

class SceneModel(QAbstractListModel):

    def __init__(self, s: Scene = None, parent = None) -> None:
        '''
        '''
        super(SceneModel, self).__init__(parent)
        self.scenelist = s or list() # init data

    def sync(self, sl: list) -> None:
        '''
        sync "scenelist" with the app queue
        '''
        self.beginResetModel()
        self.scenelist = sl # aware of duplicates
        self.endResetModel()

    def clear(self) -> None:
        '''
        reset "scenelist" UI view & model
        '''
        self.beginResetModel()
        self.scenelist.clear()
        self.endResetModel() # model cleared

    def rowCount(self, parent = QModelIndex()) -> int:
        '''
        :return: number of scenes
        '''
        return len(self.scenelist)

    def data(self, index, role: int = Qt.DisplayRole):
        '''
        retrieve data according to its role
        '''
        s = self.scenelist[index.row()] # get the current item
        if role == SceneDataRole.PerformersRole:
            return s.perfs_as_string()
        elif role == SceneDataRole.PaysiteRole:
            return s.paysite
        elif role == SceneDataRole.TitleRole:
            return s.title # or s.name()
        elif role == SceneDataRole.DateRole:
            return f'{s.released or "not defined"}'
        elif role == SceneDataRole.SizeRole:
            return s.size # not humanreadable yet
        elif role == SceneDataRole.SceneRole:
            return s # return the reference to the object
        elif role == Qt.DecorationRole:
            thumbnail = cache(s.basename())
            if thumbnail:
                return QImage(thumbnail)
            else:
                return QIcon.fromTheme(s.mimetype()).pixmap(64, 64)
        return None # return QVariant() -> Emergency Exit

    def setData(self, index: QModelIndex, value, role: int) -> bool:
        '''
        '''
        s = self.scenelist[index.row()] # get the current item
        if role == SceneDataRole.PerformersRole:
            if value and type(value) == list and set(value) != set(s.performers):
                s.performers = value
                return True
        elif role == SceneDataRole.DateRole:
            if value and type(value) == date and value != s.released:
                s.released = value
                return True
        elif role == SceneDataRole.TitleRole:
            if value != s.title:
                s.title = value
                return True
        elif role == SceneDataRole.PaysiteRole:
            if value and value != s.paysite:
                s.paysite = value # set modified paysite as string
                return True
        else:
            print(f'Warning: An unhandled role "{role}" was caught')
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags: return super().flags(index) | Qt.ItemIsEditable
