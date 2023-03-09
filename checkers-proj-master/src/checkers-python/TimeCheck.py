import time

# Timer class
class TimeCheck():
    def __init__(self):
        self.time = 0           # Total time elapsed
        self.start_time = 0     # When the timer starts/resumes

    def start(self):
        # Set the start time to the current time
        self.start_time = time.time()

    def pause(self):
        # Add the elapsed time to the total
        self.time += time.time() - self.start_time

    def check_time(self):
        # Return the total elapsed time
        return (self.time + (time.time() - self.start_time))
