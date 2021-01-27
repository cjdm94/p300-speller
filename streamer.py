import threading

# Emotiv Insight data sample schema: 
# [
#   "COUNTER",
#   "INTERPOLATED",
#   "AF3","T7","Pz","T8","AF4",
#   "RAW_CQ",
#   "MARKER_HARDWARE",
#   "MARKERS"
# ]
# e.g. "eeg":[93,0,4146.667,4485.641,4166.154,4222.051,4132.308,450.0,0,[]]

class Streamer(threading.Thread):
    def __init__(self, cortex, classifier, emit):
        super(Streamer, self).__init__()
        self.cortex = cortex
        self.classifier = classifier
        self.emit = emit

        self.cortex.do_prepare_steps()
        self.cortex.sub_request('eeg')
    def run(self):
        while True:
            sample = self.cortex.stream_eeg()
            if sample != "":
                prediction = self.classifier.add_sample(sample[2:7])
                if prediction != "":
                    print("PREDICTION:", prediction)
                    self.emit('prediction', prediction)