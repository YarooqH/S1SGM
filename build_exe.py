import PyInstaller.__main__
import os

# Get the directory containing build_exe.py
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'src/main.py',  # Your main script
    '--name=ScheduleISaveSync',  # Name of the executable
    '--onefile',  # Create a single executable file
    '--windowed',  # Don't show console window when running the executable
    '--icon=assets/icon.ico',  # Optional: Add an icon (you'll need to create/add this)
    '--add-data=README.md;.',  # Optional: Include additional files
    '--clean',  # Clean cache before building
    '--distpath=dist',  # Output directory
    '--workpath=build',  # Work directory
    '--specpath=build',  # Spec file directory
]) 