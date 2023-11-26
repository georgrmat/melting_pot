import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
from classes import *

def animated_scatter_plot():
    # Set up the figure and axis
    fig, ax = plt.subplots()
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    # Create a Streamlit placeholder for the plot
    plot_placeholder = st.empty()

    # Run the simulation
    for i in range(50):
        # Generate random coordinates
        x = np.random.random()
        y = np.random.random()

        # Plot the point
        plt.plot(x, y, '.', color='blue')
        plt.xlim(0, 1)
        plt.ylim(0, 1)

        # Display the plot in Streamlit
        plot_placeholder.pyplot(fig)

        # Pause for a short duration
        time.sleep(0.1)

        # Clear the current axis
        ax.cla()

        # Check if the stop button is pressed
        if stop_button:
            plt.close()
            return

    # Close the plot after the loop
    plt.close()

# Create start and stop buttons
start_button = st.button("Launch")
stop_button = st.button("Stop")

# Check if the start button is pressed
if start_button:
    animated_scatter_plot()
