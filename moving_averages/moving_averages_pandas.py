# Python program to calculate
# simple moving averages using pandas
import pandas as pd

arr = [1, 2, 3, 7, 9]
window_size = 3

# Convert array of integers to pandas series
numbers_series = pd.Series(arr)

# Get the window of series
# of observations of specified window size
windows = numbers_series.rolling(window_size)

# Create a series of moving
# averages of each window
moving_averages = windows.mean()

# Convert pandas series back to list
moving_averages_list = moving_averages.tolist()

# Remove null entries from the list
final_list = moving_averages_list[window_size - 1:]

print(final_list)
