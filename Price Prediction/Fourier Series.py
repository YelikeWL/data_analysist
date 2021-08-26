import math
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as p
    
def fourierExtrapolation(train, test):
    big_n = 100                     # the number of harmonics (N) - best approximation by testing
    t = np.arange(len(train))
    p = np.polyfit(t, train, 1)                 # find linear trend in x by least square
    train_detrend = train - int(p[0]) * t       # detrended x
    train_freq = np.fft.fft(train_detrend)      # detrended x in frequency domain
    f = np.fft.fftfreq(len(train))              # the frequencies 
    indexes = list(range(len(train)))
    # sort indexes by frequency, lower -> higher
    indexes.sort(key = lambda i: np.absolute(f[i]))
 
    t = np.arange(0, len(test))
    predicted_val = np.zeros(len(t))
    for i in indexes[:big_n]:
        ampli = np.absolute(train_freq[i]) / len(train)     # amplitude
        phase = np.angle(train_freq[i])                     # phase
        predicted_val += ampli * np.cos(2 * math.pi * f[i] * t + phase) #the fourier in phasor form
    return (predicted_val + p[0] * t)

#To open the file and returns a list of its lines
def read(filename):     #filename as string
    with open(filename, 'r') as reader:
        return reader.readlines()

def load(data, data_list):          #Load data into a list
    for i in data:
        i = float(i[:len(i)-1])     #remove the \n and transform str to float
        data_list.append(i)         #add to new list

#Extract data from the txt 
training_data = read(r'Part1_training_data.txt')
train = list()
load(training_data, train)
testing_data = read(r'Part1_testing_data.txt')
test = list()
load(testing_data, test)

four_predictions = fourierExtrapolation(train, test)
rmse_four = math.sqrt(mean_squared_error(test, four_predictions))        #find the root mean square
print('Test RMSE: %.3f' % (rmse_four/2))

p.plot(test, color='blue') 
p.plot(four_predictions, color='red')
p.show()