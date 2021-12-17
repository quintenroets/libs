try:
    import dbus
    from libs.popup import Popup as ProgressBar
except:
    session_bus = None
    from libs.cliprogress import Progress as ProgressBar
