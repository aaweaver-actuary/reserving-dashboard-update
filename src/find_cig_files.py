"""
# Description:
Module that finds all the CIG files starting in the root directory

"""

# module that finds all the files in a directory that have a certain extension
# and whose filenames contain a certain string
# and whose filenames indicate they are from a certain year and quarter
# and separates them based on the presence of a certain string in the filename
# and returns a dictionary with the filenames separated into the different categories

import os
import pandas as pd


def find_files_with_extension_in_single_folder(
    # input is a directory and a file extension
    directory: str = 'O:/STAFFHQ/SYMDATA/Actuarial/Reserving Applications/IBNR Allocation', extension: str = '.xlsb'

    # output is a list of the filenames that have the extension
) -> list(str):
    """
    # Description:
    Finds all the files in a directory
    that have a certain extension
    and returns a list of the full file paths

    # Inputs:
    directory: *str* the directory to search
                default is the directory where the files are stored
    extension: *str* the extension to search for
                default is '.xlsb'

    # Outputs:
    files: *list* a list of the filenames that have the extension

    """
    # get a list of all the files in the directory
    files = os.listdir(directory)

    # filter the list of files to only include the files with the extension
    files = [file for file in files if file.endswith(extension)]

    # add the directory to the beginning of the file path
    files = [directory + '/' + file for file in files]

    # return the list of files
    return files

# function that finds all the files in a directory that have a certain extension
# starting in the root directory and going through all the subdirectories
# using the find_files_with_extension_in_single_folder function
# and returning a list of the full file paths of the files that have the extension
# in the root directory and all the subdirectories

def find_files_with_extension(
    # input is a root directory and a file extension
    root_directory: str = 'O:/STAFFHQ/SYMDATA/Actuarial/Reserving Applications/IBNR Allocation', extension: str = '.xlsb'

    # output is a list of the filenames that have the extension
) -> list(str):
    """
    # Description:
    Finds all the files in a directory
    that have a certain extension
    starting in the root directory and going through all the subdirectories
    using the find_files_with_extension_in_single_folder function
    and returns a list of the full file paths of the files that have the extension
    in the root directory and all the subdirectories

    # Inputs:
    root_directory: *str* the root directory to search
                    default is the directory where the files are stored
    extension: *str* the extension to search for
                default is '.xlsb'

    # Outputs:
    files: *list* a list of the filenames that have the extension

    """
    # get a list of all the full file paths for all folders in the root directory
    folders = [root_directory + '/' + folder for folder in os.listdir(root_directory)]

    # loop through each folder and keep adding subfolders to the list of folders until there are no more subfolders
    while True:
        
          # get the number of folders before adding the subfolders
          num_folders = len(folders)
  
          # loop through each folder
          for folder in folders:
  
              # if the folder is a directory
              if os.path.isdir(folder):
  
                  # get a list of all the subfolders in the folder
                  subfolders = [folder + '/' + subfolder for subfolder in os.listdir(folder)]

                  # do not include any folders with the word "delete" in the name (not case sensitive)
                  subfolders = [subfolder for subfolder in subfolders if 'delete' not in subfolder.lower()]

                  # same thing with the word "archive" or "older"
                  subfolders = [subfolder for subfolder in subfolders if 'archive' not in subfolder.lower()]
                  subfolders = [subfolder for subfolder in subfolders if 'older' not in subfolder.lower()]
  
                  # append the subfolders to the list of folders
                  folders.extend(subfolders)

          # get the number of folders after adding the subfolders
          num_folders_after = len(folders)

          # if the number of folders before adding the subfolders is the same as the number of folders after adding the subfolders
          # then there are no more subfolders
          if num_folders == num_folders_after:
              break

    # get a list of all the files in each folder that have the extension
    files = []
    for folder in folders:
        files.extend(find_files_with_extension_in_single_folder(folder, extension))

    # return the list of files
    return files


def get_filenames(
    # input is a list of file paths
    files: list

    # output is a list of the filenames
) -> list(str):
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
    # get the base name of the file from the file path
    filenames = []

    # loop through the list of file paths
    for file in files:

        # get the base name of the file from the file path
        filenames.append(os.path.basename(file))

    #
    return filenames

  # function that takes a list of filen paths and returns
  # a pandas dataframe with the file name, the year, and the quarter
  # by first extracting the file name from the file path using
  # the get_filenames function
  # and then extracting the year and quarter from the filename
  # by extracting the year and quarter from the filename
  # year and quarter are in the format '2021Q2' or '3Q2023'
  # year may come before or after the quarter in the filename
  # year is 4 digits and quarter is 1 digit, separated by a Q
  # year and quarter are split into two columns
  #


def get_year_quarter(
    # input is a list of file paths
    file_paths: list

    # output is a pandas dataframe with
    # the file name, the year, and the quarter
) -> pd.DataFrame(str, int, int):
    """
    # Description:
    Takes a list of file paths and returns
    a pandas dataframe with the file name, the year, and the quarter
    by first extracting the file name from the file path using 
    the get_filenames function
    and then extracting the year and quarter from the filename
    by extracting the year and quarter from the filename
    year and quarter are in the format '2021Q2' or '3Q2023'
    year may come before or after the quarter in the filename
    year is 4 digits and quarter is 1 digit, separated by a Q
    year and quarter are split into two columns

    # Inputs:
    file_paths: *list* a list of file paths

    # Outputs:
    df: *pandas dataframe* a dataframe with the file name, the year, and the quarter

    # Example:
    file_paths = ['C:/Users/username/Desktop/file 2021Q1.txt', 'C:/Users/username/Desktop/file 2Q2023.txt']
    get_year_quarter(file_paths)
    > file_name  year  quarter
    > 0  file 2021Q1.txt  2021        1
    > 1  file 2Q2023.txt  2023        2
    """
    filenames = get_filenames(file_paths)
    df = pd.DataFrame(filenames, columns=['file_name'])

    # year may come before or after the quarter in the filename
    # but year is always 4 digits and quarter is always 1 digit
    df['year'] = df['file_name'].str.extract(r'(\d{4})')

    # column 'year' is a string, convert it to an integer
    df['year'] = df['year'].astype(int)

    # quarter may come before or after the year in the filename
    # first try to extract the quarter after the year
    df['quarter'] = df['file_name'].str.extract(r'Q(\d)')

    # if quarter is not found after the year, try to extract the quarter before the year
    df['quarter'] = df['quarter'].fillna(df['file_name'].str.extract(r'(\d)Q'))

    # column 'quarter' is a string, convert it to an integer
    df['quarter'] = df['quarter'].astype(int)

    # return the dataframe
    return df

  # function that takes a data frame with the file name, the year, and the quarter
  # creates an analysis index column that is 4 * year + quarter
  # filters the data frame to only include the files with indices greater than
  # or equal to the filter parameter that defaults to (4*2021 + 4) = 8084
  # for files from 2021Q4 and later
  # returns the filtered data frame
  #


def filter_year_quarter(
    # input is a data frame with
    # the file name, the year, and the quarter
    # and an optional `analysis_idx_filter` parameter
    # that defaults to 8084 for files from 2021Q4 and later
    df: pd.DataFrame(str, int, int), analysis_idx_filter: int = 8084

    # output is a data frame with
    # the file name, the year, and the quarter
    # filtered to only include files with indices
    # greater than or equal to the `analysis_idx_filter` parameter
) -> pd.DataFrame(str, int, int):
    """
    # Description:
    Takes a data frame with the file name, the year, and the quarter
    creates an analysis index column that is 4 * year + quarter
    filters the data frame to only include the files with indices greater than
    or equal to the `analysis_idx_filter` parameter
    that defaults to (4*2021 + 4) = 8084
    for files from 2021Q4 and later
    returns the filtered data frame

    # Inputs:
    df: *pandas dataframe* a dataframe with the file name, the year, and the quarter
    analysis_idx_filter: *int* the analysis index to filter the data frame on
        defaults to 8084 for files from 2021Q4 and later

    # Outputs:
    df: *pandas dataframe* a dataframe with the file name, the year, and the quarter
        filtered to only include files with indices greater than or equal to the filter parameter

    # Example:
    df = pd.DataFrame({'file_name': ['file 2021Q1.txt', 'file 2Q2023.txt'], 'year': [2021, 2023], 'quarter': [1, 2]})
    df
    > file_name  year  quarter
    > 0  file 2021Q1.txt  2021        1
    > 1  file 2Q2023.txt  2023        2

    filter_year_quarter(df)
    > file_name  year  quarter  analysis_index
    > 1  file 2Q2023.txt  2023        2              8086

    """
    # create an analysis index column that is 4 * year + quarter
    df['analysis_index'] = 4 * df['year'] + df['quarter']

    # filter the data frame to only include the files with indices greater than
    # or equal to the filter parameter
    df = df[df['analysis_index'] >= analysis_idx_filter]

    # return the filtered data frame
    return df

  # function that takes a list of file paths and returns
  # a pandas dataframe with the file name, the year, and the quarter
  # by first extracting the file name from the file path using
  # the get_filenames function
  # and then extracting the year and quarter from the filename
  # by extracting the year and quarter from the filename
  # year and quarter are in the format '2021Q2' or '3Q2023'
  # year may come before or after the quarter in the filename
  # year is 4 digits and quarter is 1 digit, separated by
