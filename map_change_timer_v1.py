import time
import pendulum
import pickle
from os import system


MAP_DURATION:int = 180
MAP_NAMES = ["Goblin Caves", "The Forgotten Castle (Crypt)", "The Frost Mountain"]
MAP_TARGET = 0

def time_loop(loop_length_seconds:int, map_names:list[str], target_index:int) -> None:

    # Read in the start marker
    start_time = read_marker()
    # Report to user   
    print(f"Loading origin as >> {start_time}") 
    print(f"Maps:\t {map_names}")
    print(f"Target:\t {target_index} - {map_names[target_index]}")
    print("")

    # Start loop
    while True:
        # Caluclate time since start
        time_since = start_time - pendulum.now()
        # Convert to time left in current window and how many completed windows have passed
        remaining_seconds, completed_windows = remaining_in_window(time_since.in_seconds(),loop_length_seconds)
        # Fetch info on current map using completed_windows and select desired map

        map_name, map_index = get_map_from_cycle(completed_windows, map_names, target_index)
        # maps_to_target = (map_index-target_index) % len(map_names)
        maps_to_target = target_index-map_index
   
       
        # Fulcap name of map if it's the target map
        map_name = map_name.upper() if maps_to_target == 0 else map_name
        # calc remaining info to show time till target/desired map
        remaining_to_target = remaining_seconds+((maps_to_target-1)*loop_length_seconds)
        
        # update report to user
        print(" "*35, end="\r")
        print(f" {map_name} [{remaining_seconds:03d} // {map_index} {maps_to_target} {remaining_to_target}]", end="\r")
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
        fn (str, optional): name of desired file. Defaults to "start.time".

    Returns:
        pendulum.Date: start time from file
    """
    with open(fn, "rb") as file:
        return pickle.load(file)

def remaining_in_window(seconds_elapsed:int,window_length_seconds:int=180) -> tuple[int,int]:
    """Returns the number of seconds remaining in the current window 
        uses time elapsted from a known target time

    Args:
        seconds_elapsed (int): time in seconds since the know start/change marker
        window_length_seconds (int, optional): _description_. Defaults to 180.

    Returns:
        tuple[int,int]: seconds_remaining, num_of_windows_observed
    """
    return (seconds_elapsed%window_length_seconds,seconds_elapsed//window_length_seconds)

def get_map_from_cycle(index:int,names:list[str]=["a", "b", "c"], target:int=0)->tuple[str,int]:
    """Converts current map index/count into a map name and also how many items
        away from the target you currently are

    Args:
        index (int): index of current map (can be a count of all maps observed)
        names (list[str], optional): list of maps names for display. Defaults to ["a", "b", "c"].
        target (int, optional): index of desired target. Defaults to 0.

    Returns:
        tuple[str,int]: name_of_current, index_of_current
    """
    cycle_size:int=len(names)
    return (names[index%cycle_size],index%cycle_size)

def main() -> None:
    # write new time marker (comment it out after setting it the first time)
    # save_marker()
    system("cls")

    # Primary loop to track along with map timers
    time_loop(MAP_DURATION,MAP_NAMES,MAP_TARGET)

if __name__ == "__main__":
    main()  