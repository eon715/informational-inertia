import numpy as np
from inertia.analyze import analyze

np.random.seed(0)

# noise
x = np.random.randn(2000)
np.savetxt("noise.csv", x, delimiter=",")

r_noise = analyze("noise.csv")

# structured signal
t = np.linspace(0, 10*np.pi, 2000)
y = np.sin(t)
np.savetxt("signal.csv", y, delimiter=",")

r_signal = analyze("signal.csv")

print("NOISE Ī:", r_noise.I_bar)
print("SIGNAL Ī:", r_signal.I_bar)

assert r_signal.I_bar > r_noise.I_bar
