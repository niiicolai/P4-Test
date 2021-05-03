# Dependencies
from config import ORIGINAL_NAMES_C, MANIPULATED_NAMES_C, \
    ORIGINAL_NAMES_T1, MANIPULATED_NAMES_T1, \
    ORIGINAL_NAMES_T2, MANIPULATED_NAMES_T2, \
    GRAPH_AUDIO

from gui import Application


# GROUP STATES
C_GROUP = "C-GROUP"
T1_GROUP = "T1-GROUP"
T2_GROUP = "T2-GROUP"

# Set to C_GROUP, T1_GROUP, or T2_GROUP depending on the test
CURRENT_TEST_GROUP = T1_GROUP

if __name__ == '__main__':

    original_names = {C_GROUP: ORIGINAL_NAMES_C,
                      T1_GROUP: ORIGINAL_NAMES_T1,
                      T2_GROUP: ORIGINAL_NAMES_T2}[CURRENT_TEST_GROUP]

    manipulated_names = {C_GROUP: MANIPULATED_NAMES_C,
                         T1_GROUP: MANIPULATED_NAMES_T1,
                         T2_GROUP: MANIPULATED_NAMES_T2}[CURRENT_TEST_GROUP]

    # Create an application object
    app = Application(original_names, manipulated_names, GRAPH_AUDIO)
    # Activate the main loop
    app.mainloop()

    # if the app stops
    if not app.arduino_interface is None:
        app.arduino_interface.stop()