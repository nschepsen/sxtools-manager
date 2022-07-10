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
    'PerformersRole PaysiteRole TitleRole DateRole SizeRole ResolutionRole PathRole MimeTypeRole',
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
        s = self.scenelist[index.row()]
        # switch on current role
        if role == SceneDataRole.PerformersRole:
            return s.perfs_as_string()
        elif role == SceneDataRole.PaysiteRole:
            return s.paysite
        elif role == SceneDataRole.TitleRole:
            return s.name() # or s.title
        elif role == SceneDataRole.DateRole:
            return f'{s.released or "not defined"}'
        elif role == SceneDataRole.SizeRole:
            return s.size # not humanreadable yet
        elif role == SceneDataRole.ResolutionRole:
            return s.resolution()
        elif role == SceneDataRole.PathRole:
            return s.path
        elif role == SceneDataRole.MimeTypeRole:
            return s.mimetype()
        elif role == Qt.DecorationRole:
            thumbnail = cache(s.basename())
            if thumbnail:
                return QImage(thumbnail)
            else:
                return QIcon.fromTheme(s.mimetype()).pixmap(47, 47)
        return None # return QVariant() -> Emergency Exit
