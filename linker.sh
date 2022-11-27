# This script will link all the files in .config and subdirectories to the ~/.config directory

# This is the directory where the files are stored
CONFIG_DIR="$HOME/.config"

# This is the directory where the files are stored
GITSTORE_DIR="$HOME/.gitstore"

# Get all the files in the .config directory
ENTRIES=$(find $GITSTORE_DIR/.config)

# Loop through all the files
for ENTRY in $ENTRIES; do
    # Check if the entry is a file
    if [ -f $ENTRY ]; then
        # Check if the file already exists
        if [ -f $CONFIG_DIR/$ENTRY ]; then
            # Check if the file is a symlink
            if [ -L $CONFIG_DIR/$ENTRY ]; then
                # Remove the symlink
                rm $CONFIG_DIR/$ENTRY
            else
                # Move the file to a backup directory
                mkdir -p $GITSTORE_DIR/.config-backup
                mv $CONFIG_DIR/$ENTRY $GITSTORE_DIR/.config-backup/$ENTRY
            fi
        fi
    fi

    # Check if the entry is a directory
    if [ -d $ENTRY ]; then
        # Remove the .config directory from the path
        DIR=$(echo $ENTRY | sed "s|$GITSTORE_DIR/.config||g")

        # Check if the directory exists
        if [ ! -d $CONFIG_DIR$DIR ]; then
            # Create the directory
            mkdir -p $CONFIG_DIR$DIR
        fi

        # Print creating the directory
        echo "Creating directory: $CONFIG_DIR$DIR"
    fi
done