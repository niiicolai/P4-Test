# Dependencies
from csv import DictWriter

"""
    The 4 steps below provide the general usage of this class

    1. import class
    from csvWriter import CSVWriter

    2. Create some test data
    data = [{
        "original":{"amplitude":1, "phase_shift":0},
        "manipulated":{"amplitude":1, "phase_shift":0}
    }]

    3. Create a CSVWriter object using the data
    writer = CSVWriter(data)

    4. Write the data to a CSV file specified at the path above
    writer.save()
"""

# CSV file path
FILE_PATH = 'assets/csv/result.csv'

# CSV Field names
FIELD_NAMES = [
    'original amplitude',
    'original phase shift',
    'manipulated amplitude',
    'manipulated phase shift',
    'amplitude difference',
    'phase shift difference']

# DATA Keys
ORIGINAL_KEY = "original"
MANIPULATED_KEY = "manipulated"
AMPLITUDE_KEY = "amplitude"
PHASE_SHIFT_KEY = "phase_shift"


class CSVWriter:
    """A class used to write the state
       of the sound files to a CSV file, after being
       manipulated through the sound control system"""

    def __init__(self, data):
        """The class constructor."""
        self.__data = data

    def save(self):
        """Writes the provided data to a CSV file"""
        with open(FILE_PATH, 'w', newline='') as csv_file:
            writer = DictWriter(csv_file, fieldnames=FIELD_NAMES)
            writer.writeheader()

            # format and calculate results
            for v in self.__data:
                # Calculate differences
                amplitude_diff = abs(v[ORIGINAL_KEY][AMPLITUDE_KEY] - v[MANIPULATED_KEY][AMPLITUDE_KEY])
                phase_shift_diff = abs(v[ORIGINAL_KEY][PHASE_SHIFT_KEY] - v[MANIPULATED_KEY][PHASE_SHIFT_KEY])

                # Format row
                res = {
                    FIELD_NAMES[0]: v[ORIGINAL_KEY][AMPLITUDE_KEY],
                    FIELD_NAMES[1]: v[ORIGINAL_KEY][PHASE_SHIFT_KEY],
                    FIELD_NAMES[2]: v[MANIPULATED_KEY][AMPLITUDE_KEY],
                    FIELD_NAMES[3]: v[MANIPULATED_KEY][PHASE_SHIFT_KEY],
                    FIELD_NAMES[4]: amplitude_diff,
                    FIELD_NAMES[5]: phase_shift_diff
                }

                # Write results to the csv file
                writer.writerow(res)
