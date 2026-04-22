import numpy as np

BUTTON_NAME = "Onde Sinusoïdale"

def generate_plot(figure):
    ax = figure.add_subplot(111)
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax.plot(x, y, color='blue')
    ax.set_title("Sinus")
