import time
import pendulum
import pickle
from os import system


MAP_DURATION:int = 180
MAP_NAMES = ["Ruins (Crypt)", "Frost Mtn", "Goblin Caves"]

def time_loop(loop_length_seconds, map_names) -> None:

    # Read in the start marker
    start_time = read_marker()
    # Report to user   
    print(f"Loading origin as >> {start_time}") 
    print(f"Maps: {map_names}")

    # Start loop
    while True:
        # Caluclate time since start
        time_since = start_time - pendulum.now()
        # Convert to time left in current window and how many completed windows have passed
        remaining_seconds, completed_windows = remaining_in_window(time_since.in_seconds(),loop_length_seconds)
        # Fetch info on current map using completed_windows and select desired map
        map_name, maps_to_target = map_name_from_cycle(completed_windows, map_names, 2)
        # Fulcap name of map if it's the target map
        map_name = map_name.upper() if maps_to_target == 0 else map_name
        # calc remaining info to show time till target/desired map
        remaining_to_target = max(0,remaining_seconds+((maps_to_target-1)*loop_length_seconds))
        
        # update report to user
        print(" "*35, end="\r")
        print(f" {map_name} [{remaining_seconds:03d} // {remaining_to_target}]", end="\r")
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
    return (seconds_elapsed%window_length_seconds,abs(seconds_elapsed//window_length_seconds))

def map_name_from_cycle(index:int,names:list[str]=["a", "b", "c"], target:int=0)->tuple[str,int]:
    """Converts current map index/count into a map name and also how many items
        away from the target you currently are

    Args:
        index (int): index of current map (can be a count of all maps observed)
        names (list[str], optional): list of maps names for display. Defaults to ["a", "b", "c"].
        target (int, optional): index of desired target. Defaults to 0.

    Returns:
        tuple[str,int]: name_of_current, index_to_target
    """
    cycle_size:int=len(names)
    return (names[index%cycle_size],2-(index%cycle_size))

def main() -> None:
    # write new time marker (comment it out after setting it the first time)
    # save_marker()
    system("cls")

    # Primary loop to track along with map timers
    time_loop(MAP_DURATION,MAP_NAMES)

if __name__ == "__main__":
    main()  