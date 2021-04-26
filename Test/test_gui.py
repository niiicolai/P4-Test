import unittest
import soundfile as sf
import numpy as np
import copy as cp
from soundData import SoundData
from config import ORIGINAL_NAMES, MANIPULATED_NAMES
from gui import Application


# TEST DATA
# The name of test wave file
#ORIGINAL_NAMES = ["./assets/sound/test.wav", "./assets/sound/test.wav"]
#MANIPULATED_NAMES = ["./assets/sound/test.wav", "./assets/sound/test.wav"]

# Create an application object used for the tests
APP = Application(ORIGINAL_NAMES, MANIPULATED_NAMES, False)

# Load the wave file using an external library
RAW_DATA, SAMPLE_RATE = sf.read(ORIGINAL_NAMES[0])
# Calculate time data for the raw audio data
RAW_TIME = np.linspace(0, len(RAW_DATA) / SAMPLE_RATE, num=len(RAW_DATA))
# Create a sound data object used for the tests
ORIGINAL_SOUND_DATA = SoundData(ORIGINAL_NAMES[0])
MANIPULATED_SOUND_DATA = SoundData(MANIPULATED_NAMES[0])
# Get the default phase shift, used to comparing
# DEFAULT_PHASE_SHIFT = ORIGINAL_SOUND_DATA.get_default_phase_shift()

# Create a version of the raw data with double amplitude
# and is shifted 1 in the amplitude domain
RAW_DATA_DOUBLE_AMP_0_SHIFT = 2 * cp.copy(RAW_DATA) + 0

# Create a version of the raw time that is shifted
# by 2 in the phase shift domain + the default phase shift value
RAW_TIME_SHIFTED_BY_2 = cp.copy(RAW_TIME) #+ (DEFAULT_PHASE_SHIFT + 2)


class TestApplication(unittest.TestCase):
    """Used to test the class Application in gui.py"""

    """
       OTHER METHODS:
       The Application class contains also the following method.
       But it is concluded that the results of executing them
       easily can be validated either using the visual- or 
       auditory system, or are simply not used in the main 
       application but only exist for debugging purpose. 

       - show_goodbye_widgets()
       - show_sound_control()
       - plot_current_files()
       - create_graph()
       - create_graph_placeholder()
       - create_phase_shift_control()
       - create_amplitude_control()
       - create_sound_control_widgets()
       - create_goodbye_widgets()
       - create_welcome_widgets()
       - clear_page()
       - toggle_play()
       - next_audio_files()
    """


if __name__ == '__main__':
    unittest.main()
