import os
import json
from tkinter import messagebox

class ConfigManager:
    def __init__(self):
        self.default_save_dir = os.path.join(os.environ['USERPROFILE'], 
                                         "AppData", "LocalLow", "TVGS", "Schedule I", "Saves")
        self.config_dir = os.path.join(os.environ['APPDATA'], "ScheduleISync")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.config = self.load_config()

    def load_config(self):
        default_config = {
            "save_dir": self.default_save_dir,
            "github_token": "",
            "github_repo": "",
            "friends": []
        }
        
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {str(e)}")
        
        return default_config

    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {str(e)}") 