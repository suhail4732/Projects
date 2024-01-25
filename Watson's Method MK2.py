from matplotlib import pyplot as plt
from matplotlib import colormaps
import numpy as np
import scipy.signal

size = 100

shotPixels = np.zeros((size, size)) # * 50nm

fig, ax = plt.subplots(2, 3, figsize = (8,8))


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


setTargetBox([10, 45], [90, 55])
setTargetBox([45, 10], [55, 90])
##setTargetBox([30, 15], [70, 30])
##setTargetBox([30, 50], [70, 65])
##setTargetBox([70, 15], [85, 85])

print("Shots set")

##plt.subplot(2, 3, 1)
ax[0, 0].matshow(shotPixels)
#plt.show()

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
dosePixels = baseDosePower * scipy.signal.convolve2d(shotPixels, scatterDistr, mode = "same", boundary = "fill", fillvalue = "0")# + shotPixels
print("done")
##    dosePixels[0][0] = 1
##    dosePixels[-1][-1] = 0

im = ax[0, 1].matshow(dosePixels)
fig.colorbar(im, ax=ax[0, 1], orientation="horizontal", pad=0.025)
##ax[0, 1].colorbar()
##plt.show()

samplePixels = np.where(dosePixels > 1, 1, 0)
ax[0, 2].matshow(samplePixels)

correctedShots = (2 * shotPixels * (1 - dosePixels)) + shotPixels
im = ax[1, 0].matshow(correctedShots)
fig.colorbar(im, ax=ax[1, 0], orientation="horizontal", pad=0.025)
##ax[1, 0].colorbar()
##plt.show()

print("Corrected convolution: ", end = "")
correctedDosePixels = baseDosePower * scipy.signal.convolve2d(correctedShots, scatterDistr, mode = "same", boundary = "fill", fillvalue = "0")# + correctedShots
print("done")

im = ax[1, 1].matshow(correctedDosePixels)
fig.colorbar(im, ax=ax[1, 1], orientation="horizontal", pad=0.025)
##ax[1, 1].colorbar()
##plt.show()

samplePixels = np.where(correctedDosePixels > 1, 1, 0)
ax[1, 2].matshow(samplePixels)

ax[0, 0].set_title("(a)")
ax[0, 1].set_title("(b)")
ax[0, 2].set_title("(c)")
ax[1, 0].set_title("(d)")
ax[1, 1].set_title("(e)")
ax[1, 2].set_title("(f)")


plt.show()

##plt.matshow(np.where(samplePixels == 1 or shotPixels == 1, 1, 0) + shotPixels)
##plt.show()
