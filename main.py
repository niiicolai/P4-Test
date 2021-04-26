# Dependencies
from config import ORIGINAL_NAMES, MANIPULATED_NAMES, GRAPH_AUDIO
from gui import Application


if __name__ == '__main__':
    # Create an application object
    app = Application(ORIGINAL_NAMES, MANIPULATED_NAMES, GRAPH_AUDIO)
    # Activate the main loop
    app.mainloop()

    # if the app stops
    if not app.arduino_interface is None:
        app.arduino_interface.stop()
