from matplotlib import pyplot as plt
import numpy as np

## Field of pixels to represent locations on sample
pixels = np.ones((100, 100))    # lengths in nm

beamPath = [[i, 50] for i in range(25, 75)]


##for i in range(220, 270):
##    beamPath.append([300, 0])

def DEI(rsquared):
    eta = 0.5
    alpha = 5 # nm
    beta = 5000 # nm
    ## https://doi.org/10.1016/S0167-9317(00)00320-8, equation in introduction:
    return 100/(1 + eta) * (((1/(np.pi * alpha**2)) * np.exp(-rsquared/alpha**2)) + ((eta/(np.pi * beta**2)) * np.exp(-rsquared/beta**2)))

def fireBeam(beamLoc):
    for y in range(len(pixels)):
        for x in range(len(pixels[0])):
            pixels[x][y] += DEI((beamLoc[0] - x)**2 + (beamLoc[1] - y)**2)
            pixels[x][y] = max(0, pixels[x][y])

for i, location in enumerate(beamPath):
    fireBeam(location)
    print(str(location) + ": " + str(i + 1) + "/" + str(len(beamPath)))

plt.matshow(pixels)
plt.show()
