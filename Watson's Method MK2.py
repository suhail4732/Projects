from matplotlib import pyplot as plt
import numpy as np
import scipy.signal

size = 100

shotPixels = np.zeros((size, size)) # * 50nm



eta = 0.5
sigma_B = 120 # * 50nm
sigma_A = 15   # * 50nm

baseDosePower = 50

shotPixels[int(  size/4)][int(size/8) : int(7*size/8) : int(size/20)] = baseDosePower
shotPixels[int(3*size/4)][int(size/8) : int(7*size/8) : int(size/20)] = baseDosePower
for x in range(int(size/4), int(3*size/4), int(size/20)):
    shotPixels[int(x)][int(  size/8)] = baseDosePower

plt.matshow(shotPixels)
plt.show()

P_B = lambda rsquared : (eta/(sigma_B**2)) * np.exp(-rsquared/(sigma_B**2))
P_A = lambda rsquared : (1  /(sigma_A**2)) * np.exp(-rsquared/(sigma_A**2))

scatterDistr = np.zeros((size, size))
for x in range(size):
    for y in range(size):
        scatterDistr[x][y] += (P_B(dist := (x-size/2)**2 + (y-size/2)**2) + P_A(dist))

plt.matshow(scatterDistr)
plt.show()

##plt.matshow(scatterDistr)
##plt.show()


##for doseCount in range(1):
print("Convolution:")
dosePixels = scipy.signal.convolve2d(shotPixels, scatterDistr, mode = "same", boundary = "fill", fillvalue = "0")
print("done")
##    dosePixels[0][0] = 1
##    dosePixels[-1][-1] = 0

##plt.figure()
##ax = fig.add_subplot(111)
plt.matshow(dosePixels)
plt.colorbar()

plt.show()

samplePixels = np.where(dosePixels > 1, 1, 0)
plt.matshow(samplePixels)
plt.show()
