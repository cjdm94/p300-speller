from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import model_selection
import time
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import os

class Classifier():
    def __init__(self,
                 start_time,    # start time in seconds
                 num_trials=3,
                 num_rows=6,
                 num_columns=6,
                 flash=0.2,
                 inter_flash=0.1,
                 inter_trial=1,
                 inter_mega_trial=3,
                 target_char_flashes=200,
                ):
        self.column_order = [5, 3, 2, 0, 4, 1, 3, 2, 0, 1, 5, 4, 3, 4, 0, 5, 2, 1]
        self.row_order =    [1, 4, 2, 5, 0, 3, 3, 2, 5, 0, 1, 4, 4, 0, 2, 3, 1, 5]
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.lda = LinearDiscriminantAnalysis()
        self.fs = 128
        self.data = []
        self.stimulus_time = int((inter_flash + flash) * self.fs)  # 38
        self.trial_length = self.stimulus_time * (num_rows + num_columns) # 456
        self.samples_in_data = num_trials * self.trial_length # 1368
        self.num_samples = 0
        self.start_time = start_time
        self.inter_trial = inter_trial
        self.inter_mega_trial = inter_mega_trial
        self.counter = 0
        self.window_length = int(0.6 * self.fs)        
        self.target_char_row = 1
        self.target_char_col = 0
        
        # e.g. (75 * (6+6)) + (1 * 250)
        # this takes into account the row-col interval of 1s
        # that occurs between trial 1 and trial 2, and trial 2 and trial 3.
        # in each mega trial, the target row and target col is flashed 3 times each
        # so the target char is flashed 6 times
        samples_in_trial = self.trial_length + (self.inter_trial * self.fs) # 456 + 128 = 584
        samples_in_mega_trial = samples_in_trial * num_trials # 1752
        char_flashes_per_mega_trial = 2 * num_trials # 6
        target_mega_trials = int(target_char_flashes / char_flashes_per_mega_trial) # 200/6 = 33
        self.sample_limit = target_mega_trials * samples_in_mega_trial # 33 * 1752 = 57816
        self.stim_samples = int((inter_flash + flash) * self.fs)
        self.subtrial_intvl_samples = int(self.inter_trial * self.fs)
        self.trial_intvl_samples = int(self.inter_mega_trial * self.fs)
        self.training_data_path = "./data/training_data.txt"
        self.target_stims_path = "./data/target_stims.txt"
        self.non_target_stims_path = "./data/non_target_stims.txt"
        self.delim = ","
        
    def add_sample(self, sample):
        if time.time() <= self.start_time or self.num_samples > 15360: 
            return ""

        self.data.append(sample[0])
        self.num_samples += 1
        
        if self.num_samples % 1000 == 0:
            print("NUM SAMPLES:", self.num_samples)

        if self.num_samples == 15360:
            print("Sample limit reached:", time.time() - self.start_time)  
            all_stims = self.determine_stims(
                self.sample_limit, 
                self.stim_samples, 
                self.subtrial_intvl_samples, 
                self.trial_intvl_samples
            )
            stims = self.split_stims(all_stims)
            self.write_data_to_file(self.data, self.training_data_path)
            self.write_data_to_file(stims['targets'], self.target_stims_path)
            self.write_data_to_file(stims['non_targets'], self.non_target_stims_path)
            self.classify_training_data()
            os.system('say "training data classified!"')
        return ""

    def classify_training_data(self):
        data = np.loadtxt(self.training_data_path, delimiter=self.delim)
        data = self._filter(data, 0.16)
        target_stims = np.loadtxt(self.target_stims_path, dtype=np.uint)
        non_target_stims = np.loadtxt(self.non_target_stims_path, dtype=np.uint)
        target_epochs = self.epoch_data(data, target_stims)
        non_target_epochs = self.epoch_data(data, non_target_stims)
        X = np.vstack((target_epochs, non_target_epochs))
        Y = []
        Y += ([1] * len(target_epochs))
        Y += ([0] * len(non_target_epochs))

        validation_size = 0.20
        seed = 7
        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(self.lda, X_train, Y_train, cv=kfold, scoring='accuracy')
        print("Cross validation results:", cv_results)

        plt.figure()
        plt.plot(data[:257])
        plt.figure()
        x = np.arange(600, step=600/self.window_length)
        plt.plot(x, np.mean(target_epochs, axis=0)[:], label="Target stimulus")
        plt.plot(x, np.mean(non_target_epochs, axis=0)[:], label="Nontarget stimulus")
        plt.title('Averaged response to flashing stimuli')
        plt.xlabel('Time (ms)')
        plt.ylabel('Response (microvolts)')
        plt.legend()

        self.lda.fit(X_train, Y_train)
        print("Classifier mean accuracy:", self.lda.score(X_validation, Y_validation))
        y = self.lda.predict_proba(X_train)
        print("Classifier probability:", y)
    
    def epoch_data(self, arr, stims):
        new_arr = []
        for i in stims:
            window_end = int(i+self.window_length)
            if window_end > len(arr):
                break 
            new_arr.append(arr[i:window_end])
        n = np.array(new_arr)
        return n
    
    def split_stims(self, stims):
        targets = []
        non_targets = []
        stimIndex = 0
        mega_trial_flashes = len(self.row_order) + len(self.column_order)
        # in a mega trial, 35 flashes of row/col; 
        # these are indexes of flash of row/col containing target char (a)
        target_flashes = [0,9,16,20,28,32] 
        non_target_flashes = [1,2,3,4,5,6,7,8,10,11,12,13,14,15,17,18,19,21,22,23,24,25,26,27,29,30,31,33,34,35]
        while stimIndex <= len(stims):
            # target_flash_indexes = mega_trial_target_flash_indexes
            # end_index = stimIndex+mega_trial_flashes
            if stimIndex+mega_trial_flashes > len(stims) - 1:
                return { 'targets': targets, 'non_targets': non_targets }
                # cut_off = 35 - (end_index - len(stims) - 1)
                # target_flash_indexes = [x for x in target_flash_indexes if x < cut_off]
                # do the same for the non_target_flashes^
                # end_index = len(stims) - 1
                # print("END_INDEX:", end_index)

            mega_trial_stims = np.array(stims)[stimIndex:stimIndex+mega_trial_flashes]
            mega_trial_targets = mega_trial_stims[target_flashes]
            mega_trial_non_targets = mega_trial_stims[non_target_flashes]
            targets = targets + list(mega_trial_targets)
            non_targets = non_targets + list(mega_trial_non_targets)
            stimIndex += mega_trial_flashes
        return { 'targets': targets, 'non_targets': non_targets }

    def write_data_to_file(self, data, filename):
        with open(filename, "w+") as txt_file:
            for v in data:
                txt_file.write(str(v) + "\n")

    def _filter(self, data, cutoff, order=1):
        nyq = 0.5 * self.fs
        normal_cutoff = cutoff / nyq
        b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
        y = signal.filtfilt(b, a, data)
        return y

    @staticmethod
    def determine_stims(sample_limit, 
                        stim_samples, 
                        subtrial_intvl_samples, 
                        trial_intvl_samples
                        ):
        stims = []
        sampleIndex = 0
        stimEvents = 0
        trials = 0
        while sampleIndex <= sample_limit:
            stimEvents += 1
            stims.append(sampleIndex)
            sampleIndexIncrement = stim_samples
            if stimEvents % 12 == 0:
                sampleIndexIncrement = subtrial_intvl_samples
                trials += 1
                if trials == 3:
                    sampleIndexIncrement = trial_intvl_samples
                    trials = 0
            sampleIndex += sampleIndexIncrement
            
        return stims