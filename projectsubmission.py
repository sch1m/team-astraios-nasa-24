import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from obspy import read
from obspy.signal.trigger import classic_sta_lta
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from datetime import timedelta
import pandas as pd 

def select_file():
    filepath = filedialog.askopenfilename(title="Select Test File", filetypes=[("mseed files", "*.mseed")])
    entry.delete(0, tk.END)
    entry.insert(0, filepath)
    popup_root.lift()
    popup_root.focus_force() 

def run_analysis():
    filepath = entry.get()
    if not filepath:
        messagebox.showerror("Error", "Please select a file")
        return
    try:
        analysis(filepath)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        popup_root.destroy()

def analysis(filepath):
    # Read in seismic data using ObsPy
    st = read(filepath)

    # Apply the bandpass filter
    minfreq = 0.5
    maxfreq = 1.0
    st_filt = st.copy()
    st_filt.filter('bandpass', freqmin=minfreq, freqmax=maxfreq)
    tr_filt = st_filt.traces[0].copy()
    tr_times_filt = tr_filt.times()
    tr_data_filt = tr_filt.data

    # Extract seismic data
    csv_times = tr_times_filt
    csv_data = tr_data_filt

    # Identify the highest velocity peak
    max_vel_index = np.argmax(csv_data)
    max_vel_time = csv_times[max_vel_index]
    print(f"Highest peak in velocity found at time {max_vel_time} s with value {csv_data[max_vel_index]} m/s")

    # Implement STA/LTA detection algorithm
    df = tr_filt.stats.sampling_rate
    sta_len = 120
    lta_len = 600
    cft = classic_sta_lta(tr_data_filt, int(sta_len * df), int(lta_len * df))

    # Find all peaks in the STA/LTA characteristic function
    cft_peaks, _ = find_peaks(cft) 
    cft_peak_times = tr_times_filt[cft_peaks]
    cft_peak_values = cft[cft_peaks]

    # Define a window size around the velocity peak
    window_size = 1000

    # Filter STA/LTA peaks within the window around the velocity peak
    valid_peaks_indices = np.where(np.abs(cft_peak_times - max_vel_time) <= window_size)[0]

    if len(valid_peaks_indices) == 0:
        print("No valid STA/LTA peak found within the specified range.")
        messagebox.showerror("Error", "No valid STA/LTA peak found within the specified range.")
        return

    # Select the highest STA/LTA peak within this window
    highest_peak_index_in_window = valid_peaks_indices[np.argmax(cft_peak_values[valid_peaks_indices])]
    closest_trigger_time = cft_peak_times[highest_peak_index_in_window]
    print(f"Closest highest STA/LTA trigger found at time {closest_trigger_time} s")

    # Plot the graph with the Best Trigger On line
    plt.figure(figsize=(12, 6))
    plt.plot(csv_times, csv_data)
    plt.axvline(x=closest_trigger_time, color='green', label='Best Trigger On')
    plt.xlim([min(csv_times), max(csv_times)])
    plt.ylabel('Velocity (m/s)')
    plt.xlabel('Time (s)')
    plt.title(f'{filepath}', fontweight='bold')
    plt.legend()

    plt.tight_layout()
    plt.show()

    # Detection Export to Catalog
    fname = filepath 
    starttime = tr_filt.stats.starttime.datetime 

    # Calculate the absolute time for the best trigger
    best_trigger_time_abs = starttime + timedelta(seconds=closest_trigger_time)
    best_trigger_time_str = best_trigger_time_abs.strftime('%Y-%m-%dT%H:%M:%S.%f')

    # Compile DataFrame with only the Best Trigger On
    detect_df = pd.DataFrame(data={
        'filename': [fname],
        'time_abs(%Y-%m-%dT%H:%M:%S.%f)': [best_trigger_time_str],
        'time_rel(sec)': [closest_trigger_time]
    })

    # Export the detection catalog to a CSV file
    output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save Catalog")
    if output_path:
        detect_df.to_csv(output_path, index=False)
        print(f"Catalog exported to {output_path}")

# GUI Setup
root = tk.Tk()
root.title("Seismic Event Detector by Schimmel")
root.state("zoomed")

heading = tk.Label(root, text="Welcome to Seismic Event Detector", font=("Arial", 40, "bold"))
heading.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

subheading = tk.Label(root, text="by Team Astraios", font=("Arial", 20, "bold"))
subheading.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

button = tk.Button(root, text="Analyze Data", font=("Arial", 20), command=lambda: popup())
button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def popup():
    global popup_root
    popup_root = tk.Toplevel(root)
    popup_root.title("Select Test File")
    popup_root.resizable(False, False)

    label = tk.Label(popup_root, text="Please select a test file (.mseed file)")
    label.pack()

    global entry
    entry = tk.Entry(popup_root, width=50)
    entry.pack()

    browse_button = tk.Button(popup_root, text="Browse", command=select_file)
    browse_button.pack()

    run_button = tk.Button(popup_root, text="Run", command=run_analysis)
    run_button.pack()

root.mainloop()

'''
Sources: demo_notebook provided by NASA, resources in NASA's data packet, AI assistance
Working: Adds a human element to the detection process by looking at the velocity/time seismic plot first,
and judging the best prediction for the quake by also assessing the STA/LTA characteristic function graph.
This program works well for most data tested on it, except for a few where sudden bursts of velocity throws it off.
Made by Schimmel Hafeez of Team Atraios with the help of AI tools, NASA Space Apps 2024, Pakistan
'''
