import time

def time_this(func):
    """
    A decorator that measures and prints the execution time of a function.

    Parameters:
    func (function): The function to be decorated.

    Returns:
    function: The wrapper function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time of {func.__name__}: {end_time - start_time:.4f} seconds")
        return result
    return wrapper