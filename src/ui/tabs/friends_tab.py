import tkinter as tk
from tkinter import ttk, messagebox
from utils.github_manager import GitHubManager
from utils.save_manager import SaveManager

class FriendsTab(ttk.Frame):
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        self.config_manager = config_manager
        self.github_manager = GitHubManager(config_manager)
        self.save_manager = SaveManager(config_manager)
        self.setup_ui()

    def setup_ui(self):
        # Add friend section
        self.create_add_friend_frame()
        
        # Friends list section
        self.create_friends_list_frame()
        
        # Action buttons
        self.create_action_frame()
        
        # Populate friends list
        self.update_friends_list()

    def create_add_friend_frame(self):
        add_frame = ttk.LabelFrame(self, text="Add Friend's Repository")
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(add_frame, text="GitHub Repository URL:").grid(row=0, column=0, padx=5, pady=10)
        self.friend_repo_entry = ttk.Entry(add_frame, width=50)
        self.friend_repo_entry.grid(row=0, column=1, padx=5, pady=10)
        
        ttk.Label(add_frame, text="Friend's Name:").grid(row=1, column=0, padx=5, pady=10)
        self.friend_name_entry = ttk.Entry(add_frame, width=50)
        self.friend_name_entry.grid(row=1, column=1, padx=5, pady=10)
        
        add_btn = ttk.Button(add_frame, text="Add Friend", command=self.add_friend)
        add_btn.grid(row=2, column=1, sticky=tk.E, padx=5, pady=10)

    def create_friends_list_frame(self):
        list_frame = ttk.LabelFrame(self, text="Friends' Saves")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for friends list
        columns = ("name", "repo", "last_updated")
        self.friends_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.friends_tree.heading("name", text="Friend's Name")
        self.friends_tree.heading("repo", text="Repository")
        self.friends_tree.heading("last_updated", text="Last Updated")
        
        # Define columns
        self.friends_tree.column("name", width=150)
        self.friends_tree.column("repo", width=300)
        self.friends_tree.column("last_updated", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.friends_tree.yview)
        self.friends_tree.configure(yscroll=scrollbar.set)
        
        # Pack elements
        self.friends_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_action_frame(self):
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.download_btn = ttk.Button(action_frame, text="Download Selected Save", 
                                      command=self.download_friend_save)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        self.remove_friend_btn = ttk.Button(action_frame, text="Remove Friend", 
                                           command=self.remove_friend)
        self.remove_friend_btn.pack(side=tk.LEFT, padx=5)

    def add_friend(self):
        repo_url = self.friend_repo_entry.get()
        friend_name = self.friend_name_entry.get()
        
        if not repo_url or not friend_name:
            messagebox.showerror("Error", "Both repository URL and friend name are required")
            return
        
        # Add friend to config
        friend_info = {
            "name": friend_name,
            "repo": repo_url,
            "last_updated": "Never"
        }
        
        self.config_manager.config["friends"].append(friend_info)
        self.config_manager.save_config()
        
        # Clear entry fields
        self.friend_repo_entry.delete(0, tk.END)
        self.friend_name_entry.delete(0, tk.END)
        
        # Update friends list
        self.update_friends_list()
        messagebox.showinfo("Friend Added", f"Added {friend_name}'s repository successfully")

    def update_friends_list(self):
        # Clear existing items
        for item in self.friends_tree.get_children():
            self.friends_tree.delete(item)
        
        # Add friends from config
        for friend in self.config_manager.config["friends"]:
            self.friends_tree.insert("", tk.END, values=(
                friend["name"],
                friend["repo"],
                friend["last_updated"]
            ))

    def download_friend_save(self):
        selected = self.friends_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a friend's save to download")
            return
        
        # Get selected friend info
        item = self.friends_tree.item(selected[0])
        friend_name = item["values"][0]
        friend_repo = item["values"][1]
        
        try:
            # TODO: Implement download functionality
            messagebox.showinfo("Download", f"Downloading save from {friend_name}'s repository...")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download save: {str(e)}")

    def remove_friend(self):
        selected = self.friends_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a friend to remove")
            return
        
        # Get selected friend info
        item = self.friends_tree.item(selected[0])
        friend_name = item["values"][0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove {friend_name}?"):
            # Remove friend from config
            self.config_manager.config["friends"] = [
                friend for friend in self.config_manager.config["friends"]
                if friend["name"] != friend_name
            ]
            self.config_manager.save_config()
            self.update_friends_list()
            messagebox.showinfo("Friend Removed", f"Removed {friend_name} successfully") 