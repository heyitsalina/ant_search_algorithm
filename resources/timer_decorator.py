import time

class TimeTracker:
    execution_times = {}

def time_this(func):
    """
    A decorator that measures the execution time of a function and adds it to the total execution time.

    Parameters:
    func (function): The function to be decorated.

    Returns:
    function: The wrapper function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if func.__name__ not in TimeTracker.execution_times:
            TimeTracker.execution_times[func.__name__] = 0.0
        TimeTracker.execution_times[func.__name__] += elapsed_time

        return result
    return wrapper

def print_execution_times():
    """
    Prints the total execution time for each tracked function.

    This function iterates over the recorded execution times stored in
    TimeTracker.execution_times, prints the total time for each function, and
    then clears the stored times.
    """
    for func_name, total_time in TimeTracker.execution_times.items():
        print(f"Total execution time of {func_name}: {total_time:.4f} seconds")
    TimeTracker.execution_times.clear()
