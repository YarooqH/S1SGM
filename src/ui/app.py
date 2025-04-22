import tkinter as tk
from tkinter import ttk
from .tabs.my_saves_tab import MySavesTab
from .tabs.friends_tab import FriendsTab
from .tabs.settings_tab import SettingsTab
from config.config_manager import ConfigManager

class ScheduleISyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Schedule I Save Sync")
        self.root.geometry("800x600")
        
        self.config_manager = ConfigManager()
        self.create_ui()
    
    def create_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.my_saves_tab = MySavesTab(self.notebook, self.config_manager)
        self.friends_tab = FriendsTab(self.notebook, self.config_manager)
        self.settings_tab = SettingsTab(self.notebook, self.config_manager)
        
        self.notebook.add(self.my_saves_tab, text="My Saves")
        self.notebook.add(self.friends_tab, text="Friends' Saves")
        self.notebook.add(self.settings_tab, text="Settings") 