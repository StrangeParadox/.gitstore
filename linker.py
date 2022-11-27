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

    def ensure_directories(self):
        # Ensure that the directories exist
        for directory in self.directories.values():
            # Check if the directory exists
            if not os.path.exists(directory):
                # Make the directory
                os.makedirs(directory, exist_ok=True)

                # Log the creation of the directory
                print(f"Created directory {directory}", style="bold green")

    def save(self):
        # Save all the files that are not links from .config into .gitstore/.config using walk
        for root, dirs, files in os.walk(self.directories['config']):
            for file in files:
                # Get the full path of the file
                full_path = os.path.join(root, file)

                # Check if the file is a link
                if not os.path.islink(file):
                    # Get the relative path
                    relative_path = os.path.relpath(full_path, self.directories['config'])

                    # Get the backup path
                    backup_path = os.path.join(self.directories['gconfig'], relative_path)

                    # Ensure that the backup path exists
                    os.makedirs(os.path.dirname(backup_path), exist_ok=True)

                    # Copy the file to the backup path
                    os.system(f"cp {full_path} {backup_path}")

                    # Log the backup
                    print(f"Moved [bold green]{full_path} to {backup_path}[/bold green]")

                    # Remove the old file
                    os.remove(full_path)

    def link(self):
        # Walk through the gconfig directory
        for root, dirs, files in os.walk(self.directories['gconfig']):
            for file in files:
                # Get the full path of the file
                full_path = os.path.join(root, file)

                if os.path.islink(full_path):
                    # Check if the link is broken
                    if not os.path.exists(os.readlink(full_path)):
                        # Remove the broken link
                        os.remove(full_path)

                        # Log the removal of the broken link
                        print(f"Removed broken link [bold red]{full_path}[/bold red]")
                    
                    # Read the link and check if it is a link to the config directory
                    elif not os.readlink(full_path) == os.path.relpath(full_path, self.directories['gconfig']):
                        # Alert the user that the link is not a link to the config directory
                        print(f"Link [bold red]{full_path}[/bold red] is not a link to the config directory")

                if os.path.isfile(full_path):
                    # Get the relative path
                    relative_path = os.path.relpath(full_path, self.directories['gconfig'])

                    # Get the link path
                    link_path = os.path.join(self.directories['config'], relative_path)

                    # Ensure that the link path exists
                    os.makedirs(os.path.dirname(link_path), exist_ok=True)

                    # Create the link
                    os.symlink(full_path, link_path)

                    # Log the link
                    print(f"Linked [bold green]{full_path} to {link_path}[/bold green]")


if __name__ == '__main__':
    m = Main()
    m.ensure_directories()
    m.save()
    m.link()