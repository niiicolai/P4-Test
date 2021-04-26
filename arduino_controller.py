import threading
import serial
import re

POTENTIO_KEY = 'potentioValue='
BUTTON_KEY = 'buttonValue='

REGULAR_EXP = re.compile(r'\w+=\d+')
REGULAR_POT = re.compile(POTENTIO_KEY)
REGULAR_BTN = re.compile(BUTTON_KEY)

range = 1.6
MIN_POTENTIO_VALUE = 0
MAX_POTENTIO_VALUE = 1024

PORT = 'COM3'
BAUD_RATE = 9600
TIMEOUT = .1

DECODE = 'utf-8'


class Arduino:
    def __init__(self, gui):
        self.ser = serial.Serial(port=PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
        self.gui = gui
        self.force_stop = False
        self.last_potentio_value = 0
        self.last_button_value = 0

    def stop(self):
        self.force_stop = True

    def listen_async(self):
        thread = threading.Thread(target=self.listen, args=())
        thread.start()

    def listen(self):
        should_run = True
        while should_run:

            if self.force_stop or not self.ser.isOpen():
                should_run = False
                continue

            msg = self.ser.readline()
            decoded_bytes = msg.decode(DECODE)
            match = REGULAR_EXP.match(decoded_bytes)

            if match and REGULAR_POT.match(decoded_bytes):

                potentio_value = int(re.sub(POTENTIO_KEY, "", match.group()))

                normalized_value = abs(range * (potentio_value - MIN_POTENTIO_VALUE) /
                                       (MAX_POTENTIO_VALUE - MIN_POTENTIO_VALUE) - range)
                normalized_value = round(normalized_value, 2)
                if normalized_value != self.last_potentio_value:
                    self.gui.set_slider_value(normalized_value)
                    self.last_potentio_value = normalized_value

            elif match and REGULAR_BTN.match(decoded_bytes):

                button_value = int(re.sub(BUTTON_KEY, "", match.group()))
                if button_value != self.last_button_value:
                    self.gui.confirm()
                    self.last_button_value = button_value


"""
ARDUINO CODE EXAMPLE

int POTENTIOMETER_PIN = A0;
int lastPotentioValue = 0;

int BUTTON_PIN = 4;
int lastButtonValue = LOW;

void setup() {
  // Init button
  pinMode(BUTTON_PIN, INPUT);

  // Init the serial monitor
  Serial.begin(9600);

  // Wait until serial monitor is started
  while (!Serial) {};

}

void loop() {

  // Get, detect potentiometer state changes
  // and print result to serial connections
  int currentPotentioValue = analogRead(POTENTIOMETER_PIN);
  //if (currentPotentioValue != lastPotentioValue) {
    // Print message
    Serial.print("potentioValue=");
    Serial.print(currentPotentioValue);
    Serial.print("\n");
    // Update state
    lastPotentioValue = currentPotentioValue;
  //}

  // Get, detect button state changes
  // and print result to serial connections
  int currentButtonValue = digitalRead(BUTTON_PIN);
  //if (currentButtonValue != lastButtonValue) {
    // Print message
    Serial.print("buttonValue=");
    Serial.print(currentButtonValue);
    Serial.print("\n");
    // Update state
    lastButtonValue = currentButtonValue;
  //}
}
"""