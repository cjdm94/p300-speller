import unittest
from training_classifier import Classifier
import time

class TestClassifier(unittest.TestCase):
    
    def test_split_stims(self):
        self.maxDiff = None
        
        stims = []
        for i in range(200):
            stims.append(i)
        
        clf = Classifier(time.time())
        actual = clf.split_stims(stims)

        # self.column_order = [5, 3, 2, 0, 4, 1, 3, 2, 0, 1, 5, 4, 3, 4, 0, 5, 2, 1]
        # self.row_order =    [1, 4, 2, 5, 0, 3, 3, 2, 5, 0, 1, 4, 4, 0, 2, 3, 1, 5]
        # target char a flash indexes = [0,9,16,20,28,32]
        # [
        #     {r1}, r4, r2, r5, r0, r3, 
        #     c5, c3, c2, {c0}, c4, c1, 
        #     r3, r2, r5, r0, {r1}, r4,
        #     c3, c2, {c0}, c1, c5, c4,
        #     r4, r0, r2, r3, {r1}, r5,
        #     c3, c4, {c0}, c5, c2, c1
        # ]
        expected_targets = [
            0,9,16,20,28,32,
            36,45,52,56,64,68,
            72,81,88,92,100,104,
            108,117,124,128,136,140,
            144,153,160,164,172,176,
        ]
        expected_non_targets = [
            1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17,
            18, 19, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 33,
            34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48,
            49, 50, 51, 53, 54, 55, 57, 58, 59, 60, 61, 62, 63, 
            65, 66, 67, 69, 70, 71, 73, 74, 75, 76, 77, 78, 79, 
            80, 82, 83, 84, 85, 86, 87, 89, 90, 91, 93, 94, 95,
            96, 97, 98, 99, 101, 102, 103, 105, 106, 107, 109, 
            110, 111, 112, 113, 114, 115, 116, 118, 119, 120, 
            121, 122, 123, 125, 126, 127, 129, 130, 131, 132, 
            133, 134, 135, 137, 138, 139, 141, 142, 143, 145, 
            146, 147, 148, 149, 150, 151, 152, 154, 155, 156, 
            157, 158, 159, 161, 162, 163, 165, 166, 167, 168, 
            169, 170, 171, 173, 174, 175, 177, 178, 179
        ]
        self.assertEqual(actual['targets'], expected_targets)
        self.assertEqual(actual['non_targets'], expected_non_targets)
        self.assertEqual(list(set().intersection(actual['targets'], actual['non_targets'])), [])

    def test_write_data_to_file(self):
        self.maxDiff = None
        clf = Classifier(time.time())
        data = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
        filename = "test.txt"
        clf.write_data_to_file(data, filename)
    
    def test_determine_stims(self):
        self.maxDiff = None
        clf = Classifier(time.time())
        actual = clf.determine_stims(
            sample_limit=1000, 
            stim_samples=10, 
            subtrial_intvl_samples=5, 
            trial_intvl_samples=15)

        # Each element in the array is the flash onset of a distinct row or col.
        # Onset is denoted by the sample index, not a timestamp.
        # E.g. 0 means the very first sample received. 10 is the 10th sample received.
        # Each trial is made up of 3 sub trials:
        # Sub-trial 1: 6 rows flashed, then 6 cols, then a sub-trial interval (5 samples)
        # Sub-trial 2: 6 rows flashed, then 6 cols, then a sub-trial interval (5 samples)
        # Sub-trial 3: 6 rows flashed, then 6 cols, then a trial interval     (15 samples)
        # repeat
        expected = [
            # r1, r2, r3, r4, r5, r6, c1, c2, c3, c4, c5, c6
            0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110,            # +5 samples
            115, 125, 135, 145, 155, 165, 175, 185, 195, 205, 215, 225, # +5 samples
            230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, # +15 samples
            355, 365, 375, 385, 395, 405, 415, 425, 435, 445, 455, 465, # +5 samples
            470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, # +5 samples
            585, 595, 605, 615, 625, 635, 645, 655, 665, 675, 685, 695, # +15 samples
            710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, # +5 samples
            825, 835, 845, 855, 865, 875, 885, 895, 905, 915, 925, 935, # +5 samples
            940, 950, 960, 970, 980, 990, 1000
        ]

        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()