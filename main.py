# An attempt to rewrite the codebase as a script

import numpy as np
import pandas as pd
import dask.dataframe as dd
import matplotlib.pyplot as plt
import json

chunksize = 10 ** 4
filepath = "data/2022_place_canvas_history.csv"

ddf = dd.read_csv(filepath, blocksize="25MB")

part = ddf.partitions[2]
part["timestamp"] = dd.to_datetime(part["timestamp"])
# part.sort_values(by=["timestamp"], ascending=True)

print("Formatted CSV.")

timestamp_idx = 1
user_id_idx = 2


# Danny's rewrite attempt

## Re-arrange the data set to organize it by key: user value: time place
## TO DO: Maybe use dataframe to organize this data set instead due to it's large size?
user_pixels_placed = {}

for row in part.itertuples():
    user_id = row[user_id_idx]
    if not (user_id in user_pixels_placed):
        user_pixels_placed[user_id] = []
    user_pixels_placed[user_id].append(row[timestamp_idx])

## Process this data
user_placement_variance = {}

for user_id in user_pixels_placed.keys():
    placement_time_list = user_pixels_placed[user_id]
    # 2 pixels placements aren't sufficient and will end up in the values equating to one
    if len(placement_time_list)>2:
        # Find differences between pixel placements
        difference_in_time = []
        for i in range(1, len(placement_time_list)):
            difference_in_time.append( abs(placement_time_list[i] - placement_time_list[i - 1]).total_seconds() )
        # Compare differences between the pixels placed by dividing idk if this is a good way or hella inefficient probably is
        average = sum(difference_in_time) / len(difference_in_time)

        variance = []
        for time in difference_in_time:
            # scuffed fix for now but not understanding how tf people getting 0 seconds
            if average > 0 and time > 0:
                variance.append(time / average)

        if len(variance) > 0:
            user_placement_variance[user_id] = sum(variance) / len(variance)

with open("variance.txt", "w") as file:
    file.write(json.dumps(user_placement_variance))