"""
@Author: StrangeParadox
@Description: A simple linker for gitstore, which links the files in the .config file to the $HOME/.config directory
"""

import os
from rich import print
from rich.console import Console
from datetime import datetime

class Main:
    directories = {
        'config': os.path.expanduser('~/.config'),
        'gitstore': os.path.expanduser('~/.gitstore'),
        'gconfig': os.path.expanduser('~/.gitstore/.config'),
        'backup': os.path.expanduser('~/.gitstore/backup')
    }
    
    def __init__(self):
        self.console = Console()
        self.console.clear()
        self.console.log("Starting gitstore linker", style="bold green", justify="center")
        print()

    def ensuree_directories(self):
        for directory in self.directories.values():
            if not os.path.exists(directory):
                os.mkdir(directory)

    def walk(self):
        for root, dirs, files in os.walk(self.directories['gconfig']):
            for file in files:
                # Get the path of the file
                path = os.path.join(root, file)

                # Get the relative path of the file
                relative_path = os.path.relpath(path, self.directories['gconfig'])
                
                # Get the path of the file in the $HOME/.config directory
                home_path = os.path.join(self.directories['config'], relative_path)

                # Check if the file exists in the $HOME/.config directory
                if os.path.exists(home_path):
                    # Check if the file is a symlink
                    if os.path.islink(home_path):
                        # Check if the symlink is pointing to the right file
                        if os.readlink(home_path) == path:
                            print(f"[bold yellow]{relative_path}[/bold yellow] is already linked")
                        else:
                            print(f"[bold red]{relative_path}[/bold red] is already linked to a different file")

                    # Check if the file is a regular file
                    elif os.path.isfile(home_path):
                        # Create a backup of the file
                        backup_path = os.path.join(self.directories['backup'], relative_path)
                        
                        # Ensure the relative path exists
                        os.makedirs(os.path.dirname(backup_path), exist_ok=True)

                        # Get the current date/time
                        now = datetime.now()
                        
                        # Format: Mon-01 Jan 2021 12:00:00
                        date = now.strftime("%a-%d %b %Y %H:%M:%S")

                        # Move the file to the backup directory
                        os.rename(home_path, f"{backup_path} ({date})")
                
                # Create the symlink
                os.symlink(path, home_path)

if __name__ == '__main__':
    m = Main()
    m.walk()