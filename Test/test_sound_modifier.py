import unittest
import soundfile as sf
import numpy as np
import copy as cp
import random
from config import ORIGINAL_NAMES_C, MANIPULATED_NAMES_C
from soundData import SoundData
from soundModifier import SoundModifier
from csvWriter import ORIGINAL_KEY, MANIPULATED_KEY, \
     AMPLITUDE_KEY, PHASE_SHIFT_KEY

# TEST DATA
# The name of test wave file
# ORIGINAL_NAMES = ["./assets/sound/test.wav", "./assets/sound/test.wav"]
# MANIPULATED_NAMES = ["./assets/sound/test.wav", "./assets/sound/test.wav"]

# Create a sound modifier object used for the tests
SOUND_MODIFIER = SoundModifier(ORIGINAL_NAMES_C, MANIPULATED_NAMES_C)

# Load the wave file using an external library
RAW_DATA, SAMPLE_RATE = sf.read(ORIGINAL_NAMES_C[0])
# Calculate time data for the raw audio data
RAW_TIME = np.linspace(0, len(RAW_DATA) / SAMPLE_RATE, num=len(RAW_DATA))
# Create a sound data object used for the tests
ORIGINAL_SOUND_DATA = SoundData(ORIGINAL_NAMES_C[0])
MANIPULATED_SOUND_DATA = SoundData(MANIPULATED_NAMES_C[0])
# Get the default phase shift, used to comparing
# DEFAULT_PHASE_SHIFT = ORIGINAL_SOUND_DATA.get_default_phase_shift()

# Create a version of the raw data with double amplitude
# and is shifted 1 in the amplitude domain
RAW_DATA_DOUBLE_AMP_0_SHIFT = 2 * cp.copy(RAW_DATA) + 0

# Create a version of the raw time that is shifted
# by 2 in the phase shift domain + the default phase shift value
RAW_TIME_SHIFTED_BY_2 = cp.copy(RAW_TIME) #+ (DEFAULT_PHASE_SHIFT + 2)


class TestSoundModifier(unittest.TestCase):
    """Used to test the class SoundModifier in soundModifier.py"""

    def test_get_current_sound_index(self):
        """Ensure get_current_sound_index
           returns the correct index value"""
        self.assertEqual(SOUND_MODIFIER.get_current_sound_index(), 0, "Should be equal")

    def test_get_should_play(self):
        """Ensure get_should_play returns true
           after executing toggle_play and
           ensure it returns false after
           executing toggle_play again"""
        SOUND_MODIFIER.toggle_play(mute=True)
        self.assertEqual(SOUND_MODIFIER.get_should_play(), True, "Should be equal")
        SOUND_MODIFIER.toggle_play(mute=True)
        self.assertEqual(SOUND_MODIFIER.get_should_play(), False, "Should be equal")

    def test_get_number_of_sounds(self):
        """Ensure get_number_of_sounds
           output the correct number of sounds"""
        self.assertEqual(SOUND_MODIFIER.get_number_of_sounds(), 3, "Should be equal")

    def test_get_finished_sequence(self):
        """Ensure get_finished_sequence
           increase after listening to all
           available sound files"""
        for n in ORIGINAL_NAMES_C:
            SOUND_MODIFIER.next_audio_files()
        self.assertEqual(SOUND_MODIFIER.get_finished_sequence(), 1, "Should be equal")

    def test_append_current_result_data(self):
        """Ensure append_current_result_data
           appends a dictionary of the current
           sound states to the result list"""
        data = {
            ORIGINAL_KEY: {
                AMPLITUDE_KEY: SOUND_MODIFIER.current_original_sound().get_amplitude(),
                PHASE_SHIFT_KEY: SOUND_MODIFIER.current_original_sound().get_phase_shift()
            },
            MANIPULATED_KEY: {
                AMPLITUDE_KEY: SOUND_MODIFIER.current_manipulated_sound().get_amplitude(),
                PHASE_SHIFT_KEY: SOUND_MODIFIER.current_manipulated_sound().get_phase_shift()
            }
        }
        next_state = cp.copy(SOUND_MODIFIER.get_results())
        next_state.append(data)
        SOUND_MODIFIER.append_current_result_data()
        self.assertEqual(SOUND_MODIFIER.get_results(), next_state, "Should be equal")

    def test_randomize_original_sound_phase_shift(self):
        """Ensure randomize_original_sound_phase_shift
           updates the current phase shift of all
           original sounds to a new random value
           between a given range"""
        initial_state = cp.copy(SOUND_MODIFIER.get_original_sound_files())[0].get_phase_shift()
        SOUND_MODIFIER.randomize_original_sound_phase_shift()
        updated_state = SOUND_MODIFIER.get_original_sound_files()
        self.assertNotEqual(initial_state, updated_state[0].get_phase_shift(), "Should not be equal")

    """
        OTHER METHODS:
        The SoundModifier class contains also the following method.
        But it is concluded that the results of executing them
        easily can be validated either using the visual- or 
        auditory system, or are simply not used in the main 
        application but only exist for debugging purpose. 

        - play_audio_files()
        - toggle_play()
        - get_results()
        - get_original_sound_files()
        - get_manipulated_sound_files()
    """


if __name__ == '__main__':
    unittest.main()
