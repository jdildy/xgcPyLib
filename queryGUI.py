import os

def findOutputDiagnostics():
    """
    Lists all .bp files in the current working directory and its subdirectories.

    Returns:
        List[str]: A list of paths to .bp files.
    """
    parent_directory = os.path.dirname(os.getcwd())
    rundir_path = os.path.join(parent_directory, 'rundir')

    bp_directories = []
    
    if os.path.exists(rundir_path):
        for root, dirs, files in os.walk(rundir_path):
            for dir in dirs:
                if dir.endswith('.bp'):
                    full_path = os.path.basename(root, dir)
                    bp_directories.append(full_path)
    else: 
        print(f"The 'rundir' directory does not exist at path: {rundir_path}")
    return bp_directories

def listOutputDiagnostics():
    """
    Prints the list of .bp files to the terminal.
    """
    bp_directories = findOutputDiagnostics()
    
    if bp_directories:
        print(f"Found {len(bp_directories)} .bp files:")
        for directory in bp_directories:
            print(directory)
    else:
        print("No .bp files found.")

# Example usage
if __name__ == "__main__":
    listOutputDiagnostics()