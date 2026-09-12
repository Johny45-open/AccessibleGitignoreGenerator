from PyQt6.QtWidgets import QLabel, QWidget, QMessageBox, QApplication
from PyQt6.QtCore import QTimer, Qt
try:
    from PyQt6.QtGui import QAccessible  # type: ignore
except ImportError:
    QAccessible = None  # type: ignore
    try:
        from PyQt6.QtCore import QAccessible  # type: ignore
    except ImportError:
        QAccessible = None  # type: ignore


# PKIE vzor: zádný SAPI/QTextToSpeech. Hlas = NVDA pres MSAA/UIA.
# Toto je sjednocený helper – zivá oblast + debounce + focus restore.

_last_announce_text: str = ""
_last_announce_ms: int = 0
_announcer_label: QLabel | None = None


def set_accessible_name(widget: QWidget, name: str):
    widget.setAccessibleName(name)
    widget.setAccessibleDescription(name)


def create_label(text: str, buddy: QWidget | None = None, accessible_name: str | None = None) -> QLabel:
    label = QLabel(text)
    label.setWordWrap(True)
    label.setTextInteractionFlags(label.textInteractionFlags() | label.textInteractionFlags())
    if buddy is not None:
        label.setBuddy(buddy)
    if accessible_name:
        label.setAccessibleName(accessible_name)
    else:
        label.setAccessibleName(text)
    return label


def create_focusable_label(text: str, accessible_name: str | None = None) -> QLabel:
    """PKIE vzor IntroPage.label – focusable label pro NVDA."""
    label = QLabel(text)
    label.setWordWrap(True)
    label.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    label.setAccessibleName(accessible_name or text)
    return label


def focus_widget_delayed(widget: QWidget):
    QTimer.singleShot(0, widget.setFocus)


def get_or_create_announcer(parent: QWidget) -> QLabel:
    """Skrytá zivá oblast – jako PKIE statusLabel. Nevytvári paralelní TTS."""
    global _announcer_label
    if _announcer_label is not None:
        try:
            # pokud parent zmenil, presunout
            if _announcer_label.parent() is not parent and parent is not None:
                _announcer_label.setParent(parent)
        except RuntimeError:
            _announcer_label = None
    if _announcer_label is None:
        _announcer_label = QLabel(parent)
        _announcer_label.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        _announcer_label.hide()
        _announcer_label.setAccessibleName("")
    return _announcer_label


def announce(text: str, parent: QWidget | None = None, focus: bool = False):
    """Oznam pro NVDA – aktualizuje AccessibleName + QAccessible event.
    Debounce 300 ms potlacuje duplicitní hlásení (pozadavek: jedno oznámení = jedno prehrání).
    Neblokuje GUI, nevytvári druhý hlas."""
    global _last_announce_text, _last_announce_ms
    if not text or not text.strip():
        return
    t = text.strip()
    # debounce – stejný text do 300 ms preskoc
    try:
        from PyQt6.QtCore import QDateTime
        now = QDateTime.currentMSecsSinceEpoch()
        if t == _last_announce_text and (now - _last_announce_ms) < 300:
            return
        _last_announce_ms = now
    except Exception:
        pass
    _last_announce_text = t

    label = None
    if parent is not None:
        label = get_or_create_announcer(parent)
        label.setText(t)
        label.setAccessibleName(t)
        label.setAccessibleDescription(t)
        # QAccessible event – NVDA ho zachytí jako zmenu (pokud je dostupné)
        if QAccessible is not None:
            try:
                QAccessible.updateAccessibility(
                    QAccessible.QAccessibleEvent(label, QAccessible.Event.NameChanged)
                )
                QAccessible.updateAccessibility(
                    QAccessible.QAccessibleEvent(label, QAccessible.Event.ValueChanged)
                )
            except Exception:
                pass
        if focus:
            QTimer.singleShot(0, label.setFocus)
    else:
        w = QApplication.focusWidget()
        if w is not None:
            try:
                w.setAccessibleName(t)
                if QAccessible is not None:
                    QAccessible.updateAccessibility(
                        QAccessible.QAccessibleEvent(w, QAccessible.Event.NameChanged)
                    )
            except Exception:
                pass


def show_accessible_message(parent: QWidget | None, title: str, text: str,
                            icon: QMessageBox.Icon = QMessageBox.Icon.Information) -> int:
    """PKIE vzor: QMessageBox s StaysOnTopHint + AccessibleName, lokalizované tlacítko.
    Vrací result z exec()."""
    box = QMessageBox(parent)
    box.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
    box.setWindowTitle(title)
    box.setText(text)
    box.setIcon(icon)
    box.setStandardButtons(QMessageBox.StandardButton.Ok)
    try:
        btn = box.button(QMessageBox.StandardButton.Ok)
        if btn is not None:
            btn.setText("OK")
            btn.setAccessibleName("OK")
    except Exception:
        pass
    box.setAccessibleName(f"{title}. {text}")
    box.setAccessibleDescription(text)
    return box.exec()


def show_accessible_warning(parent: QWidget | None, title: str, text: str) -> int:
    return show_accessible_message(parent, title, text, QMessageBox.Icon.Warning)


def show_accessible_error(parent: QWidget | None, title: str, text: str) -> int:
    return show_accessible_message(parent, title, text, QMessageBox.Icon.Critical)


def show_accessible_question(parent: QWidget | None, title: str, text: str) -> bool:
    """PKIE can_close vzor – Ano/Ne s AccessibleName."""
    box = QMessageBox(parent)
    box.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
    box.setWindowTitle(title)
    box.setText(text)
    box.setIcon(QMessageBox.Icon.Question)
    box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    try:
        yes_btn = box.button(QMessageBox.StandardButton.Yes)
        no_btn = box.button(QMessageBox.StandardButton.No)
        if yes_btn:
            yes_btn.setText("Ano")
            yes_btn.setAccessibleName("Ano")
        if no_btn:
            no_btn.setText("Ne")
            no_btn.setAccessibleName("Ne")
        box.setDefaultButton(QMessageBox.StandardButton.No)
    except Exception:
        pass
    box.setAccessibleName(f"{title}. {text}")
    ret = box.exec()
    return ret == QMessageBox.StandardButton.Yes


def focus_with_restore(widget_to_focus: QWidget, prev_widget: QWidget | None = None):
    """Obnova fokusu po dialogu – QTimer.singleShot(0, prev.setFocus)."""
    target = prev_widget or widget_to_focus
    if target is None:
        return
    try:
        # over, ze widget jeste existuje
        if not target.isVisible():
            # pokud neni viditelny, zkus prvni focusable child
            pass
    except RuntimeError:
        return
    QTimer.singleShot(0, target.setFocus)
