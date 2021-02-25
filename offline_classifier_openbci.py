#%%
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import mne
%matplotlib qt
#%%

def notch_mains_interference(data):
    notch_freq_Hz = np.array([60.0])  # main + harmonic frequencies
    for freq_Hz in np.nditer(notch_freq_Hz):  # loop over each target freq
        bp_stop_Hz = freq_Hz + 3.0*np.array([-1, 1])  # set the stop band
        b, a = signal.butter(3, bp_stop_Hz/(250 / 2.0), 'bandstop')
        data = signal.lfilter(b, a, data, axis=0)
        print("Notch filter removing: " + str(bp_stop_Hz[0]) + "-" + str(bp_stop_Hz[1]) + " Hz")
    return data

# Applies notch filter to get rid of main interference, then applies
# bandpass filter to get rid of eeg artefacts e.g. eye blinks?
def filter_(arr, lowcut, highcut, order):
   arr = notch_mains_interference(arr)
   nyq = 0.5 * 250
   b, a = signal.butter(1, [lowcut/nyq, highcut/nyq], btype='band')
   for i in range(0, order):
       arr = signal.lfilter(b, a, arr, axis=0)
   return arr
       
def epoch_data(arr, stims, window_length):
    new_arr = []
    for i in stims:
        window = arr[i:int(i+window_length)].T
        window = np.mean(window, axis=0)
        if np.max(np.abs(window)) < 300:
            new_arr.append(window)
    n = np.array(new_arr)
    print("Epochs shape:", n.shape)
    return n

#%%
plot_flag = 1
data = np.loadtxt('./data/raw_training.txt',
                      delimiter=',').T
stims = np.loadtxt('./data/target.txt', dtype=np.uint)
nstims = np.loadtxt('./data/nontarget.txt', dtype=np.uint)
#%%

#%%
fs = 250
ds_factor = 10 # downsampling factor
s1 = filter_(data.T, 0.4, 20,1) #filter data

# Plot filtered data
plt.figure()
for ch in s1.T:
    plt.plot(ch)
#%%
#%%
# Epoch and downsample
t_ep1 = epoch_data(s1, stims, int(0.6*fs))
print("TARGET EPOCHS:", len(t_ep1))
t_ep = t_ep1[:, ::ds_factor]
n_ep1 = epoch_data(s1, nstims, int(0.6*fs))
print("NON-TARGET EPOCHS:", len(n_ep1))
n_ep = n_ep1[:, ::ds_factor]
#%%

#%%
# Prepare inputs for classifier
t_ep = np.hstack((t_ep, np.ones([t_ep.shape[0],1])))
n_ep = np.hstack((n_ep, np.zeros([n_ep.shape[0],1])))
print("NON-TARGET EPOCHS:", len(n_ep))
X = np.vstack((t_ep, n_ep))[:,:-1]
Y = np.vstack((t_ep, n_ep))[:,-1]
#%%

#%%
# Classification
validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
kfold = model_selection.KFold(n_splits=10, random_state=seed)
clf = LinearDiscriminantAnalysis()
cv_results = model_selection.cross_val_score(clf, X_train, Y_train, cv=kfold, scoring='accuracy')
print("Cross validation results:", cv_results)
#%%

#%%   
if plot_flag:
    plt.figure()
    for ep in n_ep1[:20]:
        plt.plot(ep)
    
    plt.figure()
    x = np.arange(600, step=4)
    plt.plot(x, np.mean(t_ep1, axis=0)[:], label="Target stimulus")
    plt.plot(x, np.mean(n_ep1, axis=0)[:], label="Nontarget stimulus")
    plt.title('Averaged response to flashing stimuli')
    plt.xlabel('Time (ms)')
    plt.ylabel('Response (microvolts)')
    plt.legend()
#%%


#%%
# Fit training data - target epochs and non-target epochs - to classifier
clf.fit(X_train, Y_train)
print("Classifier score:", clf.score(X_validation, Y_validation))
# Get probability that the training target data is target
y = clf.predict_proba(X_train)
#%%``