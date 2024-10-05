# Seismic Event Detector

## Project Summary

The Seismic Event Detector is a Python application developed to analyze seismic data stored in MiniSEED (.mseed) files. The tool employs a combination of signal processing techniques to identify significant seismic events and visualize the corresponding data. It effectively tackles the challenge of detecting seismic activities by providing a user-friendly interface that allows for efficient file selection and data analysis. This program is crucial for contributing to a better understanding of seismic event dynamics on Mars and the moon.

## Project Details

The Seismic Event Detector reads seismic data from MiniSEED files, applies filtering techniques, and utilizes the Short-Term Average/Long-Term Average (STA/LTA) algorithm to identify peaks in seismic data that correspond to significant events. The algorithm runs to detect the highest peak in the seismic plot, which usually ends up being the start of the quake. It then looks for the closest and highest STA/LTA characteristic function peak. The time for this is used to plot the trigger on the seismic plot graph. The details of the data file, arrival time in relative and absolute time is then exported as a .csv to the directory of your choosing.  Here’s a brief overview of the program's functionalities:

1. **File Selection**: Users can easily browse and select .mseed files for analysis.
2. **Data Processing**: The program reads seismic data, applies a bandpass filter to enhance signal quality, and extracts relevant data for further analysis.
3. **Peak Detection**: It implements an STA/LTA detection algorithm to find the most significant seismic events, filtering for peaks that align with the highest velocity detected in the data.
4. **Visualization**: The application provides a graphical representation of the seismic data, marking the identified trigger points for easy interpretation.
5. **Data Export**: Finally, the tool compiles the results into a CSV file for easy record-keeping and further analysis.

### Benefits

The application features a simple GUI built with Tkinter, making it accessible even for users with minimal programming experience. It automates the process of seismic data analysis, saving time for researchers. The program detects seismic events by assessing both the seismic plot graph and the STA/LTA characteristic function graph, adding a creative, almost human element to it, which has proven to be better than a standalone STA/LTA algorithm at avoiding false positives. It solves the challenge by employing a creative, out of the box solution which combines different approaches to identify the beginning of seismic events fairly accurately.

### Tools and Technologies Used

- **Programming Language**: Python
- **Libraries**:
  - [`Tkinter](https://docs.python.org/3/library/tkinter.html)`: For building the GUI.
  - [`ObsPy`](https://docs.obspy.org/): For reading and processing seismic data.
  - [`NumPy`](https://numpy.org/): For numerical operations and data handling.
  - [`SciPy`](https://scipy.org/): For signal processing functions.
  - [`Matplotlib`](https://matplotlib.org/): For data visualization.
  - [`Pandas`](https://pandas.pydata.org/): For data manipulation and exporting results.


The source code is developed by Schimmel Hafeez of Team Astraios with the help of AI tools like ChatGPT and Blackbox to write code, explain the JupyterNotebook, and fix errors. The NASA-provided Jupyter Notebook was also heavily used in the making of this program. 
