from matplotlib import pyplot as plt
import numpy as np
import scipy.signal

shotPixels = np.zeros((500, 500)) # μm

shotPixels[250][200:300:3] = 1

eta = 0.5
sigma_B = 6 # μm

P_B = lambda rsquared : (eta/(sigma_B**2)) * np.exp(-rsquared/(sigma_B**2))

scatterDistr = np.zeros((500, 500))
for x in range(len(scatterDistr)):
    for y in range(len(scatterDistr)):
        scatterDistr[x][y] += P_B((x-50)**2 + (y-50)**2)

##plt.matshow(scatterDistr)
##plt.show()


##for doseCount in range(1):
print("Convolution:")
dosePixels = scipy.signal.convolve2d(shotPixels, scatterDistr, mode = "same", boundary = "fill", fillvalue = "0")
##    dosePixels[0][0] = 1
##    dosePixels[-1][-1] = 0
plt.matshow(dosePixels)
plt.show()
