# P4-App
An application designed to let a user align two versions 
of the same audio file, while they can hear the two versions 
divided into a left and right speaker. After aligning all of
the available audio files, the application calculate the
differences between the phase of the original and manipulated
versions and output it to a csv file, 
found under assets/csv/result.csv   

![Example of application](https://github.com/niiicolai/P4-App/blob/main/assets/images/ExampleImage.JPG?raw=true)

# Table of contents
* [Main](https://github.com/niiicolai/P4-App#mainpy)
* [Configuration](https://github.com/niiicolai/P4-App#configpy)
* [GUI](https://github.com/niiicolai/P4-App#guipy)
* [CSV Writer](https://github.com/niiicolai/P4-App#csvwriterpy)
* [Sound Data](https://github.com/niiicolai/P4-App#sounddatapy)
* [Sound Modifier](https://github.com/niiicolai/P4-App#soundmodifierpy)
* [Unit Test](https://github.com/niiicolai/P4-App#unit-test)

# main.py
Initialize the application by creating an instance of the Application object,
using the parameters from `config.py`, and executing the `mainloop()` method.

# config.py
Contains configuration variables used to initialize the application. 

* `GRAPH_AUDIO` set to true, to see a graph of the audio files (*For debugging*)
* `FILE_PATH` specifies the directory for sound files
* `ORIGINAL_NAMES` specifies the names of the original sound files
* `MANIPULATED_NAMES` specifies the names of the manipulated sound files

# gui.py
Contains a class used to implement the main GUI features.

**The 4 steps below provide the general usage of this class**

1. import class
```python
from gui import Application
```

2. Create some test data
```python
ORIGINAL_NAMES = ["test.wav"]
MANIPULATED_NAMES = ["reverb_test.wav"]
```

3. Create an Application object a list of file paths to original and manipulated names
```python
app = Application(ORIGINAL_NAMES, MANIPULATED_NAMES)
```

4. Run the main loop to show the GUI
```python
app.mainloop()
```

# csvWriter.py
Contains a class used to write the state of the sound files to a
CSV file, after being manipulated through the sound control system.

**The 4 steps below provide the general usage of this class**

1. import class
```python
from csvWriter import CSVWriter
```

2. Create some test data
```python
data = [{
  "original":{"amplitude":1, "phase_shift":0},
  "manipulated":{"amplitude":1, "phase_shift":0}
}]
```

3. Create a CSVWriter object using the data
```python
writer = CSVWriter(data)
```

4. Write the data to a CSV file specified at the path above
```python
writer.save()
```

# soundData.py
Contains a class used to easy manipulate an audio file,
plot its graph, and listen to its output.

**The 7 steps below provide the general usage of this class**

1. import class
```python
from soundData import SoundData
```

2. Create a sound data object using the original data
```python
original_sound = SoundData('original_sound.wav')
```

3. Load a manipulated version of the original data
```python
manipulated_sound = SoundData('manipulated_sound.wav')
```

4. Manipulate the sound
```python
manipulated_sound.set_phase_shift(1)  # +1
manipulated_sound.set_amplitude_shift(.1) # +.1
manipulated_sound.set_amplitude(5) # +5
```

5. Plot the sounds against each other
```python
original_sound.plot_against(manipulated_sound)
```

6. Play the original sound using the left speaker
```python
original_sound.play(channel=1)
```

7. Play the manipulated sound using the right speaker
```python
manipulated_sound.play(channel=2)
```

# soundModifier.py
Contains a class used to change amplitude and current phase of
a manipulated sound, to play the original and manipulated
sounds sequential, and to save the state of the manipulation
compared to the original sounds to a CSV file.

**The 10 steps below provide the general usage of this class**

1. import class
```python
from soundModifier import SoundModifier
# Note: import matplotlib to plot the graph
# in step 4 and 5
import matplotlib.pyplot as plt
```

2. Create some test data
```python
ORIGINAL_NAMES = ["test.wav"]
MANIPULATED_NAMES = ["reverb_test.wav"]
```

3. Create a SoundModifier object a list of file paths to original and manipulated names
```python
sound_modifier = SoundModifier(ORIGINAL_NAMES, MANIPULATED_NAMES)
```

4. Graph current state of original sound file
```python
x = sound_modifier.current_original_sound().get_time()
y = sound_modifier.current_original_sound().get_data()
plt.figure(1)
plt.plot(x, y)
plt.show()
```

5. Graph current state of manipulated sound file
```python
x = sound_modifier.current_manipulated_sound().get_time()
y = sound_modifier.current_manipulated_sound().get_data()
plt.figure(1)
plt.plot(x, y)
plt.show()
```

6. Change amplitude of manipulated sound
```python
sound_modifier.set_amplitude(amplitude=2)
```

7. Phase shift manipulated sound
```python
sound_modifier.set_phase_shift(phase_shift=.5)
```

8. Toggle play
```python
sound_modifier.toggle_play()
```

9. Move to next audio files
```python
sound_modifier.next_audio_files()
```

10. Check if all audio files has been played
```python
if sound_modifier.get_finished_sequence() > 0:
  print("ALL SOUND FILES HAS BEEN HEARD")
```

# Unit Test
The project uses the [`unittest`](https://docs.python.org/3/library/unittest.html) library to implement
unit tests to test the application. All unit test 
classes can be found in the `/Tests` directory.

**Procedure to validate all tests:**
1. Open the terminal
2. Run [`nose2`](https://docs.nose2.io/en/latest/)
```
$ python -m nose2
```

**Example:**

```
(venv) C:\Users\PCName\PycharmProjects\P4-App>python -m nose2
....................
----------------------------------------------------------------------
Ran 20 tests in 0.028s

OK

```