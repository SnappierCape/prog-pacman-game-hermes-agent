"""Game difficulty settings for ghost spawn rates and behavior"""

# Define different difficulty levels with distinct ghost behaviors
DIFFICULTY_SETTINGS = {
    'easy': {
        'name': 'Easy Mode',
        'description': 'Few ghosts, slow movement - perfect for beginners',
        'ghost_count': 2,  # Only spawn 2 out of 4 possible ghosts
        'spawn_delay': 3.0,  # Seconds between spawning each ghost
        'move_speed_factor': 0.6,  # Ghosts move at 60% normal speed
        'tracking_aggressiveness': 0.7  # Lower tracking intensity toward player
    },
    'normal': {
        'name': 'Normal Mode', 
        'description': 'Balanced challenge for average players',
        'ghost_count': 3,
        'spawn_delay': 2.0,
        'move_speed_factor': 0.85,
        'tracking_aggressiveness': 0.9
    },
    'hard': {
        'name': 'Hard Mode - Pro',
        'description': 'Maximum ghost pressure for expert players', 
        'ghost_count': 4,
        'spawn_delay': 1.5,
        'move_speed_factor': 1.0,
        'tracking_aggressiveness': 1.2
    }
}

class DifficultySelector:
    """Handles game difficulty selection and settings management"""
    
    def __init__(self):
        self.diffs = list(DIFFICULTY_SETTINGS.keys())
        self.current_difficulty = 'normal'
        self.settings = DIFFICULTY_SETTINGS[self.current_difficulty]
        
    def get_available_difficulties(self):
        """Return list of available difficulty names"""
        return [DIFFICULTY_SETTINGS[d]['name'] for d in self.diffs]
        
    def select_next(self):
        """Cycle to next difficulty level"""
        idx = (self.diffs.index(self.current_difficulty) + 1) % len(self.diffs)
        return self.diffs[idx]
        
    def apply_settings(self):
        """Apply selected difficulty settings and return them"""
        return self.settings.copy()
