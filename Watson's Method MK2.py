from matplotlib import pyplot as plt
import numpy as np
import scipy.signal

size = 100

shotPixels = np.zeros((size, size)) # * 50nm



eta = 0.5
sigma_B = 15 # * 50nm
sigma_A = 15   # * 50nm

baseDosePower = 1

def setTargetBox(pt1, pt2):
    global shotPixels
    
    for x in range(pt1[0], pt2[0] + 1):
        for y in range(pt1[1], pt2[1] + 1):
            shotPixels[x][y] = 1
            #print(shotPixels)


setTargetBox([15, 15], [30, 85])
setTargetBox([30, 15], [70, 30])
setTargetBox([30, 50], [70, 65])
setTargetBox([70, 15], [85, 85])

print("Shots set")

plt.matshow(shotPixels)
plt.show()

P_B = lambda rsquared : (eta/(sigma_B**2)) * np.exp(-rsquared/(sigma_B**2))
P_A = lambda rsquared : 0#1 if rsquared < 1 else 0 #(1  /(sigma_A**2)) * np.exp(-rsquared/(sigma_A**2))

scatterDistr = np.zeros((size, size))
for x in range(size):
    for y in range(size):
        scatterDistr[x][y] += (P_B(dist := (x-size/2)**2 + (y-size/2)**2) + P_A(dist))

##plt.matshow(scatterDistr)
##plt.colorbar()
##plt.show()


##for doseCount in range(1):
print("First convolution: ", end = "")
dosePixels = baseDosePower * scipy.signal.convolve2d(shotPixels, scatterDistr, mode = "same", boundary = "fill", fillvalue = "0")
print("done")
##    dosePixels[0][0] = 1
##    dosePixels[-1][-1] = 0

plt.matshow(dosePixels)
plt.colorbar()
plt.show()

correctedShots = (3 * shotPixels * (1 - dosePixels)) + shotPixels
plt.matshow(correctedShots)
plt.colorbar()
plt.show()

print("Corrected convolution: ", end = "")
correctedDosePixels = baseDosePower * scipy.signal.convolve2d(correctedShots, scatterDistr, mode = "same", boundary = "fill", fillvalue = "0")
print("done")

plt.matshow(correctedDosePixels)
plt.colorbar()
plt.show()

samplePixels = np.where(correctedDosePixels > 1, 1, 0)
plt.matshow(samplePixels)
plt.show()

##plt.matshow(np.where(samplePixels == 1 or shotPixels == 1, 1, 0) + shotPixels)
##plt.show()
