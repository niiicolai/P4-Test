# Dependencies
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from soundModifier import SoundModifier
from config import ARDUINO_INTERFACE
from arduino_controller import Arduino

"""
    The 4 steps below provide the general usage of this class

    1. import class
    from gui import Application

    2. Create some test data
    ORIGINAL_NAMES = ["test.wav"]
    MANIPULATED_NAMES = ["reverb_test.wav"]

    3. Create an Application object a list of file paths to 
       original and manipulated names
    app = Application(ORIGINAL_NAMES, MANIPULATED_NAMES)

    4. Run the main loop to show the GUI
    app.mainloop()
"""

# BUTTON COLORS
DEFAULT_BTN_BGG = "white"
ACTIVE_BTN_BGG = "red"

# TEXT COLORS
DEFAULT_TXT_COLOR = "black"
DEFAULT_BGG_COLOR = "white"

# FONTS
HEADER_FONT = ("Arial", 15, 'bold')
TITLE_FONT = ("Arial", 9, 'bold')
ALTERNATIVE_FONT = ("Arial", 12, 'bold')

# FRAME PROPERTIES
SIZE = "540x555"
TITLE = "P4 Project"

# SLIDER
SLIDER_TITLE_POSITION = (20, 180)
SLIDER_TITLE_SIZE = (15, 3)

# WIDGETS

C_BUTTON_POSITION = (170, 299)
C_BUTTON_WIDTH = 27
C_BUTTON_HEIGHT = 2

D_BUTTON_WIDTH = 20
D_BUTTON_HEIGHT = 2
D_BUTTON_POSITION = (370, 495)

PLAY_BUTTON_OFFSET = 50


class Application(tk.Frame):
    """A class used to implement the main GUI features"""

    def __init__(self, original_names, manipulated_names, graph_audio=False):
        """The class constructor. Creates a
           sound modifier using the name paths"""
        master = tk.Tk()
        super().__init__(master)

        self.sound_modifier = SoundModifier(original_names, manipulated_names)
        self.master = master
        self.graph_audio = graph_audio
        self.master.geometry(SIZE)
        self.master.resizable(False, False)
        self.master.title(TITLE)
        self.callback_activated = False
        self.current_page = "THREE"
        self.next_callback = "TWO"
        self.phase_shift_slider = None
        self.ax = None
        self.create_demo_step_three()
        self.grid(row=0, column=0)
        self.master.protocol("WM_DELETE_WINDOW", self.on_quit)


        self.arduino_interface = None
        if ARDUINO_INTERFACE:
            self.arduino_interface = Arduino(gui=self)
            self.arduino_interface.listen_async()

    # TKINTER METHODS

    def on_quit(self):
        self.master.quit()
        self.sound_modifier.stop_play()

    def clear_page(self):
        """Loop through the frame's widgets
           and destroy them"""
        for w in self.master.winfo_children():
            w.destroy()

    # DEMO METHODS

    def recreate_demo_step(self):
        self.clear_page()
        self.create_demo_step_three()

    def create_demo_step_one(self):
        """Creates a page representing the first step of the
           interactive demo"""

        self.current_page = "ONE"
        self.create_top_background()
        self.create_top_panel("Step 1")
        self.create_top_small_panel("Before the actual test, you will have to complete the following demo.\n"
                                    "Imagine the graph below represents two sounds fx two piano chords.")
        self.create_graph()

        # Create play button
        button = tk.Button(self.master, text="OK", fg=DEFAULT_TXT_COLOR,
                           bg=DEFAULT_BGG_COLOR, width=D_BUTTON_WIDTH,
                           height=D_BUTTON_HEIGHT, command=self.confirm)
        # Place button
        button.place(x=D_BUTTON_POSITION[0], y=D_BUTTON_POSITION[1])

    def create_demo_step_two_callback(self):
        """Add widgets to the current page when step two's task is completed"""
        # Create play button
        button = tk.Button(self.master, text="OK", fg=DEFAULT_TXT_COLOR,
                           bg=DEFAULT_BGG_COLOR, width=D_BUTTON_WIDTH,
                           height=D_BUTTON_HEIGHT, command=self.confirm)
        # Place button
        button.place(x=D_BUTTON_POSITION[0], y=D_BUTTON_POSITION[1])

    def create_demo_step_two(self):
        """Creates a page representing the second step of the
           interactive demo"""
        self.clear_page()

        self.current_page = "TWO"
        self.callback_activated = False
        self.next_callback = "ONE"
        self.create_top_background()
        self.create_top_panel("Step 2")
        self.create_top_small_panel("Use the slider to the left to align the two sounds\n"
                                    "represented in the graph, until the button shows up.\n\n"
                                    "Click on the right or left side of the slider to\n"
                                    " move the slider to align the sounds.")
        self.create_graph()
        self.create_phase_shift_control(title_position=SLIDER_TITLE_POSITION, title_size=SLIDER_TITLE_SIZE,
                                        command=(lambda e: self.demo_phase_shift()))

    def create_demo_step_three_callback(self):
        """Add widgets to the current page when step three's task is completed"""
        # Create confirm button
        button = tk.Button(self.master, text="OK", fg=DEFAULT_TXT_COLOR,
                           bg=DEFAULT_BGG_COLOR, width=D_BUTTON_WIDTH,
                           height=D_BUTTON_HEIGHT, command=self.confirm)
        # Place button
        button.place(x=D_BUTTON_POSITION[0], y=D_BUTTON_POSITION[1])

    def create_demo_step_three(self):
        """Creates a page representing the third step of the
           interactive demo"""

        self.current_page = "THREE"
        self.callback_activated = False
        self.next_callback = "TWO"
        self.create_top_background()
        self.create_top_panel("Trial test - preparation for the real test")
        self.create_top_small_panel("Here you can try out the task of aligning the sounds. Use the play button to play\n"
                                    " and listen to the sounds repeatedly and align the two sounds until you think they match.\n\n"
                                    "You may find this difficult, but do your best. Adjust the volume on your laptop to a \n"
                                    "comfortable level. After some experimentation, an \"OK\" button will appear.\n"
                                    "When you feel comfortable with the task you can go\n"
                                    "to the actual listening test by pressing ‘OK’.")
        self.create_phase_shift_control()
        # self.create_phase_shift_control(title_position=SLIDER_TITLE_POSITION, title_size=SLIDER_TITLE_SIZE,
        #                                command=(lambda e: self.set_phase_shift()))
        self.create_play_button()

        # Create confirm button
        button = tk.Button(self.master, text="OK", fg=DEFAULT_TXT_COLOR,
                           bg=DEFAULT_BGG_COLOR, width=D_BUTTON_WIDTH,
                           height=D_BUTTON_HEIGHT, command=self.confirm)
        # Place button
        button.place(x=D_BUTTON_POSITION[0], y=D_BUTTON_POSITION[1])


    def create_demo_step_four(self):
        """Creates a page representing the fourth step of the
           interactive demo"""
        self.clear_page()

        if self.sound_modifier.get_should_play():
            self.sound_modifier.toggle_play()

        self.current_page = "FOUR"
        self.create_top_background()
        self.create_top_panel("Trial test completed")
        self.create_top_small_panel("You can now start the actual test. \n"
                                    "Alternatively, let the experimenter know if you have any questions at this point.\n")

        position_x = 200
        position_offset = 90

        button = tk.Button(self.master, text="Start test", fg=DEFAULT_TXT_COLOR,
                           bg=DEFAULT_BGG_COLOR, width=D_BUTTON_WIDTH,
                           height=D_BUTTON_HEIGHT, command=self.create_sound_control_widgets)
        button.place(x=position_x, y=C_BUTTON_POSITION[1])

        """
        button = tk.Button(self.master, text="Retry demo", fg=DEFAULT_TXT_COLOR,
                           bg=DEFAULT_BGG_COLOR, width=D_BUTTON_WIDTH,
                           height=D_BUTTON_HEIGHT, command=self.recreate_demo_step)
        button.place(x=position_x-position_offset, y=C_BUTTON_POSITION[1])
        """

    # WIDGETS METHODS

    def create_welcome_widgets(self):
        """Adds the necessary widgets
           to build the welcome page"""

        self.current_page = "WELCOME"
        self.create_top_background()
        self.create_top_panel("Welcome")
        self.create_top_small_panel("Please read the guidelines below\n\n")

        guidelines = "Your task is to synchronise two sounds using the vertical sliders on the screen.\n\n" \
                     "Before the test you have to complete a demo test that should learn you to perform the test.\n\n" \
                     "The purpose of this test is to analyse the ability to synchronise two sounds. \n\n" \
                     "The sound control test has one slider:\n" \
                     "Change the synchronisation(time shift)\n\n" \
                     "The sound control page has two buttons:\n" \
                     "1. The 'play' button can be used to listen to the sounds\n" \
                     "2. The 'next' button is used to confirm " \
                     "that you perceive the \ntwo sounds to be synchronised " \
                     "and you are ready to be\n presented to two new sounds.\n\n" \
                     "This process will continue until all 5 sounds are judged to be synchronised.\n\n" \
                     "Be careful when you press play the first time, it is recommended\n" \
                     "to set the local volume of your computer to a low value, and slowly\n" \
                     "increase it to a suitable volume level.\n\n" \
                     "You will listen to 5 sounds that should be synchronised,\n " \
                     "the test should take at least 5 minutes but you should take the time you need.\n\n" \
                     "Thank you for participating!"
        guidelines_label2 = tk.Label(self.master,
                                     text=guidelines,
                                     fg=DEFAULT_TXT_COLOR,
                                     width="78", height="22", font=TITLE_FONT)
        # position the label
        guidelines_label2.place(x=0, y=120)
        start_button_offset_y = 180
        start_button = tk.Button(self.master, text="OK, I understand", fg=DEFAULT_TXT_COLOR,
                                 bg=DEFAULT_BGG_COLOR, width=C_BUTTON_WIDTH, height=C_BUTTON_HEIGHT, command=self.confirm)
        start_button.place(x=C_BUTTON_POSITION[0], y=C_BUTTON_POSITION[1]+start_button_offset_y)

    def create_goodbye_widgets(self):
        """Adds the necessary widgets
           to build the goodbye page"""
        self.clear_page()

        self.current_page = "GOODBYE"
        self.create_top_background()
        self.create_top_panel("Thank you, for participating")
        self.create_top_small_panel("You can safely close the page now by pressing the x, up in the right corner.\n"
                                    "Feel free to contact the researchers if you have any questions,\n"
                                    " or would like to give feedback or would like to redraw your consent to use the data.\n"
                                    "All data collected is anonymous and cannot be traced back to a single individual.\n"
                                    "Insert image stating that this is a student project and that the students can be\n"
                                    "contacted by their group email or the email from the researcher.")

    def create_sound_control_widgets(self):
        """Adds the necessary widgets
           to build the sound control page"""
        self.clear_page()

        self.current_page = "SOUNDCONTROL"
        self.create_top_background()
        self.create_top_panel()
        text = f"Sound {self.sound_modifier.get_current_sound_index() + 1} out " \
               f"of {self.sound_modifier.get_number_of_sounds()}"
        self.create_top_small_panel(text)
        self.create_phase_shift_control()

        if not self.arduino_interface is None:
            self.toggle_play()
        else:
            self.create_play_button()

        # Create confirm button
        button = tk.Button(self.master, text="OK", fg=DEFAULT_TXT_COLOR,
                           bg=DEFAULT_BGG_COLOR, width=D_BUTTON_WIDTH, height=D_BUTTON_HEIGHT, command=self.confirm)
        button.place(x=D_BUTTON_POSITION[0], y=D_BUTTON_POSITION[1])

    # SINGLE WIDGETS METHODS

    def create_top_background(self):
        """Creates a label with no text and a white background
           for the top panel"""
        # create the top label
        top_label = tk.Label(self.master, text="", fg=DEFAULT_TXT_COLOR,
                             bg=DEFAULT_BGG_COLOR, width="45", height="7",
                             font=HEADER_FONT)
        # position the top label
        top_label.place(x=0, y=0)

    def create_top_small_panel(self, text=""):
        """Creates a label meant to be placed on top of the top background
           where there can be inserted a small information piece of text"""
        # create the top label
        self.counter_label = tk.Label(self.master,
                                      text=text,
                                      fg=DEFAULT_TXT_COLOR, bg=DEFAULT_BGG_COLOR,
                                      width="78", height="7", font=TITLE_FONT)
        # position the top label
        self.counter_label.place(x=0, y=45)

    def create_top_panel(self, text="Synchronise the sounds"):
        """Creates a label meant to be placed on top of the top background
           where there can be inserted a short title"""
        # create the top label
        top_label = tk.Label(self.master, text=text, fg=DEFAULT_TXT_COLOR,
                             bg=DEFAULT_BGG_COLOR, width="45", height="2",
                             font=HEADER_FONT)
        # position the top label
        top_label.place(x=0, y=0)

    def create_play_button(self, text="Play"):
        """Creates a play button that triggers the toggle play button when pressed"""
        # Create play button
        self.play_button = tk.Button(self.master, text=text, fg=DEFAULT_TXT_COLOR,
                                     bg=DEFAULT_BGG_COLOR, width=D_BUTTON_WIDTH,
                                     height=D_BUTTON_HEIGHT, command=self.toggle_play)
        # Place button
        self.play_button.place(x=D_BUTTON_POSITION[0], y=D_BUTTON_POSITION[1]-PLAY_BUTTON_OFFSET)

    # SOUND CONTROL SLIDERS

    def create_amplitude_control(self):
        """Adds the necessary widgets to
           build a slider to control amplitude"""
        title_position = (20, 110)
        title_size = (15, 3)

        # create the top label
        top_label = tk.Label(self.master, text="Loudness Level\n(db)", fg=DEFAULT_TXT_COLOR,
                             width=title_size[0], height=title_size[1],
                             font=TITLE_FONT)

        # position the top label
        top_label.place(x=title_position[0], y=title_position[1])

        # slider offsets
        slider_top_offset = 50
        slider_left_offset = 16

        # calculate slider start position and size
        slider_length = 330
        slider_position = (title_position[0] + slider_left_offset,
                           title_position[1] + slider_top_offset)

        # Label values
        self.amplitude_labels = [1.6, 1.3, .9, .6, .3, 0, -.3, -.6, -.9, -1.3, -1.6]

        # Build slider
        self.amplitude_slider = tk.Scale(self.master, from_=self.amplitude_labels[0],
                                         to=self.amplitude_labels[len(self.amplitude_labels) - 1],
                                         tickinterval=self.amplitude_labels[len(self.amplitude_labels) - 1],
                                         resolution=.01, length=slider_length)
        self.amplitude_slider["command"] = (lambda amplitude=self.amplitude_slider.get():
                                            self.set_amplitude(amplitude))
        self.amplitude_slider.set(1)
        self.amplitude_slider.place(x=slider_position[0], y=slider_position[1])

    def create_phase_shift_control(self, title_position=SLIDER_TITLE_POSITION,
                                   title_size=SLIDER_TITLE_SIZE, command=None):
        """Adds the necessary widgets to
           build a slider to control phase shift"""

        # create the top label
        top_label = tk.Label(self.master, text="Time Shift (s)", fg=DEFAULT_TXT_COLOR,
                             width=title_size[0], height=title_size[1],
                             font=TITLE_FONT)
        # position the top label
        top_label.place(x=title_position[0], y=title_position[1])

        # slider offsets
        slider_top_offset = 35
        slider_left_offset = 16

        # calculate slider start position and size
        slider_length = 280
        slider_position = (title_position[0] + slider_left_offset,
                           title_position[1] + slider_top_offset)

        # Label values
        self.phase_shift_labels = [0, .3, .6, .9, 1.3, 1.6]  # , -.3, -.6, -.9, -1.3, -1.6]

        # Build slider
        self.phase_shift_slider = tk.Scale(self.master, from_=self.phase_shift_labels[0],
                                           to=self.phase_shift_labels[len(self.phase_shift_labels) - 1],
                                           tickinterval=self.phase_shift_labels[len(self.phase_shift_labels) - 1],
                                           resolution=.001, length=slider_length, orient="horizontal")

        if command is None:
            command = (lambda phase_shift=self.phase_shift_slider.get():
                       self.set_phase_shift(phase_shift))
        self.phase_shift_slider["command"] = command
        self.phase_shift_slider.set(0)
        self.phase_shift_slider.place(x=slider_position[0], y=slider_position[1])

    # GRAPHING

    def create_graph_placeholder(self):
        text = "Help:\n\n1. Use the sliders to adjust loudness,\n  and the time shift of the sounds.\n\n" \
               "2. Listen to the sounds simultaneously\n using the play button.\n\n" \
               "3. Press 'Next audio file' to confirm\n the audio is synchronised.\n\n" \
               "4. Repeat the process until you think\n all audio files are synchronised."
        label = tk.Label(self.master, text=text, fg=DEFAULT_TXT_COLOR, font=TITLE_FONT)
        label.place(x=240, y=130, width=270, height=250)

    def create_graph(self):
        """Adds the necessary widgets to show a graph
           of the current original and manipulated sounds"""

        f = Figure(figsize=(5, 5), dpi=50)
        self.ax = f.add_subplot(111)
        self.ax.set_ylabel('Amplitude [db]')
        self.ax.set_xlabel('Time [seconds]')
        self.ax.set_title('ADSR')

        x1 = self.sound_modifier.current_original_sound().get_time()
        y1 = self.sound_modifier.current_original_sound().get_data()
        self.ax.plot(x1, y1)

        x2 = self.sound_modifier.current_manipulated_sound().get_time()
        y2 = self.sound_modifier.current_manipulated_sound().get_data()
        self.ax.plot(x2, y2)

        self.canvas = FigureCanvasTkAgg(f, self.master)
        self.canvas.get_tk_widget().place(x=30, y=280, width=320, height=250)

    def plot_current_files(self):
        """Updates the current state of the graph to match
           the current original and manipulated sounds"""
        # if not self.graph_audio: return
        if self.ax is None: return
        # call the clear method on your axes
        self.ax.clear()

        # plot the new data
        self.ax.set_ylabel('Amplitude [db]')
        self.ax.set_xlabel('Time [seconds]')
        self.ax.set_title('ADSR')
        x1 = self.sound_modifier.current_original_sound().get_time()
        y1 = self.sound_modifier.current_original_sound().get_data()
        self.ax.plot(x1, y1)

        x2 = self.sound_modifier.current_manipulated_sound().get_time()
        y2 = self.sound_modifier.current_manipulated_sound().get_data()
        self.ax.plot(x2, y2)

        # call the draw method on your canvas
        self.canvas.draw()

    # SOUND MODIFIER METHODS

    def set_amplitude(self, amplitude):
        """Change the amplitude of the manipulated
           sound file and updates the current
           state of the graph"""
        self.sound_modifier.set_amplitude(amplitude)
        self.plot_current_files()

    def set_phase_shift(self, phase_shift):
        """Change the phase shift of the manipulated
           sound file and updates the current
           state of the graph"""
        self.sound_modifier.set_phase_shift(phase_shift)
        self.plot_current_files()

    def toggle_play(self):
        """Plays the current original
           and manipulated sound"""
        self.sound_modifier.toggle_play()
        if self.arduino_interface is None:
            if not self.sound_modifier.get_should_play():
                self.play_button.config(text="Play", bg=DEFAULT_BTN_BGG, fg=DEFAULT_TXT_COLOR)
            else:
                self.play_button.config(text="Stop", bg=ACTIVE_BTN_BGG, fg=DEFAULT_BGG_COLOR)

    def next_audio_files(self):
        """Setup the next sound files until it
           has reached one cycle, where it will
           save the results and display the
           goodbye page"""
        self.sound_modifier.next_audio_files()
        if self.arduino_interface is None:
            self.play_button.config(text="Play", bg=DEFAULT_BTN_BGG, fg=DEFAULT_TXT_COLOR)
        if self.sound_modifier.get_finished_sequence() > 0:
            self.create_goodbye_widgets()
        else:
            self.plot_current_files()
            self.counter_label.config(text=f"Sound {self.sound_modifier.get_current_sound_index() + 1} out "
                                           f"of {self.sound_modifier.get_number_of_sounds()}")

    def set_slider_value(self, val):
        if self.phase_shift_slider is None or \
                self.current_page != "ONE" and \
                self.current_page != "TWO" and \
                self.current_page != "SOUNDCONTROL":
            return
        self.phase_shift_slider.set(value=val)

    def confirm(self):
        if self.current_page == "WELCOME":
            self.create_demo_step_one()
        elif self.current_page == "ONE":
            self.create_demo_step_two()
        elif self.current_page == "TWO":
            self.create_demo_step_three()
        elif self.current_page == "THREE":
            self.create_demo_step_four()
        elif self.current_page == "FOUR":
            self.create_sound_control_widgets()
        elif self.current_page == "SOUNDCONTROL":
            self.next_audio_files()
        elif self.current_page == "GOODBYE":
            pass

    # SOUND MODIFIER DEMO METHODS

    def demo_phase_shift(self, phase_shift=None):
        """Execute a callback related to the interactive demo when
           the two current audio files has the same phase shift"""
        if self.callback_activated or \
            self.phase_shift_slider is None: return

        """offset = .2"""
        if phase_shift is None:
            phase_shift = self.phase_shift_slider.get()
        self.set_phase_shift(phase_shift)
        """
        is_within_greater = (self.sound_modifier.current_original_sound().get_phase_shift()-offset <=
                      self.sound_modifier.current_manipulated_sound().get_phase_shift())
        is_within_less = (self.sound_modifier.current_original_sound().get_phase_shift()+offset >=
                      self.sound_modifier.current_manipulated_sound().get_phase_shift())

        if is_within_greater and is_within_less:
            self.callback_activated = True
            if self.next_callback == "ONE": self.create_demo_step_two_callback()
            elif self.next_callback == "TWO": self.create_demo_step_three_callback()
        """
