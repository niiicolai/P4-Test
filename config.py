# THE WAVE GRAPH DISPLAY CAN BE
# ACTIVATED FOR DEBUGGING PURPOSE
GRAPH_AUDIO = True

# SHOULD BE TRUE BEFORE THE
# APPLICATION TRIES TO READ
# FROM AN ARDUINO THROUGH SERIAL
ARDUINO_INTERFACE = False

# Path to sound files
FILE_PATH = "assets/sound/"

# Name of original files
ORIGINAL_NAMES = [
    f"{FILE_PATH}High_Hat.wav",
    f"{FILE_PATH}Kick_Drum.wav",
    f"{FILE_PATH}Arco_Bass.wav",
    f"{FILE_PATH}Dark_Piano.wav",
    f"{FILE_PATH}Snare_Drum.wav"
]

# Name of manipulated files
MANIPULATED_NAMES = [
    f"{FILE_PATH}High_Hat_Reverb.wav",
    f"{FILE_PATH}Reverb_Kick_Drum.wav",
    f"{FILE_PATH}Reverb_Arco_Bass.wav",
    f"{FILE_PATH}Reverb_Dark_Piano.wav",
    f"{FILE_PATH}Reverb_Snare_Drum.wav"
]
