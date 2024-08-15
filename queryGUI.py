import os
import re


def findTimeSlices(): 

    """
    Searches .bp files by timeslices, denoted by xxxx in file name, i.e xgc.xxxx.bp

    Returns: 
        List[str]: A list of available times slices based on the timeslices in the query search.
    """
    parent = os.path.dirname(os.getcwd())
    rundir = os.path.join(parent, 'rundir')


    bp_timeslices = []
    
    pattern = re.compile(r'\b(?:2d|f2d)\.(\d+)\.bp\b')

    if os.path.exists(rundir):
        for root, dirs, files in os.walk(rundir):
            for dir in dirs: 
                    match = pattern.search(dir)
                    if match:
                        full_path = os.path.join(dir)
                        print(full_path)
                        bp_timeslices.append(full_path)
    else: 
        print(f"The 'rundir' directory does not exist at path: {rundir}\n")
    return bp_timeslices



def listTimeSlices():
    """
    Prints the list of .bp files that include timeslices to the terminal
    """

    bp_timeslices = findTimeSlices()

    if bp_timeslices: 
        print(f"Found {len(bp_timeslices)} time slices")
        for timeslice in bp_timeslices:
            print(timeslice)
    else: 
        print("No timeslices in the .bp files were detected.\n")


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
                    full_path = os.path.join(dir)
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
    print("\n \n \n")
    listTimeSlices()