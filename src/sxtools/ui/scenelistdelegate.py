from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPoint, QRect, QSize, Qt
from PySide6.QtGui import QBrush, QFont, QFontMetrics, QImage, QPainter, QPalette, QPixmap
from PySide6.QtWidgets import QApplication, QStyle, QStyledItemDelegate, QStyleOptionViewItem, QWidget
from sxtools.ui.sceneeditor import SceneEditor
from sxtools.ui.scenelistmodel import SceneDataRole
from sxtools.utils import fview, human_readable


class SceneDelegate(QStyledItemDelegate):

    def __init__(self, parent=None) -> None:
        '''
        '''
        super(SceneDelegate, self).__init__(parent) # init parent methods

        self.pFont = QFont(
            QApplication.font().family(), 12, QFont.Bold)
        self.sFont = QFont(
            QApplication.font().family(), 13, QFont.Bold)
        self.iconSize = 49 # height of the info text block

    @staticmethod
    def circledIcon(icon: QImage, size: int = 48) -> QImage:
        '''
        '''
        side = min(icon.width(), icon.height())
        squaded = icon.copy(
            icon.width() - side >> 1, icon.height() - side >> 1, side, side)
        circled = QImage(side, side, QImage.Format_ARGB32)
        circled.fill(Qt.transparent)
        painter = QPainter(circled)
        painter.setBrush(QBrush(squaded))
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        # painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.drawEllipse(0, 0, side, side)
        painter.end()
        return circled.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def createEditor(self, parent, option, index) -> QWidget:
        '''
        '''
        manager = self.parent().parent().parent().manager
        perfs = list(
            fview(x) for x in manager.performers.keys())
        publishers = set(manager.publishers.values())
        return SceneEditor(perfs, publishers) # ret QWidget<Editor>

    def updateEditorGeometry(self, editor, option, index):
        '''
        '''
        spawnRect = QStyle.alignedRect(
            Qt.LeftToRight,
            Qt.AlignCenter,
            editor.size(),
            QApplication.primaryScreen().availableGeometry())
        editor.setGeometry(spawnRect)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        '''
        '''
        s = index.data(SceneDataRole.SceneRole) # get scene
        if s.is_valid():
            editor.ui.iReleaseDate.setDate(s.released)
            editor.ui.iPaysite.setText(s.paysite) # always set
            editor.ui.iTitle.setText(s.title) # could be empty
            editor.ui.performerList.addItems(s.performers)
        editor.ui.lblBaseName.setText(s.basename()) # basename

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        '''
        TODO: this method needs a FIX asap! Problem: setData -> Doublechecking
        '''
        s = index.data(SceneDataRole.SceneRole) # get scene
        date = editor.ui.iReleaseDate.date().toPython()
        if s.released != date:
            model.setData(index, date, SceneDataRole.DateRole)
        paysite = editor.ui.iPaysite.text().strip()
        if paysite and s.paysite != paysite:
            model.setData(
                index, paysite, SceneDataRole.PaysiteRole)
        title = editor.ui.iTitle.text().strip()
        if s.title != title:
            model.setData(index, title, SceneDataRole.TitleRole)
        pl = editor.ui.performerList
        perfs = [x.text() for x in pl.findItems('*', Qt.MatchWildcard)]
        if perfs and set(perfs) != set(s.performers):
            model.setData(index, [x.strip().title() for x in perfs], SceneDataRole.PerformersRole)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index) -> None:
        '''
        '''
        cr = QPalette.Text # set default Qt.ColorRole
        painter.setRenderHint(
            QPainter.TextAntialiasing, True)
        painter.setRenderHint(
            QPainter.Antialiasing, True)
        painter.setRenderHint(
            QPainter.SmoothPixmapTransform, True)
        if option.state & QStyle.State_Selected:
            cr = QPalette.HighlightedText
            painter.fillRect(
                option.rect,
                option.palette.brush(QPalette.Normal, QPalette.Highlight))
        defaultFont = painter.font() # for fall-back

        painter.setPen(option.palette.color(QPalette.Normal, cr))

        paysite = index.data(SceneDataRole.PaysiteRole)
        s = index.data(SceneDataRole.SceneRole)
        released = index.data(SceneDataRole.DateRole)
        resolution = f'Resolution: {s.resolution()}'
        size = human_readable(s.size) # size as string
        title = index.data(SceneDataRole.TitleRole)
        performers = index.data(SceneDataRole.PerformersRole) # perfs as string

        wPerfs, hPerfs = QFontMetrics(self.pFont).size(0, performers).toTuple()
        wSite, _ = painter.fontMetrics().size(0, paysite).toTuple()
        wTitle, hDefault = painter.fontMetrics().size(0, title).toTuple()
        wName, _ = painter.fontMetrics().size(0, s.basename()).toTuple()
        wDate, _ = painter.fontMetrics().size(0, released).toTuple()
        wSize, hSize = QFontMetrics(self.sFont).size(0, size).toTuple()
        wResolution, _ = painter.fontMetrics().size(0, resolution).toTuple()

        x, y, w, h = option.rect.adjusted(5, 5, -5, -5).getRect() # layout coords
        w2, w3 = max(wPerfs, wSite, wTitle or wName), max(wDate, wSize, wResolution)
        height = hDefault+s.is_valid()*(hPerfs+1+bool(s.title)*(hDefault+1))
        offset = (h - min(h, self.iconSize)) >> 1
        origin = QPoint(
            x + h + 10,
            y + ((h - height) >> 1)) # origin
        # column 1: Thumbnail
        painter.drawImage(
           QRect(x + offset, y + offset, self.iconSize, self.iconSize),
           SceneDelegate.circledIcon(index.data(Qt.DecorationRole), self.iconSize))
        # column 2: Description
        if s.is_valid():
            perfsRect = QRect(origin, QSize(w2, hPerfs))
            painter.setFont(self.pFont)
            painter.drawText(
                perfsRect, Qt.AlignLeft|Qt.AlignVCenter, performers)
            painter.setFont(defaultFont)
            paysiteRect = perfsRect.adjusted(
                0, hPerfs + 1, 0, hDefault + 1)
            painter.drawText(paysiteRect, Qt.AlignLeft, paysite)
            if s.title:
                titleRect = paysiteRect.adjusted(0, hDefault + 1, 0, hDefault + 1)
                painter.drawText(titleRect, Qt.AlignLeft|Qt.AlignVCenter, title) # title
        else:
            painter.drawText(
                QRect(origin, QSize(w2, hDefault)), Qt.AlignLeft, s.basename())
        # column 3: Information
        releasedRect = QRect(
            w - w3, y + ((h - (hSize + 2*(hDefault + 1)))>>1), w3, hDefault)
        painter.drawText(releasedRect, Qt.AlignHCenter, released)
        sizeRect = releasedRect.adjusted(
            0, hDefault + 1, 0, hSize + 1)
        painter.setFont(self.sFont)
        painter.drawText(sizeRect, Qt.AlignHCenter, size)
        painter.setFont(defaultFont)
        resolutionRect = sizeRect.adjusted(0, hSize + 1, 0, hDefault + 1)
        painter.drawText(resolutionRect, Qt.AlignHCenter | Qt.AlignVCenter, resolution)

    def sizeHint(self, option: QStyleOptionViewItem, index) -> QSize:
        '''
        '''
        h = 10 + max(self.iconSize, QFontMetrics(self.sFont).height() + 2 * (QFontMetrics(option.font).height() + 1))
        # return super().sizeHint(option, index)
        return QSize(h, h) # TODO: implement a better way to estimate the size
