# This script will link all the files in .config and subdirectories to the ~/.config directory

# This is the directory where the files are stored
CONFIG_DIR="$HOME/.config"

# This is the directory where the files are stored
GITSTORE_DIR="$HOME/.gitstore"

# Get all the files in the .config directory
FILES=$(find $GITSTORE_DIR/.config -type f)

# Loop through all the files
for FILE in $FILES; do
    # Create a symlink to the file
    ln -s $FILE $CONFIG_DIR/$(basename $FILE)
done