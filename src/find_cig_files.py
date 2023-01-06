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


def find_files_with_extension(
    # input is a directory and a file extension
    directory: str = 'O:/STAFFHQ/SYMDATA/Actuarial/Reserving Applications/IBNR Allocation', extension: str = '.xlsb'

    # output is a list of the filenames that have the extension
) -> list(str):
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
    # get a list of all the files in the directory
    files = []

    # loop through the list of files
    for file in os.listdir(directory):

        # if the file has the extension, add it to the list
        if file.endswith(extension):
            files.append(file)

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
