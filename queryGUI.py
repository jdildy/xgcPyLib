import os

def findOutputDiagnostics():
    """
    Lists all .bp files in the current working directory and its subdirectories.

    Returns:
        List[str]: A list of paths to .bp files.
    """
    parent_directory = os.path.dirnam(os.getcwd())
    rundir_path = os.path.join(parent_directory, 'rundir')

    bp_files = []
    
    if os.path.exists(rundir_path):
        for root, dirs, files in os.walk(rundir_path):
            for file in files:
                if file.endswith('.bp'):
                    full_path = os.path.join(root, file)
                    bp_files.append(full_path)

    else: 
        print(f"The 'rundir' directory does not exist at path: {rundir_path}")
    return bp_files

def listOutputDiagnostics():
    """
    Prints the list of .bp files to the terminal.
    """
    bp_files = findOutputDiagnostics()
    
    if bp_files:
        print(f"Found {len(bp_files)} .bp files:")
        for file in bp_files:
            print(file)
    else:
        print("No .bp files found.")

# Example usage
if __name__ == "__main__":
    listOutputDiagnostics()