# module that finds all the files in a directory that have a certain extension
# and whose filenames contain a certain string
# and whose filenames indicate they are from a certain year and quarter
# and separates them based on the presence of a certain string in the filename
# and returns a dictionary with the filenames separated into the different categories

import os
import re

def find_files_with_extension(
    directory='O:/STAFFHQ/SYMDATA/Actuarial/Reserving Applications/IBNR Allocation'
    , extension='.xlsb'):
    """
    # Description:
    Finds all the files in a directory that have a certain extension
    and returns a list of the filenames

    # Inputs:
    directory: *str* the directory to search
                default is the directory where the files are stored
    extension: *str* the extension to search for
                default is '.xlsb'

    # Outputs:
    files: *list* a list of the filenames that have the extension

    """
    files = []
    for file in os.listdir(directory):
        if file.endswith(extension):
            files.append(file)
    return files

  # function that takes a list of file paths and returns a list of the filenames
def get_filenames(files):
    """
    # Description:
    Takes a list of file paths and returns a list of the filenames

    # Inputs:
    files: *list* a list of file paths

    # Outputs:
    filenames: *list* a list of the filenames

    # Example:
    files = ['C:/Users/username/Desktop/file1.txt', 'C:/Users/username/Desktop/file2.txt']
    get_filenames(files)
    > ['file1.txt', 'file2.txt']
    """
    filenames = []
    for file in files:
        filenames.append(os.path.basename(file))
    return filenames


def find_cig_files(directory, extension, year, quarter, cig_string, cig_string2):
    """
    # Description:
    Finds all the files in a directory that have a certain extension
    and whose filenames contain a certain string
    and whose filenames indicate they are from a certain year and quarter
    and separates them based on the presence of a certain string in the filename
    and returns a dictionary with the filenames separated into the different categories


    """
    cig_files = {}
    cig_files['cig'] = []
    cig_files['cig2'] = []
    cig_files['other'] = []
    for file