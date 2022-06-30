from PySide6.QtCore import QRect, QSize, Qt, QPoint
from PySide6.QtGui import QPainter, QPalette, QColor, QFont, QImage, QFontMetrics, QIcon, QBrush, QPixmap, QWindow
from PySide6.QtWidgets import QStyle, QStyledItemDelegate, QStyleOptionViewItem
from sxtools.ui.scenelistmodel import SceneModel
from sxtools.utils import human_readable


class SceneDelegate(QStyledItemDelegate):

    def __init__(self, parent=None) -> None:
        '''
        '''
        super(SceneDelegate, self).__init__(parent)
        self.model = self.parent().model()

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
        paysite = index.data(SceneModel.UserRoles.Paysite)
        performers = index.data(SceneModel.UserRoles.Performers)
        released = index.data(SceneModel.UserRoles.Date)
        resolution = f'Resolution: {index.data(SceneModel.UserRoles.Resolution)}'
        size = human_readable(index.data(SceneModel.UserRoles.Size)) # always set
        title = index.data(SceneModel.UserRoles.Title)
        # style & pens & fonts & metrics
        painter.setPen(option.palette.color(QPalette.Normal, cr))
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # painter.setFont(QFont('InputMono', painter.font().pointSize(), QFont.Condensed, italic=True))
        defaultFont = painter.font() # for fall-back purposes
        perfsFont, sizeFont = painter.font(), painter.font()
        perfsFont.setBold(True)
        perfsFont.setPointSize(defaultFont.pointSize() * 1.4)
        perfsFM = QFontMetrics(perfsFont)
        perfsSize = perfsFM.size(QFont.MixedCase, performers)
        paysiteSize = painter.fontMetrics().size(0, paysite)
        titleSize = painter.fontMetrics().size(0, title)
        releasedSize = painter.fontMetrics().size(0, released)
        sizeFont.setBold(True)
        sizeFont.setPointSize(defaultFont.pointSize() * 1.5)
        sizeFM = QFontMetrics(sizeFont)
        sizeSize = sizeFM.size(QFont.MixedCase, size)
        resolutionSize = painter.fontMetrics().size(0, resolution)
        # layout defining
        x, y, w, h = option.rect.adjusted(5, 5, -5, -5).getRect() # layout coordinates
        descColSize = max(
            perfsSize.width(), paysiteSize.width(), titleSize.width())
        infoColSize = max(
            releasedSize.width(), sizeSize.width(), resolutionSize.width())
        descColX, infoColX = x + h + 5, w - infoColSize
        # column 1: draw circle thumbnail
        painter.drawImage(QRect(x, y, h, h), SceneDelegate.circledIcon(thumbnail, h))
        # calculate rows count
        rows = sum(map(bool, [performers, paysite, not title.startswith(performers)]))
        # column 2: draw perfs, paysite & title
        if rows == 3:
            performersRect = QRect(descColX, y, descColSize, perfsSize.height())
            painter.setFont(perfsFont)
            painter.drawText(performersRect, Qt.AlignLeft, performers)
            painter.setFont(defaultFont)
            paysiteRect = performersRect.adjusted(
                0, performersRect.height() + 1, 0, paysiteSize.height() + 1)
            painter.drawText(paysiteRect, Qt.AlignLeft, paysite)
            titleRect = paysiteRect.adjusted(0, paysiteRect.height() + 1, 0, titleSize.height() + 1)
            painter.drawText(titleRect, Qt.AlignLeft, title)
        elif rows == 2:
            descColY = y + (h - (perfsSize.height() + paysiteSize.height()) >> 1)
            performersRect = QRect(descColX, descColY, descColSize, perfsSize.height())
            painter.setFont(perfsFont)
            painter.drawText(performersRect, Qt.AlignLeft, performers)
            painter.setFont(defaultFont)
            paysiteRect = performersRect.adjusted(
                0, performersRect.height() + 1, 0, paysiteSize.height() + 1)
            painter.drawText(paysiteRect, Qt.AlignLeft, paysite)
        else: # 1 row only
            titleRect = QRect(descColX, y, descColSize, h)
            painter.drawText(titleRect, Qt.AlignLeft | Qt.AlignVCenter, title)
        # columns 3: draw date, size & resolution
        releasedRect = QRect(infoColX, y, infoColSize, releasedSize.height())
        painter.drawText(releasedRect, Qt.AlignHCenter, released)
        sizeRect = releasedRect.adjusted(
            0, releasedRect.height() + 1, 0, sizeSize.height() + 1)
        painter.setFont(sizeFont)
        painter.drawText(sizeRect, Qt.AlignCenter, size)
        painter.setFont(defaultFont)
        resolutionRect = sizeRect.adjusted(0, sizeRect.height() + 1, 0, resolutionSize.height() + 1)
        painter.drawText(resolutionRect, Qt.AlignHCenter, resolution)

    def sizeHint(self, option: QStyleOptionViewItem, index) -> QSize:
        '''
        '''
        return QSize(58, 58) # TODO: implement a better way to estimate the size
