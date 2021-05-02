# Dependencies
import threading
import random
import sounddevice
import numpy as np
from soundData import SoundData
from csvWriter import CSVWriter, ORIGINAL_KEY, \
    MANIPULATED_KEY, AMPLITUDE_KEY, PHASE_SHIFT_KEY

"""
    The 10 steps below provide the general usage of this class

    1. import class
    from soundModifier import SoundModifier
    # Note: import matplotlib to plot the graph
    # in step 4 and 5
    import matplotlib.pyplot as plt

    2. Create some test data
    ORIGINAL_NAMES = ["test.wav"]
    MANIPULATED_NAMES = ["reverb_test.wav"]

    3. Create a SoundModifier object a list of file paths to 
       original and manipulated names
    sound_modifier = SoundModifier(ORIGINAL_NAMES, MANIPULATED_NAMES)

    4. Graph current state of original sound file
    x = sound_modifier.current_original_sound().get_time()
    y = sound_modifier.current_original_sound().get_data()
    plt.figure(1)
    plt.plot(x, y)
    plt.show()

    5. Graph current state of manipulated sound file
    x = sound_modifier.current_manipulated_sound().get_time()
    y = sound_modifier.current_manipulated_sound().get_data()
    plt.figure(1)
    plt.plot(x, y)
    plt.show()

    6. Change amplitude of manipulated sound
    sound_modifier.set_amplitude(amplitude=2)

    7. Phase shift manipulated sound
    sound_modifier.set_phase_shift(phase_shift=.5)

    8. Toggle play
    sound_modifier.toggle_play()

    9. Move to next audio files
    sound_modifier.next_audio_files()

    10. Check if all audio files has been played
    if sound_modifier.get_finished_sequence() > 0:
        print("ALL SOUND FILES HAS BEEN HEARD")
"""


class SoundModifier:
    """A class used to change amplitude and current phase of
       a manipulated sound, to play the original and manipulated
       sounds sequential, and to save the state of the manipulation
       compared to the original sounds to a CSV file"""

    def __init__(self, original_names, manipulated_names):
        """The class constructor. Reads sound files
           as SoundData objects from the provided paths
           specified in the original and manipulated list arguments"""

        if len(original_names) != len(manipulated_names):
            raise Exception("The size of the arrays should be equal!")

        self.__original_sound_files = [SoundData(name) for name in original_names]
        self.__manipulated_sound_files = [SoundData(name) for name in manipulated_names]
        self.__amplitude_range = [1.6, 1.3, .9, .6, .3, 0, -.3, -.6, -.9, -1.3, -1.6]
        self.__phase_shift_range = [1.6, 1.3, .9, .6, .3, 0]  # , -.3, -.6, -.9, -1.3, -1.6]
        self.__results = []
        self.__should_play = False
        self.__amplitude = 0
        self.__phase_shift = 0
        self.__current_sound_index = 0
        self.__finished_sequence = 0

        # Ensure to randomize the original in the time domain
        # when initializing the class
        self.randomize_original_sound_phase_shift()

    def get_should_play(self):
        """Returns whether or not the
           modifier is playing the sounds"""
        return self.__should_play

    def get_current_sound_index(self):
        """Returns the current index
           of the list of sounds that
           will be used to play, and manipulate"""
        return self.__current_sound_index

    def current_original_sound(self):
        """Returns the current original sound
           based on the sound index"""
        return self.__original_sound_files[self.__current_sound_index]

    def current_manipulated_sound(self):
        """Returns the current manipulated sound
           based on the sound index"""
        return self.__manipulated_sound_files[self.__current_sound_index]

    def get_finished_sequence(self):
        """Returns the number of times
           all sounds has been played through"""
        return self.__finished_sequence

    def get_number_of_sounds(self):
        """Returns the numbers of sound files"""
        return len(self.__original_sound_files)

    def get_results(self):
        """Returns the results parameter"""
        return self.__results

    def get_original_sound_files(self):
        """Returns the original_sound_files parameter"""
        return self.__original_sound_files

    def get_manipulated_sound_files(self):
        """Returns the manipulated_sound_files parameter"""
        return self.__manipulated_sound_files

    def set_amplitude(self, amplitude):
        """Changes the amplitude of all
           manipulated sound files"""
        amplitude = float(amplitude)
        self.__amplitude = amplitude
        # Update manipulated sound data
        for s in self.__manipulated_sound_files:
            s.set_amplitude(amplitude)

    def set_phase_shift(self, phase_shift):
        """Changes the phase shift of all
           manipulated sound files"""
        phase_shift = float(phase_shift)
        self.__phase_shift = phase_shift
        # Update manipulated sound data
        for s in self.__manipulated_sound_files:
            s.set_phase_shift(phase_shift)

    def stop_play(self):
        if self.__should_play:
            self.__should_play = False
            sounddevice.stop()

    def toggle_play(self, mute=False):
        """Creates a thread that plays the audio files
           until should_play=false, if should_play
           is already true, should_play will be set
           to false, to stop the playing thread"""
        if self.__should_play:
            self.__should_play = False
            if not mute: sounddevice.stop()
        else:
            self.__should_play = True
            if not mute:
                thread = threading.Thread(target=self.play_audio_files)
                thread.start()

    def play_audio_files(self):
        """Play the 'current' sound files until should_play is false,
           where the original sound is output on the left speaker,
           and the manipulated is output on the right speaker"""

        run = True
        while run:
            data = np.column_stack([self.__original_sound_files[self.__current_sound_index].get_data(),
                                    self.__manipulated_sound_files[self.__current_sound_index].get_data()])
            sounddevice.play(data)
            sounddevice.wait()

            if not self.__should_play:
                run = False

    def append_current_result_data(self):
        """Appends the current state of the 'current' sound files
           to the results list"""
        self.__results.append({
            ORIGINAL_KEY: {
                AMPLITUDE_KEY: self.__original_sound_files[self.__current_sound_index].get_amplitude(),
                PHASE_SHIFT_KEY: self.__original_sound_files[self.__current_sound_index].get_phase_shift()
            },
            MANIPULATED_KEY: {
                AMPLITUDE_KEY: self.__manipulated_sound_files[self.__current_sound_index].get_amplitude(),
                PHASE_SHIFT_KEY: self.__manipulated_sound_files[self.__current_sound_index].get_phase_shift()
            }
        })

    def randomize_original_sound_phase_shift(self):
        """Set the phase_shift parameter of all the
           original sound files to a random value
           from the __phase_shift_range list"""
        # randomize original sounds' phase shift
        index = random.randint(0, len(self.__phase_shift_range) - 1)
        phase_shift = self.__phase_shift_range[index]
        if phase_shift == self.__original_sound_files[0].get_phase_shift():
            self.randomize_original_sound_phase_shift()
        else:
            for s in self.__original_sound_files:
                s.set_phase_shift(phase_shift)

    def next_audio_files(self):
        """Saves the current state of the original and manipulated sound file to
           a list of results, which is saved and reset for every time, the
           sound index has reach one cycle. Note: the method randomize the
           phase shift of the original sounds to avoid the original sounds
           always follows the same phase"""

        self.append_current_result_data()

        if self.__current_sound_index + 1 >= len(self.__original_sound_files):
            writer = CSVWriter(self.__results)
            writer.save()
            self.__results = []
            self.__finished_sequence += 1
            self.stop_play()
        else:
            self.__current_sound_index = (self.__current_sound_index + 1) % len(self.__original_sound_files)

            # stop current seq.
            if self.__should_play:
                self.toggle_play()

            self.randomize_original_sound_phase_shift()
