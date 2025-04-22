from github import Github
import os
import git
from datetime import datetime
import shutil
from tkinter import messagebox

class GitHubManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.last_sync_time = "Never"

    def sync_saves(self):
        """Sync local save files to GitHub"""
        temp_dir = None
        try:
            if not self._validate_github_config():
                raise Exception("GitHub settings are not configured. Please check Settings tab.")
            
            if not os.path.exists(self.config_manager.config["save_dir"]):
                raise Exception(f"Save directory not found: {self.config_manager.config['save_dir']}")
            
            # Connect to GitHub
            g = Github(self.config_manager.config["github_token"])
            user = g.get_user()
            
            # Get or create repository
            repo = self._get_or_create_repo(user)
            
            # Create a temporary directory for git operations
            temp_dir = self._setup_temp_dir()
            
            # Initialize git repository
            git_repo = git.Repo.init(temp_dir)
            origin = git_repo.create_remote('origin', 
                repo.clone_url.replace('https://', 
                    f'https://{self.config_manager.config["github_token"]}@'))
            
            # Copy save files and push to GitHub
            self._copy_and_push_saves(git_repo, origin)
            
            self.last_sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        finally:
            # Cleanup
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    print(f"Warning: Could not remove temp directory: {e}")

    def _validate_github_config(self):
        return (self.config_manager.config["github_token"] and 
                self.config_manager.config["github_repo"])

    def _get_or_create_repo(self, user):
        try:
            # First try to get the repo name from the config
            repo_name = self.config_manager.config["github_repo"].split('/')[-1]
            
            # Try to get existing repository
            try:
                repo = user.get_repo(self.config_manager.config["github_repo"])
                print(f"Using existing repository: {repo.full_name}")
                return repo
            except Exception as e:
                print(f"Could not find repository: {e}")
            
            # If repo doesn't exist, create it with a unique name
            count = 0
            while True:
                try:
                    new_repo_name = repo_name if count == 0 else f"{repo_name}-{count}"
                    repo = user.create_repo(
                        new_repo_name,
                        description="Schedule I Save Files",
                        private=True  # Make the repository private by default
                    )
                    
                    # Update config with the new repo name
                    self.config_manager.config["github_repo"] = repo.full_name
                    self.config_manager.save_config()
                    
                    print(f"Created new repository: {repo.full_name}")
                    return repo
                except Exception as e:
                    if "name already exists" in str(e).lower():
                        count += 1
                        continue
                    raise e
        except Exception as e:
            raise Exception(f"Failed to get or create repository: {str(e)}")

    def _setup_temp_dir(self):
        # Use a temp directory in the user's home directory instead
        temp_dir = os.path.join(os.path.expanduser('~'), 'ScheduleISyncTemp')
        if os.path.exists(temp_dir):
            # Make sure we have permissions to remove the old directory
            try:
                shutil.rmtree(temp_dir)
            except PermissionError:
                # If we can't remove it, create a new uniquely named directory
                temp_dir = os.path.join(os.path.expanduser('~'), 
                                      f'ScheduleISyncTemp_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        # Create the new directory
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    def _copy_and_push_saves(self, git_repo, origin):
        # Find user ID folders
        user_folders = [f for f in os.listdir(self.config_manager.config["save_dir"]) 
                       if os.path.isdir(os.path.join(self.config_manager.config["save_dir"], f))]
        
        if not user_folders:
            raise Exception("No user save folders found")
        
        # Copy files to temp directory
        for folder in user_folders:
            src = os.path.join(self.config_manager.config["save_dir"], folder)
            dst = os.path.join(git_repo.working_dir, folder)
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        
        # Commit and push
        git_repo.git.add(A=True)
        commit_message = f"Update save files - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        git_repo.index.commit(commit_message)
        origin.push(refspec='{}:{}'.format('master', 'master')) 