import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import shutil
from github import Github
from datetime import datetime

class ScheduleISyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Schedule I Save Sync")
        self.root.geometry("800x600")
        
        # Default save directory path
        self.default_save_dir = os.path.join(os.environ['USERPROFILE'], 
                                            "AppData", "LocalLow", "TVGS", "Schedule I", "Saves")
        
        # Config file path
        self.config_dir = os.path.join(os.environ['APPDATA'], "ScheduleISync")
        self.config_file = os.path.join(self.config_dir, "config.json")
        
        # Load or create config
        self.load_config()
        
        # Create UI
        self.create_ui()
    
    def load_config(self):
        """Load configuration or create default if not exists"""
        self.config = {
            "save_dir": self.default_save_dir,
            "github_token": "",
            "github_repo": "",
            "friends": [],
            "shared_folder": ""
        }
        
        # Create config directory if it doesn't exist
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        # Load existing config if available
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {str(e)}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {str(e)}")
    
    def create_ui(self):
        """Create the main user interface"""
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.my_saves_tab = ttk.Frame(self.notebook)
        self.friends_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.my_saves_tab, text="My Saves")
        self.notebook.add(self.friends_tab, text="Friends' Saves")
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Setup each tab
        self.setup_my_saves_tab()
        self.setup_friends_tab()
        self.setup_settings_tab()
    
    def setup_my_saves_tab(self):
        """Setup the My Saves tab"""
        frame = ttk.LabelFrame(self.my_saves_tab, text="My Save Files")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status info
        status_frame = ttk.Frame(frame)
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(status_frame, text="Save Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.save_dir_label = ttk.Label(status_frame, text=self.config["save_dir"])
        self.save_dir_label.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(status_frame, text="Shared Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.shared_folder_label = ttk.Label(status_frame, text=self.config.get("shared_folder", "Not configured"))
        self.shared_folder_label.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(status_frame, text="Last Sync:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.last_sync_label = ttk.Label(status_frame, text="Never")
        self.last_sync_label.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Sync buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        self.sync_btn = ttk.Button(button_frame, text="Sync My Saves", 
                                  command=self.sync_to_shared_folder)
        self.sync_btn.pack(side=tk.LEFT, padx=10)
        
        self.backup_btn = ttk.Button(button_frame, text="Create Local Backup", 
                                    command=self.create_backup)
        self.backup_btn.pack(side=tk.LEFT, padx=10)
    
    def setup_friends_tab(self):
        """Setup the Friends tab"""
        # Friends list section
        list_frame = ttk.LabelFrame(self.friends_tab, text="Download Friend's Saves")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Instructions
        instructions = ttk.Label(list_frame, text="To download a friend's save:\n\n"
                                                 "1. Ask your friend to share their save folder with you\n"
                                                 "2. Click 'Download Friend's Save' to select from available saves\n"
                                                 "3. Choose which save to download and where to place it")
        instructions.pack(pady=20)
        
        # Action buttons
        action_frame = ttk.Frame(self.friends_tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.download_btn = ttk.Button(action_frame, text="Download Friend's Save", 
                                      command=self.download_friend_save)
        self.download_btn.pack(side=tk.LEFT, padx=5)
    
    def setup_settings_tab(self):
        """Setup the Settings tab"""
        settings_frame = ttk.LabelFrame(self.settings_tab, text="Application Settings")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Save directory setting
        ttk.Label(settings_frame, text="Schedule I Save Directory:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=10)
        
        dir_frame = ttk.Frame(settings_frame)
        dir_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=10)
        
        self.save_dir_entry = ttk.Entry(dir_frame, width=50)
        self.save_dir_entry.insert(0, self.config["save_dir"])
        self.save_dir_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_save_dir)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Shared folder setting
        ttk.Label(settings_frame, text="Shared Folder:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)
        
        shared_dir_frame = ttk.Frame(settings_frame)
        shared_dir_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=10)
        
        self.shared_dir_entry = ttk.Entry(shared_dir_frame, width=50)
        if self.config.get("shared_folder"):
            self.shared_dir_entry.insert(0, self.config["shared_folder"])
        self.shared_dir_entry.pack(side=tk.LEFT, padx=5)
        
        browse_shared_btn = ttk.Button(shared_dir_frame, text="Browse", command=self.browse_shared_dir)
        browse_shared_btn.pack(side=tk.LEFT, padx=5)
        
        # Save settings button
        save_btn = ttk.Button(settings_frame, text="Save Settings", command=self.save_settings)
        save_btn.grid(row=3, column=1, sticky=tk.E, padx=5, pady=20)
        
        # Help text
        help_text = ttk.Label(settings_frame, text="Shared Folder: This is where your saves will be stored for sharing.\n"
                                                  "You can use a folder in Dropbox, Google Drive, or any other shared location.")
        help_text.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=5, pady=10)
    
    def browse_save_dir(self):
        """Open directory browser to select save directory"""
        directory = filedialog.askdirectory(initialdir=self.config["save_dir"])
        if directory:
            self.save_dir_entry.delete(0, tk.END)
            self.save_dir_entry.insert(0, directory)
    
    def browse_shared_dir(self):
        """Open directory browser to select shared directory"""
        directory = filedialog.askdirectory(initialdir=self.config.get("shared_folder", os.path.expanduser("~")))
        if directory:
            self.shared_dir_entry.delete(0, tk.END)
            self.shared_dir_entry.insert(0, directory)
    
    def save_settings(self):
        """Save settings from the settings tab"""
        self.config["save_dir"] = self.save_dir_entry.get()
        self.config["shared_folder"] = self.shared_dir_entry.get()
        
        self.save_config()
        self.save_dir_label.config(text=self.config["save_dir"])
        self.shared_folder_label.config(text=self.config.get("shared_folder", "Not configured"))
        
        messagebox.showinfo("Settings", "Settings saved successfully!")
    
    def sync_to_shared_folder(self):
        """Sync local save files to a shared folder"""
        # Check if shared folder is configured
        if not self.config.get("shared_folder"):
            # Ask user to select a shared folder
            shared_folder = filedialog.askdirectory(title="Select a shared folder for syncing saves")
            if not shared_folder:
                return  # User canceled
            
            self.config["shared_folder"] = shared_folder
            self.save_config()
            messagebox.showinfo("Setup", f"Shared folder set to:\n{shared_folder}\n\nYou can share this folder with friends using Dropbox, Google Drive, etc.")
        
        # Check if save directory exists
        if not os.path.exists(self.config["save_dir"]):
            messagebox.showerror("Error", f"Save directory not found: {self.config['save_dir']}")
            return
        
        try:
            # Find user ID folders in the save directory
            user_folders = []
            for item in os.listdir(self.config["save_dir"]):
                if os.path.isdir(os.path.join(self.config["save_dir"], item)):
                    user_folders.append(item)
            
            if not user_folders:
                messagebox.showerror("Error", "No user save folders found")
                return
            
            # If multiple user folders, ask which one to sync
            selected_user_folder = user_folders[0]  # Default to first one
            if len(user_folders) > 1:
                user_select = tk.Toplevel(self.root)
                user_select.title("Select User Folder")
                user_select.geometry("400x300")
                user_select.transient(self.root)
                user_select.grab_set()
                
                ttk.Label(user_select, text="Select which user folder to sync:").pack(pady=10)
                
                # Create a listbox with user folders
                user_listbox = tk.Listbox(user_select, width=50, height=10)
                user_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
                
                for folder in user_folders:
                    user_listbox.insert(tk.END, folder)
                
                # Add scrollbar
                scrollbar = ttk.Scrollbar(user_select, orient=tk.VERTICAL, command=user_listbox.yview)
                user_listbox.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                # Variable to store selection
                selection_made = [False]
                
                def on_select():
                    if not user_listbox.curselection():
                        messagebox.showerror("Error", "Please select a user folder")
                        return
                    
                    nonlocal selected_user_folder
                    selected_user_folder = user_listbox.get(user_listbox.curselection()[0])
                    selection_made[0] = True
                    user_select.destroy()
                
                # Add select button
                select_btn = ttk.Button(user_select, text="Select", command=on_select)
                select_btn.pack(pady=10)
                
                # Wait for selection
                self.root.wait_window(user_select)
                
                if not selection_made[0]:
                    return  # User canceled
            
            # Create a folder for this user in the shared folder
            user_shared_dir = os.path.join(self.config["shared_folder"], "MySaves")
            if not os.path.exists(user_shared_dir):
                os.makedirs(user_shared_dir)
            
            # Create a subfolder for this user ID
            user_id_shared_dir = os.path.join(user_shared_dir, selected_user_folder)
            if not os.path.exists(user_id_shared_dir):
                os.makedirs(user_id_shared_dir)
            
            # Copy all save games from the user folder to the shared folder
            source_user_dir = os.path.join(self.config["save_dir"], selected_user_folder)
            
            # Clear existing files in the shared folder
            for item in os.listdir(user_id_shared_dir):
                item_path = os.path.join(user_id_shared_dir, item)
                if os.path.isfile(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            
            # Copy all save games
            for item in os.listdir(source_user_dir):
                s = os.path.join(source_user_dir, item)
                d = os.path.join(user_id_shared_dir, item)
                if os.path.isfile(s):
                    shutil.copy2(s, d)
                elif os.path.isdir(s):
                    shutil.copytree(s, d)
            
            # Create a metadata file with timestamp
            with open(os.path.join(user_id_shared_dir, "sync_info.txt"), "w") as f:
                f.write(f"Last synced: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"User: {selected_user_folder}\n")
            
            # Update last sync time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.last_sync_label.config(text=current_time)
            
            messagebox.showinfo("Success", f"Save files for user {selected_user_folder} successfully synced to shared folder!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sync to shared folder: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def create_backup(self):
        """Create a local backup of save files"""
        if not os.path.exists(self.config["save_dir"]):
            messagebox.showerror("Error", f"Save directory not found: {self.config['save_dir']}")
            return
        
        backup_dir = os.path.join(self.config_dir, "backups", 
                                 f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        try:
            if not os.path.exists(os.path.dirname(backup_dir)):
                os.makedirs(os.path.dirname(backup_dir))
            
            shutil.copytree(self.config["save_dir"], backup_dir)
            messagebox.showinfo("Backup", f"Backup created successfully at:\n{backup_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
    
    def download_friend_save(self):
        """Download a friend's save from the shared folder"""
        # Check if shared folder is configured
        if not self.config.get("shared_folder"):
            messagebox.showerror("Error", "Shared folder is not configured. Please sync your saves first.")
            return
        
        try:
            # Look for friend folders in the shared folder
            shared_folder = self.config["shared_folder"]
            friend_folders = []
            
            # Check all subfolders in the shared folder
            for item in os.listdir(shared_folder):
                item_path = os.path.join(shared_folder, item)
                if os.path.isdir(item_path) and item != "MySaves":  # Skip our own saves
                    friend_folders.append(item)
            
            if not friend_folders:
                messagebox.showinfo("No Friends Found", 
                                   "No friend save folders found in the shared folder.\n\n"
                                   "Ask your friends to share their save folders with you.")
                return
            
            # Create a dialog to select which friend's saves to use
            friend_select = tk.Toplevel(self.root)
            friend_select.title("Select Friend")
            friend_select.geometry("400x300")
            friend_select.transient(self.root)
            friend_select.grab_set()
            
            ttk.Label(friend_select, text="Select which friend's saves to download:").pack(pady=10)
            
            # Create a listbox with friend folders
            friend_listbox = tk.Listbox(friend_select, width=50, height=10)
            friend_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            for folder in friend_folders:
                friend_listbox.insert(tk.END, folder)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(friend_select, orient=tk.VERTICAL, command=friend_listbox.yview)
            friend_listbox.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Variable to store selection
            selected_friend = [None]
            
            def on_friend_select():
                if not friend_listbox.curselection():
                    messagebox.showerror("Error", "Please select a friend")
                    return
                
                selected_friend[0] = friend_listbox.get(friend_listbox.curselection()[0])
                friend_select.destroy()
            
            # Add select button
            select_btn = ttk.Button(friend_select, text="Select", command=on_friend_select)
            select_btn.pack(pady=10)
            
            # Add cancel button
            cancel_btn = ttk.Button(friend_select, text="Cancel", command=friend_select.destroy)
            cancel_btn.pack(pady=5)
            
            # Wait for selection
            self.root.wait_window(friend_select)
            
            if selected_friend[0] is None:
                return  # User canceled
            
            friend_name = selected_friend[0]
            friend_dir = os.path.join(shared_folder, friend_name)
            
            # Check for user ID folders in the friend's directory
            user_folders = []
            for item in os.listdir(friend_dir):
                if os.path.isdir(os.path.join(friend_dir, item)):
                    user_folders.append(item)
            
            if not user_folders:
                messagebox.showerror("Error", f"No user save folders found for {friend_name}")
                return
            
            # If multiple user folders, ask which one to use
            selected_user_folder = user_folders[0]  # Default to first one
            if len(user_folders) > 1:
                user_select = tk.Toplevel(self.root)
                user_select.title("Select User Folder")
                user_select.geometry("400x300")
                user_select.transient(self.root)
                user_select.grab_set()
                
                ttk.Label(user_select, text=f"Select which user folder to download from {friend_name}:").pack(pady=10)
                
                # Create a listbox with user folders
                user_listbox = tk.Listbox(user_select, width=50, height=10)
                user_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
                
                for folder in user_folders:
                    user_listbox.insert(tk.END, folder)
                
                # Add scrollbar
                scrollbar = ttk.Scrollbar(user_select, orient=tk.VERTICAL, command=user_listbox.yview)
                user_listbox.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                # Variable to store selection
                selection_made = [False]
                
                def on_select():
                    if not user_listbox.curselection():
                        messagebox.showerror("Error", "Please select a user folder")
                        return
                    
                    nonlocal selected_user_folder
                    selected_user_folder = user_listbox.get(user_listbox.curselection()[0])
                    selection_made[0] = True
                    user_select.destroy()
                
                # Add select button
                select_btn = ttk.Button(user_select, text="Select", command=on_select)
                select_btn.pack(pady=10)
                
                # Add cancel button
                cancel_btn = ttk.Button(user_select, text="Cancel", command=user_select.destroy)
                cancel_btn.pack(pady=5)
                
                # Wait for selection
                self.root.wait_window(user_select)
                
                if not selection_made[0]:
                    return  # User canceled
            
            # Now check for save games within the selected user folder
            source_user_dir = os.path.join(friend_dir, selected_user_folder)
            save_games = []
            for item in os.listdir(source_user_dir):
                if os.path.isdir(os.path.join(source_user_dir, item)):
                    save_games.append(item)
            
            if not save_games:
                messagebox.showerror("Error", f"No save games found in user folder {selected_user_folder}")
                return
            
            # Create a dialog to select which save game to download
            save_select = tk.Toplevel(self.root)
            save_select.title(f"Select {friend_name}'s Save Game")
            save_select.geometry("400x300")
            save_select.transient(self.root)
            save_select.grab_set()
            
            ttk.Label(save_select, text=f"Select which save game to download from {friend_name}:").pack(pady=10)
            
            # Create a listbox with save games
            save_listbox = tk.Listbox(save_select, width=50, height=10)
            save_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            for save in save_games:
                save_listbox.insert(tk.END, save)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(save_select, orient=tk.VERTICAL, command=save_listbox.yview)
            save_listbox.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            def on_download():
                if not save_listbox.curselection():
                    messagebox.showerror("Error", "Please select a save game")
                    return
                
                selected_save = save_listbox.get(save_listbox.curselection()[0])
                source_path = os.path.join(source_user_dir, selected_save)
                
                # Ask user if they want to backup their current save
                if messagebox.askyesno("Backup", "Do you want to backup your current save before downloading?"):
                    self.create_backup()
                
                # Check if the user folder exists in the local save directory
                local_user_dir = os.path.join(self.config["save_dir"], selected_user_folder)
                if not os.path.exists(local_user_dir):
                    os.makedirs(local_user_dir)
                
                # Ask where to place the downloaded save
                choice = messagebox.askquestion("Save Location", 
                                               f"Do you want to replace an existing save with {friend_name}'s save?\n\n"
                                               f"Yes: Replace existing save\n"
                                               f"No: Create a new save slot")
                
                if choice == 'yes':
                    # Get list of existing saves
                    existing_saves = []
                    for item in os.listdir(local_user_dir):
                        if os.path.isdir(os.path.join(local_user_dir, item)):
                            existing_saves.append(item)
                    
                    if not existing_saves:
                        messagebox.showinfo("Info", "No existing saves found. Creating a new save slot.")
                        choice = 'no'  # Switch to creating a new save
                    else:
                        # Let user select which save to replace
                        replace_select = tk.Toplevel(self.root)
                        replace_select.title("Select Save to Replace")
                        replace_select.geometry("400x300")
                        replace_select.transient(self.root)
                        replace_select.grab_set()
                        
                        ttk.Label(replace_select, text="Select which save to replace:").pack(pady=10)
                        
                        # Create a listbox with existing saves
                        replace_listbox = tk.Listbox(replace_select, width=50, height=10)
                        replace_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
                        
                        for save in existing_saves:
                            replace_listbox.insert(tk.END, save)
                        
                        # Add scrollbar
                        scrollbar = ttk.Scrollbar(replace_select, orient=tk.VERTICAL, command=replace_listbox.yview)
                        replace_listbox.configure(yscroll=scrollbar.set)
                        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                        
                        # Variable to store selection
                        replace_selection = [None]
                        
                        def on_replace_select():
                            if not replace_listbox.curselection():
                                messagebox.showerror("Error", "Please select a save to replace")
                                return
                            
                            replace_selection[0] = replace_listbox.get(replace_listbox.curselection()[0])
                            replace_select.destroy()
                        
                        # Add select button
                        select_btn = ttk.Button(replace_select, text="Select", command=on_replace_select)
                        select_btn.pack(pady=10)
                        
                        # Add cancel button
                        cancel_btn = ttk.Button(replace_select, text="Cancel", command=replace_select.destroy)
                        cancel_btn.pack(pady=5)
                        
                        # Wait for selection
                        self.root.wait_window(replace_select)
                        
                        if replace_selection[0] is None:
                            return  # User canceled
                        
                        # Replace the selected save
                        try:
                            replace_path = os.path.join(local_user_dir, replace_selection[0])
                            # Remove existing save
                            shutil.rmtree(replace_path)
                            # Copy the downloaded save with the same name
                            shutil.copytree(source_path, replace_path)
                            
                            messagebox.showinfo("Success", 
                                               f"Successfully replaced save {replace_selection[0]} with {friend_name}'s save: {selected_save}")
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to replace save: {str(e)}")
                
                if choice == 'no':
                    # Create a new save slot
                    try:
                        # Find the next available save slot number
                        save_numbers = []
                        for item in os.listdir(local_user_dir):
                            if item.startswith("SaveGame_") and os.path.isdir(os.path.join(local_user_dir, item)):
                                try:
                                    num = int(item.split("_")[1])
                                    save_numbers.append(num)
                                except:
                                    pass
                        
                        next_num = 1
                        if save_numbers:
                            next_num = max(save_numbers) + 1
                        
                        new_save_name = f"SaveGame_{next_num}"
                        new_save_path = os.path.join(local_user_dir, new_save_name)
                        
                        # Copy the downloaded save to the new slot
                        shutil.copytree(source_path, new_save_path)
                        
                        messagebox.showinfo("Success", 
                                           f"Successfully downloaded {friend_name}'s save as a new save slot: {new_save_name}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to create new save slot: {str(e)}")
                
                save_select.destroy()
            
            # Add download button
            download_btn = ttk.Button(save_select, text="Download Selected Save", command=on_download)
            download_btn.pack(pady=10)
            
            # Add cancel button
            cancel_btn = ttk.Button(save_select, text="Cancel", command=save_select.destroy)
            cancel_btn.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download save: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleISyncApp(root)
    root.mainloop()