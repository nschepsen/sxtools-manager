from datetime import date
from enum import IntEnum  # auto, Enum

from PySide6.QtCore import QAbstractListModel, QDate, QModelIndex, Qt
from PySide6.QtGui import QIcon, QImage
from sxtools.core.videoscene import Scene
from sxtools.logging import get_basic_logger
logger = get_basic_logger()  # sXtools.log
from sxtools.utils import bview, cache, fview

DefaultQDate = QDate(1752, 9, 14).toPython() # FIXME: QDate handling

SceneDataRole = IntEnum(
    'SceneDataRole',
    'PerformersRole PaysiteRole TitleRole DateRole SizeRole PathRole SceneRole',
    start = Qt.UserRole)

class SceneModel(QAbstractListModel):
    '''
    class for maintaining sceneslist, used by QSortFilterProxyModel
    '''
    def __init__(self, parent = None) -> None:
        '''
        initialize class itself, scenelist and hashvalues
        '''
        super(SceneModel, self).__init__(parent)
        self.scenelist = list()
        self.hashvalues = {} # aware of duplicates

    def sync(self, sl: list[Scene]) -> None:
        '''
        sync sceneview w the app queue
        '''
        self.beginResetModel()
        self.scenelist = sl
        for s in sl:
            k = s.viewname()
            self.hashvalues[k] = self.hashvalues.get(k, 0) + 1
        self.endResetModel() # model sync'd

    def clear(self) -> None:
        '''
        reset sceneview (QAbstractListModel) model
        '''
        self.beginResetModel()
        self.scenelist.clear()
        self.hashvalues.clear()
        self.endResetModel() # model clear'd

    def remove(self, index = QModelIndex()) -> None:
        '''
        delete scene with given index from the list
        '''
        if not index.isValid():
            logger.warning('The index is not valid')
            return
        row = index.row()
        self.beginRemoveRows(QModelIndex(), row, row)
        s = self.scenelist.pop(row)
        self.endRemoveRows()
        key = s.viewname()
        logger.info(f'Removed {key} successfully')
        self.hashvalues[key] = self.hashvalues.get(key, 1) - 1

    def rowCount(self, parent = QModelIndex()) -> int:
        '''
        return number of scenes in the list
        '''
        return len(self.scenelist)

    def data(self, index, role: int = Qt.DisplayRole):
        '''
        retrieve data according to its role
        '''
        s = self.scenelist[index.row()] # get the item
        if role == SceneDataRole.PerformersRole:
            return s.perfs_as_string()
        elif role == SceneDataRole.PaysiteRole:
            return s.paysite
        elif role == SceneDataRole.TitleRole:
            # FIXME: s.title is always set
            return s.title # or (s.basename() if not s.is_valid() else '')
        elif role == SceneDataRole.DateRole:
            return s.released or DefaultQDate
        elif role == SceneDataRole.SizeRole:
            return s.size # not humanreadable yet
        elif role == SceneDataRole.SceneRole:
            return s # return the reference to the scene
        elif role == SceneDataRole.PathRole:
            return s.path # absolute path of a given scene
        elif role == Qt.DecorationRole:
            thumbnail = cache(s.basename())
            if thumbnail:
                return QImage(thumbnail)
            else:
                return QIcon.fromTheme(s.mimetype()).pixmap(64, 64)
        return None # return QVariant() -> Emergency Exit

    def setData(self, index: QModelIndex, value, role: int) -> bool:
        '''
        assign data according to its role
        '''
        if type(value) == str: # remove leading and trailing spaces
            value = value.strip()
        # if not value and role != SceneDataRole.TitleRole:
        #     return False
        s = self.scenelist[index.row()] # get the current item
        if role == SceneDataRole.PerformersRole:
            assert type(value) == list
            value = list(fview(x) for x in value)
            if set(value) == set(s.performers):
                return False
            mgr = self.parent().manager # get manager
            # decrease deleting performers' rank
            for p in set(s.performers) - set(value):
                p = bview(p)
                mgr.performers[p] = mgr.performers.get(p, 1) - 1
                if not mgr.performers[p]:
                    logger.warning(f'A suspicious entry "{p}" detected')
            # increase newly added performers' rank
            for p in set(value) - set(s.performers):
                p = bview(p)
                mgr.performers[p] = mgr.performers.get(p, 0) + 1
            s.performers = value # update to the current state
            return True
        elif role == SceneDataRole.DateRole:
            if value == DefaultQDate:
                value = None # convert default qt date back to "None"
            if value != s.released:
                assert type(value) == None or date
                s.released = value
                return True
        elif role == SceneDataRole.TitleRole:
            if value != s.title:
                s.title = value
                return True # scene's title could be empty
        elif role == SceneDataRole.PaysiteRole:
            if value != s.paysite:
                s.paysite = value # set modified paysite as string
                return True
        else:
            logger.warning(f'An unhandled role "{role}" was caught')
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags: return super().flags(index) | Qt.ItemIsEditable
