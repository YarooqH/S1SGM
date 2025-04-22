import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from utils.github_manager import GitHubManager
from utils.save_manager import SaveManager

class MySavesTab(ttk.Frame):
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        self.config_manager = config_manager
        self.github_manager = GitHubManager(config_manager)
        self.save_manager = SaveManager(config_manager)
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.LabelFrame(self, text="My Save Files")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status info
        self.create_status_frame(frame)
        
        # Sync buttons
        self.create_button_frame(frame)
        
        # GitHub repo link
        self.create_link_frame(frame)
    
    def create_status_frame(self, parent):
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(status_frame, text="Save Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.save_dir_label = ttk.Label(status_frame, text=self.config_manager.config["save_dir"])
        self.save_dir_label.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(status_frame, text="GitHub Repository:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.repo_label = ttk.Label(status_frame, text=self.config_manager.config["github_repo"] or "Not configured")
        self.repo_label.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(status_frame, text="Last Sync:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.last_sync_label = ttk.Label(status_frame, text="Never")
        self.last_sync_label.grid(row=2, column=1, sticky=tk.W, pady=5)
    
    def create_button_frame(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        self.sync_btn = ttk.Button(button_frame, text="Sync to GitHub", 
                                  command=self.sync_to_github)
        self.sync_btn.pack(side=tk.LEFT, padx=10)
        
        self.backup_btn = ttk.Button(button_frame, text="Create Local Backup", 
                                    command=self.create_backup)
        self.backup_btn.pack(side=tk.LEFT, padx=10)
    
    def create_link_frame(self, parent):
        link_frame = ttk.Frame(parent)
        link_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.open_repo_btn = ttk.Button(link_frame, text="Open My GitHub Repository", 
                                       command=self.open_github_repo)
        self.open_repo_btn.pack(side=tk.LEFT, padx=10)
    
    def sync_to_github(self):
        try:
            self.github_manager.sync_saves()
            self.last_sync_label.config(text=self.github_manager.last_sync_time)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def create_backup(self):
        try:
            backup_path = self.save_manager.create_backup()
            messagebox.showinfo("Backup", f"Backup created successfully at:\n{backup_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def open_github_repo(self):
        if self.config_manager.config["github_repo"]:
            webbrowser.open(f"https://github.com/{self.config_manager.config['github_repo']}")
        else:
            messagebox.showinfo("Info", "Please configure your GitHub repository in Settings first.") 