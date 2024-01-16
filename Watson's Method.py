from matplotlib import pyplot as plt
import numpy as np

## Field of pixels to represent locations on sample
pixels = np.ones((100, 100))    # lengths in nm

beamLoc = [50, 50]


def DEI(rsquared):
    eta = 0.5
    alpha = 5 # nm
    beta = 5000 # nm
    ## https://doi.org/10.1016/S0167-9317(00)00320-8, equation in introduction:
    return 100/(1 + eta) * (((1/(np.pi * alpha**2)) * np.exp(-rsquared/alpha**2)) + ((eta/(np.pi * beta**2)) * np.exp(-rsquared/beta**2)))

for x in range(len(pixels)):
    for y in range(len(pixels[0])):
        pixels[x][y] -= DEI((beamLoc[0] - x)**2 + (beamLoc[1] - y)**2)
        pixels[x][y] = max(0, pixels[x][y])

##         np.array([[1, 2, 3],
##                   [4, 5, 6],
##                   [7, 8, 9]])

plt.matshow(pixels)
plt.show()
