from PySide6.QtCore import QRect, QSize, Qt, QPoint
from PySide6.QtGui import QBrush, QFont, QFontMetrics, QImage, QPainter, QPalette
from PySide6.QtWidgets import QStyle, QStyledItemDelegate, QStyleOptionViewItem, QApplication
from sxtools.ui.scenelistmodel import SceneDataRole, SceneModel
from sxtools.utils import human_readable


class SceneDelegate(QStyledItemDelegate):

    def __init__(self, parent=None) -> None:
        '''
        '''
        super(SceneDelegate, self).__init__(parent) # init parent methods

        self.pFont = QFont(
            QApplication.font().family(), 12, QFont.Bold)
        self.sFont = QFont(
            QApplication.font().family(), 13, QFont.Bold)

    @staticmethod
    def circledIcon(icon: QImage, size: int = 48) -> QImage:
        '''
        '''
        side = min(icon.width(), icon.height())
        squaded = icon.copy(icon.width() - side >> 1, icon.height() - side >> 1, side, side)
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

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index) -> None:
        '''
        '''
        cr = QPalette.Text # set default Qt.ColorRole
        if option.state & QStyle.State_Selected:
            cr = QPalette.HighlightedText
            painter.fillRect(
               option.rect,
               option.palette.brush(QPalette.Normal, QPalette.Highlight))
        # retrieve data from the model, TODO: get a scene obj
        thumbnail = index.data(Qt.DecorationRole) # get thumbnail for the scene
        paysite = index.data(SceneDataRole.PaysiteRole)
        performers = index.data(SceneDataRole.PerformersRole)
        released = index.data(SceneDataRole.DateRole)
        resolution = f'Resolution: {index.data(SceneDataRole.ResolutionRole)}'
        size = human_readable(index.data(SceneDataRole.SizeRole)) # always set
        title = index.data(SceneDataRole.TitleRole)
        # style & pens & fonts & metrics
        painter.setPen(option.palette.color(QPalette.Normal, cr))
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        defaultFont = painter.font() # for fall-back purposes

        perfsSize = QFontMetrics(self.pFont).size(QFont.MixedCase, performers)
        paysiteSize = painter.fontMetrics().size(0, paysite)
        titleSize = painter.fontMetrics().size(0, title)
        releasedSize = painter.fontMetrics().size(0, released)
        sizeSize = QFontMetrics(self.sFont).size(0, size)
        resolutionSize = painter.fontMetrics().size(QFont.MixedCase, resolution)

        x, y, w, h = option.rect.adjusted(5, 5, -5, -5).getRect() # layout coordinates

        c2ndW = max(i.width() for i in [
            perfsSize, paysiteSize, titleSize])
        c3rdW = max(i.width() for i in [
            releasedSize, sizeSize, resolutionSize])
        c2ndX, c3rdX = x + h + 5, w - c3rdW
        # column 1: Thumbnail
        painter.drawImage(QRect(x, y, h, h), SceneDelegate.circledIcon(thumbnail, h))
        # column 2: Description
        lines = sum(
            map(bool, [
                performers,
                paysite,
                not title.startswith(performers)]))
        titleRect = QRect(c2ndX, y, c2ndW, h) # baseRect for 1 liner
        if lines > 1:
            baseRect = QRect(
                c2ndX,
                y if lines == 3 else y + (h - (perfsSize.height() + 1 + paysiteSize.height()) >> 1),
                c2ndW,
                perfsSize.height())
            painter.setFont(self.pFont)
            painter.drawText(baseRect, Qt.AlignLeft, performers)
            painter.setFont(defaultFont)
            paysiteRect = baseRect.adjusted(
                0, baseRect.height() + 1, 0, paysiteSize.height() + 1)
            painter.drawText(paysiteRect, Qt.AlignLeft, paysite)
            titleRect = paysiteRect.adjusted(
                0, paysiteRect.height() + 1, 0, titleSize.height() + 1)
        if lines != 2:
            painter.drawText(titleRect, Qt.AlignLeft | Qt.AlignVCenter, title)
        # column 3: Information
        releasedRect = QRect(c3rdX, y, c3rdW, releasedSize.height())
        painter.drawText(releasedRect, Qt.AlignHCenter, released)
        sizeRect = releasedRect.adjusted(
            0, releasedRect.height() + 1, 0, sizeSize.height() + 1)
        painter.setFont(self.sFont)
        painter.drawText(sizeRect, Qt.AlignCenter, size)
        painter.setFont(defaultFont)
        resolutionRect = sizeRect.adjusted(0, sizeRect.height() + 1, 0, resolutionSize.height() + 1)
        painter.drawText(resolutionRect, Qt.AlignHCenter, resolution)

    def sizeHint(self, option: QStyleOptionViewItem, index) -> QSize:
        '''
        '''
        h = 5 + QFontMetrics(option.font).height() + 1 + QFontMetrics(self.pFont).height() + 1 + QFontMetrics(option.font).height() + 5
        return QSize(h, h) # TODO: implement a better way to estimate the size
