import time
import pendulum
import pickle
from os import system


MAP_DURATION:int = 180
MAP_NAMES = [" The Frost Mountain ", " The Goblin Caves ", "Ruins Castle (Crypt)"]
MAP_TARGET = 1

def time_loop(loop_length_seconds:int, map_names:list[str], target_index:int) -> None:

    list_len = len(map_names) 
    display_len = 3+sum([len(x)+3 for x in map_names])
    full_cycle_length = loop_length_seconds*list_len
    # Read in the start marker
    start_time = read_marker()
    # Report to user   
    print(f"Loading origin as >> {start_time}") 
    print(f"Target:\t\t {target_index} - {map_names[target_index]}")    
    print(f"Maps:\t\t {map_names}")

    print("")

    # Start loop
    while True:
        # Caluclate time since start                    
        time_since = start_time - pendulum.now()

        # Convert to time left in current window and how many completed windows have passed
        remaining_seconds, completed_windows = calc_window(time_since.in_seconds(),loop_length_seconds)
        
        # Fetch info on current map using completed_windows
        map_name, map_index = get_map_from_cycle(completed_windows, map_names, target_index)

        # Determine where in the cycle we are
        maps_to_target = target_index - map_index 
        if maps_to_target < 0:
            maps_to_target += list_len
       
        # Fulcap name of map if it's the target map
        map_name = map_name.upper() if maps_to_target == 0 else map_name
        
        # calc remaining info to show time till target/desired map
        remaining_to_target = max(0,remaining_seconds+((maps_to_target-1)*loop_length_seconds))

        # format seconds into full timer format (to handle things larger that just a few sec)
        duration_of_window = pendulum.duration(seconds=remaining_seconds)
        duration_to_target = pendulum.duration(seconds=remaining_to_target)
        progress_display = progress_bar_string(progress_calc(full_cycle_length-remaining_to_target,full_cycle_length),display_len, 33)

        # update report to user
        print(" "*55, end="\r")
        # print(f" {map_name=} {map_index=} {remaining_seconds=} {completed_windows=} [{duration_of_window.minutes}:{duration_of_window.seconds%60:02d} // {duration_to_target.minutes}:{duration_to_target.seconds%60:02d}]", end="\r")
        # print(f" {map_name} [{duration_of_window.minutes}:{duration_of_window.seconds%60:02d} // {duration_to_target.minutes}:{duration_to_target.seconds%60:02d}]", end="\r")
        print(f"[{duration_of_window.minutes}:{duration_of_window.seconds%60:02d} // {duration_to_target.minutes}:{duration_to_target.seconds%60:02d}] \t {progress_display}", end="\r")
        time.sleep(.5)

def save_marker(fn:str="start.time") -> None:
    """Simple wrapper to write a Pendulum Datetime to file using Pickle to convert obj

    Args:
        fn (str, optional): name of desired file. Defaults to "start.time".
    """
    with open(fn, "wb") as file:
        pickle.dump(pendulum.now(), file, pickle.HIGHEST_PROTOCOL)

def read_marker(fn:str="start.time") -> pendulum.Date:
    """Simple wrapper to read in the time marker using Pickle to rebuild
        a Pendulum.py datetime

    Args:
        fn (str, optional): name of desired file. Defaults to start.time".

    Returns:
        pendulum.Date: start time from file
    """
    with open(fn, "rb") as file:
        return pickle.load(file)

def calc_window(seconds_elapsed:int,window_length_seconds:int=180) -> tuple[int,int]:
    """Returns the number of seconds remaining in the current window 
        uses time elapsted from a known target time

    Args:
        seconds_elapsed (int): time in seconds since the know start/change marker
        window_length_seconds (int, optional): _description_. Defaults to 180.

    Returns:
        tuple[int,int]: seconds_remaining, num_of_windows_observed
    """
    return (seconds_elapsed%window_length_seconds,abs(seconds_elapsed//window_length_seconds))

def get_map_from_cycle(index:int,names:list[str]=["a", "b", "c"], target:int=0)->tuple[str,int]:
    """Converts current map index/count into a map name and index

    Args:
        index (int): index of current map (can be a count of all maps observed)
        names (list[str], optional): list of maps names for display. Defaults to ["a", "b", "c"].
        target (int, optional): DISCONTINUED. Defaults to 0.

    Returns:
        tuple[str,int]: name_of_current, index_of_current
    """
    cycle_size:int=len(names)
    index_mod = index%cycle_size
    return (names[index_mod],index_mod)

def progress_bar_string(percent_complete:float|int, width_to_fill:int=25, offset:int=0, fill_char:str="_", marker_char:str="|>") -> str:
    """Builds a display string of desired width with a marker along the portion of the string 
        that fits the percent_complete.

    Args:
        percent_complete (float | int): Percent complete (can be out of 100 or 1.0)
        width_to_fill (int, optional): Number of characters to fill. Defaults to 25.
        offset (int, optional): Offset if you'd like to have the ZERO value somewhere other than the default left. Defaults to 0.
        fill_char (str, optional): Character to fill the 'blank' spaces. Defaults to "_".

    Returns:
        str: Display-able string with a marker at the desired percent
    """
    # handle percent when given floats
    if percent_complete < 1:
        percent_complete = round(percent_complete*100)
    # add offset to the current percent to allow non-left-side-based progress in looping
    percent_complete +=offset
    if percent_complete > 100:
        percent_complete = percent_complete % 100
    # determin how many percent each char represents
    percent_per_char = 100/width_to_fill
    # set left and right buffer sizes based 
    left = round(percent_complete/percent_per_char)-len(marker_char)
    right = round((100-percent_complete)/percent_per_char)

    # return f"{" ": <left}|{" ": >right}"
    # Above can't work since we need to dynamically do it
    return fill_char*left + marker_char + fill_char*right

def progress_calc(current:int|float=50,total:int|float=100) -> float:
    """Calculates the progress of something given the current value and total

    Args:
        current (int | float, optional): Current Progress/Index. Defaults to 50.
        total (int | float, optional): Max or Total size. Defaults to 100.

    Returns:
        float: the percent completed (rescaled to be percent of 1.0)
    """
    fraction = current / total
    return min(1,max(0,fraction))


def main() -> None:
    # write new time marker (comment it out after setting it the first time)
    # save_marker()
    system("cls")
    
    # Primary loop to track along with map timers
    time_loop(MAP_DURATION,MAP_NAMES,MAP_TARGET)

if __name__ == "__main__":
    main()  