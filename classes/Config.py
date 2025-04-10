import json
import time
from datetime import datetime

class Config:
    def __init__(self):
        self.reset()  # Initialize with default values
    
    def reset(self):
        """Reset all values to their defaults"""
        self._should_be_running = False  # Changed to reflect desired state
        self._laps_elapsed = 0
        self._laps_total = 0
        self._lap_start_timestamps = []
    
    def set_laps_target(self, total_laps):
        """Set the target number of laps"""
        if not isinstance(total_laps, int) or total_laps < 0:
            raise ValueError("Total laps must be a positive integer")
        self._laps_total = total_laps
    
    def add_lap(self):
        """Add a completed lap (increments count and records timestamp)"""
        self._laps_elapsed += 1
        self.writelaptime()
        
    def set_attributes(self, should_be_running=None, laps_elapsed=None, laps_total=None, lap_start_timestamps=None):
        if should_be_running is not None:
            self._should_be_running = should_be_running
        if laps_elapsed is not None:
            self._laps_elapsed = laps_elapsed
        if laps_total is not None:
            self._laps_total = laps_total
        if lap_start_timestamps is not None:
            if isinstance(lap_start_timestamps, (list, tuple)):
                for ts in lap_start_timestamps:
                    self._validate_timestamp(ts)
                self._lap_start_timestamps = list(lap_start_timestamps)
            else:
                self._validate_timestamp(lap_start_timestamps)
                self._lap_start_timestamps = [lap_start_timestamps]
    
    def _validate_timestamp(self, timestamp):
        """Validate that the timestamp is a reasonable UNIX timestamp"""
        current_time = int(time.time())
        if not isinstance(timestamp, (int, float)):
            raise ValueError("Timestamp must be a number")
        if timestamp < 0:
            raise ValueError("Timestamp cannot be negative")
        if timestamp > current_time + 86400:  # Allow timestamps up to 1 day in future
            raise ValueError("Timestamp too far in the future")
    
    def set_should_be_running(self, value):
        """Set whether the system should be running"""
        self._should_be_running = bool(value)
    
    def add_lap_elapsed(self, value):
        self._laps_elapsed = value + 1
    
    def set_laps_total(self, value):
        self._laps_total = value
    
    def add_lap_timestamp(self, timestamp=None):
        """Add a lap timestamp (current time if none provided)"""
        if timestamp is None:
            timestamp = time.time()
        self._validate_timestamp(timestamp)
        self._lap_start_timestamps.append(timestamp)
    
    def writelaptime(self):
        """Append the current time as a lap timestamp"""
        self.add_lap_timestamp()
    
    # Property getters
    @property
    def should_be_running(self):
        """Check if the system should be running"""
        return self._should_be_running
    
    @property
    def laps_elapsed(self):
        return self._laps_elapsed
    
    @property
    def laps_total(self):
        return self._laps_total
    
    @property
    def lap_start_timestamps(self):
        return self._lap_start_timestamps.copy()
    
    # Additional getters
    def get_config_dict(self):
        """Return a dictionary of all configuration values"""
        return {
            'should_be_running': self._should_be_running,
            'laps_elapsed': self._laps_elapsed,
            'laps_total': self._laps_total,
            'lap_start_timestamps': self._lap_start_timestamps.copy()
        }
    
    def get_last_lap_time(self):
        """Get the timestamp of the last lap started"""
        if not self._lap_start_timestamps:
            return None
        return self._lap_start_timestamps[-1]
    
    def get_last_lap_time_formatted(self):
        """Get formatted string of last lap time"""
        last_lap = self.get_last_lap_time()
        if last_lap is None:
            return "No laps recorded"
        return datetime.fromtimestamp(last_lap).strftime('%Y-%m-%d %H:%M:%S')
    
    def get_laps_remaining(self):
        """Calculate remaining laps"""
        return max(0, self._laps_total - self._laps_elapsed)
    
    def is_complete(self):
        """Check if all laps are completed"""
        return self._laps_elapsed >= self._laps_total > 0
    
    def get_formatted_config(self):
        """Return a human-readable string of the configuration"""
        return (
            f"Should be running: {'Yes' if self._should_be_running else 'No'}\n"
            f"Laps Completed: {self._laps_elapsed}/{self._laps_total}\n"
            f"Laps Remaining: {self.get_laps_remaining()}\n"
            f"Last Lap Time: {self.get_last_lap_time_formatted()}\n"
            f"All Lap Times: {[self.get_last_lap_time_formatted() for _ in self._lap_start_timestamps]}"
        )
    
    def __str__(self):
        return self.get_formatted_config()
    
    def save_to_json(self, filename="config.json"):
        """Save configuration to JSON file in the config directory"""
        filepath = f"config/{filename}"
        with open(filepath, 'w') as f:
            json.dump(self.get_config_dict(), f, indent=4)

    @classmethod
    def load_from_json(cls, filename="config.json"):
        """Load configuration from JSON file in the config directory and return a Config instance"""
        filepath = f"config/{filename}"
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        config = cls()
        config.set_attributes(
            should_be_running=data.get('should_be_running', False),
            laps_elapsed=data.get('laps_elapsed', 0),
            laps_total=data.get('laps_total', 0),
            lap_start_timestamps=data.get('lap_start_timestamps', [])
        )
        return config