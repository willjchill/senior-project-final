import pywt
import numpy as np

# Sample data
data = np.genfromtxt('rest_ex.csv', delimiter=',')
data = data[0:1000]
data = data - np.mean(data)
wavelet = 'db1'  
level = 3       
modwt_coefficients = pywt.mra(data, wavelet, level)
print(np.array(modwt_coefficients))

# import matplotlib.pyplot as plt

# plt.figure(figsize=(10, 6))
# for i in range(1, level+2):
#     plt.subplot(level+2, 1, i)
#     plt.plot(modwt_coefficients[i-1])

# plt.tight_layout()
# plt.show()

# Perform wavelet transform
# wavelet = 'db1'  # You can choose different wavelets
# coefficients = pywt.wavedec(data, wavelet, level=3)

# for c in coefficients:
#     print(c.shape)

# Print coefficients
# print(coefficients)