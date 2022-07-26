from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPoint, QRect, QSize, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QFontMetrics, QImage, QPainter, QPalette
from PySide6.QtWidgets import QApplication, QStyle, QStyledItemDelegate, QStyleOptionViewItem, QWidget
from sxtools.ui.sceneeditor import SceneEditor
from sxtools.ui.scenelistmodel import SceneDataRole
from sxtools.utils import human_readable  # fmt size to a human readable string


class SceneDelegate(QStyledItemDelegate):

    def __init__(self, parent = None) -> None:
        '''
        '''
        super(SceneDelegate, self).__init__(parent) # init parent methods

        self.pFont = QFont(
            QApplication.font().family(), 12, QFont.Bold)
        self.sFont = QFont(
            QApplication.font().family(), 13, QFont.Bold)
        self.iconSize = 49 # height of the info text block

    @staticmethod
    def circledIcon(image: QImage, dimention: int = 49) -> QImage:
        '''
        create a circled thumbnail as an item decoration
        '''
        side = min(image.width(), image.height())
        squaded = image.copy(
            image.width() - side >> 1, image.height() - side >> 1, side, side)
        circled = QImage(side, side, QImage.Format_ARGB32)
        circled.fill(Qt.transparent)
        painter = QPainter(circled)
        painter.setBrush(QBrush(squaded))
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        # painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.drawEllipse(0, 0, side, side)
        painter.end()
        return circled.scaled(dimention, dimention, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def createEditor(self, parent, option, index) -> QWidget:
        '''
        '''
        return SceneEditor(self.parent().parent().parent().manager) # ret QWidget<Editor>

    def updateEditorGeometry(self, editor, option, index):
        '''
        adjust the position of a window on the screen
        '''
        spawnRect = QStyle.alignedRect(
            Qt.LeftToRight,
            Qt.AlignCenter,
            editor.size(),
            self.parent().parent().parent().geometry())
        editor.setGeometry(spawnRect) # apply the new geometry

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        '''
        '''
        s = index.data(SceneDataRole.SceneRole) # get scene object
        editor.ui.iReleaseDate.setDate(
            index.data(SceneDataRole.DateRole))
        editor.ui.iPaysite.setText(
            index.data(SceneDataRole.PaysiteRole)) # fmt'd paysite
        editor.ui.iTitle.setText(index.data(SceneDataRole.TitleRole))
        editor.ui.performerList.addItems(s.performers)
        editor.ui.lblBaseName.setText(s.sanitize()) # sanitized due to date parsing issues

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        '''
        '''
        s = model.data(index, SceneDataRole.SceneRole)
        flags = 0x0 # unset flags
        # Performers .. 0x1
        # Paysite ..... 0x2
        # Title ....... 0x4
        # ReleaseDate . 0x8
        vOld, nOld = s.is_valid(), s.viewname()
        hv = model.sourceModel().hashvalues # prevent duplicates
        flags |= model.setData(
            index,
            editor.ui.iReleaseDate.date().toPython(),
            SceneDataRole.DateRole) << 3
        flags |= model.setData(
            index,
            editor.ui.iPaysite.text(),
            SceneDataRole.PaysiteRole) << 1
        flags |= model.setData(
            index,
            editor.ui.iTitle.text(), SceneDataRole.TitleRole) << 2
        flags |= model.setData(
            index,
            [x.text() for x in editor.ui.performerList.findItems(
                '*', Qt.MatchWildcard)],
            SceneDataRole.PerformersRole) << 0
        vNew, nNew = s.is_valid(), s.viewname()
        if flags: # changes made, update the duptracker
            hv[nOld] = hv.get(nOld, 1) - 1
            hv[nNew] = hv.get(nNew, 0) + 1
        if vOld ^ vNew or flags & (0x1 << (model.filterRole() - Qt.UserRole)):
            model.invalidateFilter()
            # print(f'Invalidating "{flags:>08b}"')

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
        if index.model().sourceModel().hashvalues.get(s.viewname(), 0) > 1:
            painter.setPen(QColor('red'))
        released = str(index.data(SceneDataRole.DateRole))
        resolution = f'Resolution: {s.resolution()}'
        size = human_readable(s.size) # size as string
        title = index.data(SceneDataRole.TitleRole) if s.is_valid() else s.viewname()
        performers = index.data(SceneDataRole.PerformersRole) # perfs as string

        wPerfs, hPerfs = QFontMetrics(self.pFont).size(0, performers).toTuple()
        wSite, _ = painter.fontMetrics().size(0, paysite).toTuple()
        wTitle, hDefault = painter.fontMetrics().size(0, title).toTuple()
        wDate, _ = painter.fontMetrics().size(0, released).toTuple()
        wSize, hSize = QFontMetrics(self.sFont).size(0, size).toTuple()
        wResolution, _ = painter.fontMetrics().size(0, resolution).toTuple()

        x, y, w, h = option.rect.adjusted(5, 5, -5, -5).getRect() # layout coords
        w2, w3 = max(wPerfs, wSite, wTitle), max(wDate, wSize, wResolution)
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
                QRect(origin, QSize(w2, hDefault)), Qt.AlignLeft, s.viewname())
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
        return QSize(h, h) # TODO: implement a better way to estimate the size
