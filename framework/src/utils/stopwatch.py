"""
This module provides convenient methods to keep the time and give time deltas.
"""
from datetime import datetime

class StopWatch:
    """
    This class has methods to start, stop and get time deltas between tests.
    """
    def __init__(self):
        """
        Constructor initializes the t0 time and keeps it.
        """
        self.timeSinceStart = datetime.now()
        self.timeStart = None
        self.timeStop  = None
    
    def startTimer(self):
        """
        This funtion starts the timer by assigning current time.
        """
        self.timeStart = datetime.now()
        
    def timeDeltaFly(self):
        """
        This funtion gives the time delta between the start of the timer and now.
        @see: getTimeDelta()
        """
        return str(datetime.now() - self.timeStart)
    
    def stopTimer(self):
        """
        This funtion stops the timer.
        """
        self.timeStop = datetime.now()
        
    def getTimeDelta(self):
        """
        This funtion should be called after calling stopTimer(). This function
        gives the time delta between the start and stop of the timer.
        @see: timeDeltaFly()
        """
        if self.startTimer == None:
            raise Exception('Stop Watch was not started!')
        if self.stopTimer == None:
            raise Exception('Stop Watch was not stoped!')
        return str(self.timeStop - self.timeStart)
    
    def getTimeSinceStart(self):
        """
        This funtion gives the time delta of the t0 and now.
        """
        return str(self.timeSinceStart - datetime.now())