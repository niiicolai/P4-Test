# Dependencies
import threading
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import sounddevice
import time
import copy as cp

"""
    The 7 steps below provide the general usage of this class

    1. import class
    from soundData import SoundData

    2. Create a sound data object using the original data
    original_sound = SoundData('original_sound.wav')

    3. Load a manipulated version of the original data
    manipulated_sound = SoundData('manipulated_sound.wav')

    4. Manipulate the sound
    manipulated_sound.set_phase_shift(1)  # +1
    manipulated_sound.set_amplitude_shift(.1) # +.1
    manipulated_sound.set_amplitude(5) # +5

    5. Plot the sounds against each other
    original_sound.plot_against(manipulated_sound)

    6. Play the original sound using the left speaker
    original_sound.play(channel=1)

    7. Play the manipulated sound using the right speaker
    manipulated_sound.play(channel=2)
"""


class SoundData:
    """A class used to easy manipulate an audio file,
       plot its graph, and listen to its output"""

    def __init__(self, filename):
        """The class constructor. Reads an audio file with
           the name provided as an argument and save its
           data as a 1-D. array of amplitude and a related
           sample rate"""
        self.__data, self.__sample_rate = sf.read(filename)
        self.__amplitude = 1
        self.__amplitude_shift = 0
        self.__phase_shift = 0
        self.__is_playing = False
        self.__possible_duration = 1.6

    def get_shifted_data_array(self):
        """Returns the audio audio shifted either left or right
           using zeros matching the phase shift in a given direction"""

        # Calculate number of shifts
        shifts = np.zeros(int(self.__sample_rate * abs(self.__phase_shift)))
        # self.__sample_rate => 44100
        # abs(self.__phase_shift) => et tal mellem 0 og 1.6
        # lad os sige at det i dette eksempel er 0.5
        # self.__sample_rate * abs(self.__phase_shift) = 44100 * 0.5 = 22050 antal nuller
        # før amplitude dataen
        # shifts => [0, 0, ..., 0] (22050 nuller)

        # For at beregne antal nuller tilgængelige til phase shifting, se nedenstående:
        # Bemærk dette step ikke bliver brugt, men kan hjælpe med det større billede
        # possible_shifts = np.zeros(int(self.__sample_rate * self.__possible_duration))
        # self.__sample_rate => 44100
        # self.__possible_duration => præcis 1.6 (ikke en range som med phase shift)
        # self.__sample_rate * self.__possible_duration = 44100 * 1.6 = 70560 antal nuller
        # Bemærk ovenstående tal betyder vi kan tilføje 70560 antal nuller på venstre side, højre side
        # eller fordelt skævt eller ligeligt på begge sider
        # possible_shifts => [0, 0, ..., 0] (70560 nuller)

        # Copy original data
        copied_data = cp.copy(self.__data)
        # Et array som indeholder amplitude data for selve audio filen
        # Dette array indeholder både nuller, negative og positive tal.
        # Da værdierne i i dette tilfælde er forskelligt fra lydfil til lydfil
        # så lader vi som om (for eksemplets skyld) copied_data ser ud på følgende måde:
        # copied_data => [1, 2, 3, 4]

        # Calculate missing shifts
        missing_zeros = int(self.__sample_rate * self.__possible_duration) - len(shifts)
        # self.__sample_rate => 44100
        # self.__possible_duration => præcis 1.6 (ikke en range som med phase shift)
        # len(shifts) => længden af shifts variablen, i dette eksempel: 22050 (nuller)
        # int(self.__sample_rate * self.__possible_duration)-len(shifts) => 70560 - 22050 = 48510
        # Tallet, 48510, betyder at vi skal tilføje 48510 nuller på højre side
        # missing_zeros => 48510

        missing_shifts = np.zeros(abs(missing_zeros))
        # missing_shifts => [0, 0, ..., 0] (48510 nuller)

        # Herfra er der 3 vigtige parameter:
        # shifts => S[0, 0, ..., 0] (22050 nuller)
        # copied_data => [1, 2, 3, 4]
        # missing_shifts=> M[0, 0, ..., 0] (48510 nuller)
        # Bemærk jeg har indsat et 'S' og et 'M' foran
        # shifts og missing_shifts variablen så vi kan
        # se forskel på dem i efterfølgende kommentarer.

        # Insert shifts before
        copied_data = np.append(shifts, copied_data)
        # copied_data => S[0, 0, ..., 0] + [1, 2, 3, 4]

        # Insert missing shifts after
        copied_data = np.append(copied_data, missing_shifts)
        # Bemærk nedenstående er 3 eksempler på det samme:
        # copied_data => S[0, 0, ..., 0] + [1, 2, 3, 4] + M[0, 0, ..., 0]
        # copied_data => [0, 0, ..., 0 (22050 nuller), 1, 2, 3, 4, 0, 0, ..., 0 (48510 nuller)]
        # copied_data => [0, 0, ..., 0, 1, 2, 3, 4, 0, 0, ..., 0]

        return copied_data

    def set_amplitude(self, amplitude):
        """Changes the amplitude of the final data output"""
        self.__amplitude = amplitude

    def set_amplitude_shift(self, amplitude_shift):
        """Shifts the amplitude of the final data output,
           valid range: (0.0-0.9)"""
        self.__amplitude_shift = amplitude_shift

    def set_phase_shift(self, phase_shift):
        """Shifts the phase of the final data output,
           currently only working in the positive direction
           when playing the sound, however it works when plotting
           the graph in both directions"""
        self.__phase_shift = phase_shift

    def get_data(self):
        """Returns the data multiplied with the amplitude parameter
           and shifted by adding the amplitude-shift parameter"""
        return self.get_shifted_data_array() * self.__amplitude  # + self.__amplitude_shift

    def get_amplitude_shift(self):
        """Returns the amplitude shift parameter"""
        return self.__amplitude_shift

    def get_amplitude(self):
        """Returns the amplitude parameter"""
        return self.__amplitude

    def get_phase_shift(self):
        """Returns the phase shift parameter"""
        return self.__phase_shift

    def get_sample_rate(self):
        """Returns the audio files sample rate"""
        return self.__sample_rate

    def get_time(self):
        """Returns an array of evenly spaced time points used
           to represent the audio files time sequence on the x-axis"""
        data = self.get_data()
        return np.linspace(0, len(data) / self.__sample_rate, num=len(data))

    def save(self, name):
        """Save the current state of the data to a file"""
        sounddevice.write(name, self.get_data(), self.__sample_rate)

    def play(self, channel):
        """Plays the current state of the audio data"""
        sounddevice.play(self.get_data(), self.__sample_rate, mapping=[channel])
        return sounddevice.wait()

    def play_async(self, channel):
        """Play the audio file in a separate thread"""
        thread = threading.Thread(target=self.play, args=(channel,))
        thread.start()

    def plot(self, title="Plot of a single audio wave"):
        """Plot the current state of data with time on the
           x-axis and amplitude on the y-axis"""
        plt.figure(1)
        plt.title(title)
        plt.plot(self.get_time(), self.get_data())
        plt.show()

    def plot_against(self, other, title="Plot of two audio waves"):
        """Plot the current state of data with time on the
           x-axis and amplitude on the y-axis, against the
           same parameters on another sound data object"""
        plt.figure(1)
        plt.title(title)
        plt.plot(self.get_time(), self.get_data())
        plt.plot(other.get_time(), other.get_data())
        plt.show()
