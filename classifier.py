from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import model_selection
import time
from scipy import signal
import numpy as np
import sys

class Classifier():
    def __init__(self,
                 start_time,    #start time in seconds
                 channels = [0,1,2],
                 num_trials=3,
                 num_rows=6,
                 num_columns=6,
                 flash=0.2,
                 inter_flash=0.1,
                 inter_mega_trial=3):
        self.column_order = [5, 3, 2, 0, 4, 1, 3, 2, 0, 1, 5, 4, 3, 4, 0, 5, 2, 1]
        self.row_order = [1, 4, 2, 5, 0, 3, 3, 2, 5, 0, 1, 4, 4, 0, 2, 3, 1, 5]
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.lda = LinearDiscriminantAnalysis()
        self.fs = 128
        self.started = False
        self.collecting = False
        self.buffer = []
        self.data = []
        # (0.1 + 0.2) * 128 = 38
        self.stimulus_time = int((inter_flash + flash) * self.fs)
        # 38.4 * (6 + 6) = 456
        self.trial_length = self.stimulus_time * (num_rows + num_columns)
        # 3 * 456 = 1368 samples covering the time window during which three flashing trials are run
        # (each row and column is flashed three times)
        self.samples_in_data = num_trials * self.trial_length
        
        self.samples_since_last = 0
        self.num_samples = 0
        self.channels = channels
        self.start_time = start_time
        self.inter_mega_trial = inter_mega_trial
        self.counter = 0

        # This is the number of samples during 600ms - using 600ms windows
        self.window_length = int(0.6 * self.fs)
        
        self.lowcut = 0.5
        self.highcut = 20
        self.ds_factor = 3 #TODO is downsample needed, Emotiv downsamples already 
        
        self.train()
    def train(self):
        data = np.loadtxt('data/training_data.txt',
                      delimiter=',')
        target_stims = np.loadtxt('data/target_stims.txt', dtype=np.uint)
        non_target_stims = np.loadtxt('data/non_target_stims.txt', dtype=np.uint)
        data = self._filter(data, 0.16)
        target_epochs = self.epoch_data_by_stims(data, target_stims)
        non_target_epochs = self.epoch_data_by_stims(data, non_target_stims)
        X = np.vstack((target_epochs, non_target_epochs))
        Y = []
        Y += ([1] * len(target_epochs))
        Y += ([0] * len(non_target_epochs))
        self.lda.fit(X,Y)
        print("TRAINING COMPLETE")
        
    def add_sample(self, sample):
        message = ''
        self.counter += 1
        
        if self.collecting:
            self.data.append(sample[0])
            self.num_samples += 1
            if self.num_samples == self.samples_in_data:
                print(self.num_samples, " samples collected; running prediction...")
                message = self.run_prediction()
                self.reset()
        else:
            self.buffer.append(sample[0])
            self.samples_since_last += 1
            if self.started:
                # 3 * 128 = 384 samples between trials, ignore
                if self.samples_since_last == self.inter_mega_trial * self.fs:
                    self.collecting = True
            else: 
                if time.time() > self.start_time:
                    self.started = True
                    self.collecting = True
                else:
                    print("Classifier: sample received before start time; ignoring.")
        return message
    def reset(self):
        self.buffer = self.data[-self.fs*5:]
        self.data = []
        self.samples_since_last = 0
        self.num_samples = 0
        self.collecting = False
        
    def run_prediction(self):
        all_data = self.buffer + self.data
        filtered_data = self._filter(all_data, 0.16)
        data = filtered_data[len(self.buffer):]
        epochs = self.epoch_data(data)
       
        lens = []
        for e in epochs:
            lens.append(len(e))
        print("EPOCHS LENS:", lens)
        print("EPOCH 1:", epochs[0])
        print("EPOCH N", epochs[-1])

        rows = self.extract(epochs, row=True)
        columns = self.extract(epochs, row=False)
        row_probs = np.array([np.mean(self.lda.predict_proba(row), axis=0) for row in rows])
        pred_row = np.argmax(row_probs[:, 1])
        col_probs = np.array([np.mean(self.lda.predict_proba(column), axis=0) for column in columns])
        pred_col = np.argmax(col_probs[:, 1])
        message = str(pred_row) + str(pred_col)
        print("PROBABILITIES ROWS:\n", row_probs)
        print("PROBABILITIES COLS:\n", col_probs)
        return message

    def _filter(self, data, cutoff, order=1):
        nyq = 0.5 * self.fs
        normal_cutoff = cutoff / nyq
        b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
        y = signal.filtfilt(b, a, data)
        return y
       
    def epoch_data(self, arr):
        new_arr = []
        i = 0 
        n = 0
        while i <= len(arr) - self.window_length:
            window_end = int(i+self.window_length)
            new_arr.append(arr[i:window_end])
            i += self.stimulus_time
            n += 1
        if (i < len(arr)):
            window = arr[i:]
            zero_pad = np.zeros(self.window_length - len(window))
            window = np.concatenate((window, zero_pad))
            new_arr.append(window)
        n = np.array(new_arr)
        return n

    def epoch_data_by_stims(self, arr, stims):
        new_arr = []
        for i in stims:
            window_end = int(i+self.window_length)
            new_arr.append(arr[i:window_end])
        n = np.array(new_arr)
        return n

    def extract(self, arr, row=True):
        if row:
            order = self.row_order
            num_ = self.num_rows
            arr = arr[[0,1,2,3,4,5,12,13,14,15,16,17,24,25,26,27,28,29]]
        else: 
            order = self.column_order
            num_ = self.num_columns
            arr = arr[[6,7,8,9,10,11,18,19,20,21,22,23,30,31,32,33,34,35]]
        new_arr = [[] for i in range (0, num_)]
        for i, elem in enumerate(order):
            new_arr[elem].append([arr[i]])
        return np.squeeze(np.array(new_arr))