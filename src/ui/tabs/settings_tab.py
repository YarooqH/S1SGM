import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser

class SettingsTab(ttk.Frame):
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setup_ui()

    def setup_ui(self):
        settings_frame = ttk.LabelFrame(self, text="Application Settings")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Save directory setting
        self.create_save_dir_setting(settings_frame)
        
        # GitHub settings
        self.create_github_settings(settings_frame)
        
        # Save settings button
        save_btn = ttk.Button(settings_frame, text="Save Settings", command=self.save_settings)
        save_btn.grid(row=4, column=1, sticky=tk.E, padx=5, pady=20)
        
        # Help section
        self.create_help_section(settings_frame)

    def create_save_dir_setting(self, parent):
        ttk.Label(parent, text="Schedule I Save Directory:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=10)
        
        dir_frame = ttk.Frame(parent)
        dir_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=10)
        
        self.save_dir_entry = ttk.Entry(dir_frame, width=50)
        self.save_dir_entry.insert(0, self.config_manager.config["save_dir"])
        self.save_dir_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_save_dir)
        browse_btn.pack(side=tk.LEFT, padx=5)

    def create_github_settings(self, parent):
        ttk.Label(parent, text="GitHub Personal Access Token:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)
        
        token_frame = ttk.Frame(parent)
        token_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=10)
        
        self.token_entry = ttk.Entry(token_frame, width=50, show="*")
        if self.config_manager.config["github_token"]:
            self.token_entry.insert(0, self.config_manager.config["github_token"])
        self.token_entry.pack(side=tk.LEFT, padx=5)
        
        token_help_btn = ttk.Button(token_frame, text="?", width=2, 
                                   command=self.show_token_help)
        token_help_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(parent, text="GitHub Repository Name:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=10)
        
        repo_frame = ttk.Frame(parent)
        repo_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=10)
        
        self.repo_entry = ttk.Entry(repo_frame, width=50)
        if self.config_manager.config["github_repo"]:
            self.repo_entry.insert(0, self.config_manager.config["github_repo"])
        self.repo_entry.pack(side=tk.LEFT, padx=5)
        
        repo_help_btn = ttk.Button(repo_frame, text="?", width=2, 
                                  command=lambda: messagebox.showinfo(
                                      "Repository Name Help",
                                      "Enter your GitHub username followed by the desired repository name.\n\n"
                                      "Format: username/repository-name\n"
                                      "Example: johndoe/schedule1-saves\n\n"
                                      "If the repository already exists, it will be used.\n"
                                      "If not, a new private repository will be created."
                                  ))
        repo_help_btn.pack(side=tk.LEFT, padx=5)

    def create_help_section(self, parent):
        help_frame = ttk.LabelFrame(parent, text="Help")
        help_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=10)
        help_text = (
            "1. Create a GitHub Personal Access Token:\n"
            "   - Go to GitHub.com and log in\n"
            "   - Click your profile picture → Settings\n"
            "   - Scroll down to 'Developer settings' in the left sidebar\n"
            "   - Click 'Personal access tokens' → 'Tokens (classic)'\n"
            "   - Click 'Generate new token' → 'Generate new token (classic)'\n"
            "   - Give it a name like 'Schedule I Save Sync'\n"
            "   - For permissions, select:\n"
            "     • repo (all repo permissions)\n"
            "     • workflow\n"
            "   - Click 'Generate token'\n\n"
            "2. Repository Name should be in format: username/repository\n"
            "   Example: johndoe/schedule-1-saves"
        )
        
        help_label = ttk.Label(help_frame, text=help_text, justify=tk.LEFT)
        help_label.pack(padx=10, pady=10)

    def browse_save_dir(self):
        directory = filedialog.askdirectory(initialdir=self.config_manager.config["save_dir"])
        if directory:
            self.save_dir_entry.delete(0, tk.END)
            self.save_dir_entry.insert(0, directory)

    def show_token_help(self):
        webbrowser.open("https://github.com/settings/tokens")

    def save_settings(self):
        # Update config with new values
        self.config_manager.config["save_dir"] = self.save_dir_entry.get()
        self.config_manager.config["github_token"] = self.token_entry.get()
        self.config_manager.config["github_repo"] = self.repo_entry.get()
        
        # Save to file
        self.config_manager.save_config()
        messagebox.showinfo("Settings", "Settings saved successfully!") 