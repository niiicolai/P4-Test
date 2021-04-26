import unittest
import random
import csv
from csvWriter import CSVWriter, ORIGINAL_KEY, \
    MANIPULATED_KEY, AMPLITUDE_KEY, PHASE_SHIFT_KEY


# TEST DATA
# The path to the result CSV file
CSV_FILE = "./assets/csv/result.csv"

# Create some randomized test data
a, b = -2, 2
data = [
    {ORIGINAL_KEY: {AMPLITUDE_KEY: random.randint(a, b), PHASE_SHIFT_KEY: -random.randint(a, b)},
    MANIPULATED_KEY: {AMPLITUDE_KEY: random.randint(a, b), PHASE_SHIFT_KEY: random.randint(a, b)}},
    {ORIGINAL_KEY: {AMPLITUDE_KEY: random.randint(a, b), PHASE_SHIFT_KEY: -random.randint(a, b)},
    MANIPULATED_KEY: {AMPLITUDE_KEY: random.randint(a, b), PHASE_SHIFT_KEY: random.randint(a, b)}},
]

# Create a csv writer object used for the tests
WRITER = CSVWriter(data)


class TestCSVWriter(unittest.TestCase):
    """Used to test the class CSVWriter in cswWriter.py"""

    def test_save(self):
        """Ensure the result CSV file contains
           the correct values after saving"""
        WRITER.save()
        with open(CSV_FILE) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            i = 0
            for row in csv_reader:
                if i == 0: continue
                self.assertEqual(row[0], data[i][ORIGINAL_KEY][AMPLITUDE_KEY], "Should be equal")
                self.assertEqual(row[1], data[i][ORIGINAL_KEY][PHASE_SHIFT_KEY], "Should be equal")
                self.assertEqual(row[2], data[i][MANIPULATED_KEY][AMPLITUDE_KEY], "Should be equal")
                self.assertEqual(row[3], data[i][MANIPULATED_KEY][PHASE_SHIFT_KEY], "Should be equal")
                i += 1

    """
       OTHER METHODS:
       None
    """


if __name__ == '__main__':
    unittest.main()
