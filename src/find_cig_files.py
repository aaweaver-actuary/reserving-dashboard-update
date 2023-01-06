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
  folders = [root_directory + '/' +
      folder for folder in os.listdir(root_directory)]

  # loop through each folder and keep adding subfolders to the list of folders until there are no more subfolders
  while True:

        # get the number of folders before adding the subfolders
        num_folders = len(folders)

        # loop through each folder
        for folder in folders:

            # if the folder is a directory
            if os.path.isdir(folder):

                # get a list of all the subfolders in the folder
                subfolders = [folder + '/' +
                    subfolder for subfolder in os.listdir(folder)]

                # do not include any folders with the word "delete" in the name (not case sensitive)
                subfolders = [
                    subfolder for subfolder in subfolders if 'delete' not in subfolder.lower()]

                # same thing with the word "archive" or "older"
                subfolders = [
                    subfolder for subfolder in subfolders if 'archive' not in subfolder.lower()]
                subfolders = [
                    subfolder for subfolder in subfolders if 'older' not in subfolder.lower()]

                # append the subfolders to the list of folders
                folders.extend(subfolders)

        # get the number of folders after adding the subfolders
        num_folders_after = len(folders)

        # if the number of folders before adding the subfolders is the same as the number of folders after adding the subfolders
        # then there are no more subfolders
        if num_folders == num_folders_after:
            break

  # get a list of all the filepaths in each folder that have the extension
  files = []
  for folder in folders:
      files.extend(
          find_files_with_extension_in_single_folder(folder, extension))

  # return the list of files
  return files


def get_filenames(
    # input is a list of file paths
    # and the extension of the files
    files: list, extension: str = '.xlsb'

    # output is a list of the filenames
) -> list(str):
  """
  # Description:
  Takes a list of file paths and the extension of the files
  and returns a list of the filenames with the extension

  # Inputs:
  files: *list* a list of file paths
  extension: *str* the extension of the files
              default is '.xlsb'

  # Outputs:
  filenames: *list* a list of the filenames having the extension


  # Example:
  files = ['O:/2019/2019 Q1/test 2019Q1.xlsb',
      'O:/2019/2019 Q2/test 2Q2020.xlsb']
  extension = '.xlsb'
  get_filenames(files, extension)
  ['test 2019Q1.xlsb', 'test 2Q2020.xlsb']
  """
  # get the base name of the file from the file path
  filenames = []

  # loop through the list of file paths
  for file in files:

      # get the base name of the file from the file path
      filenames.append(os.path.basename(file))

  # return the list of filenames
  return filenames


def get_year_quarter(
    # input is a list of file paths and a file extension
    file_paths: list, extension: str = '.xlsb'

    # output is a pandas dataframe with
    # the file path, the file name, the year, and the quarter
) -> pd.DataFrame(str, str, int, int):
  """
  # Description:
  Takes a list of file paths and returns
  a pandas dataframe with the file path, the file name, the year, and the quarter
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
  df: *pandas dataframe* a dataframe with the file path, file name, the year, and the quarter

  # Example:
  files = ['O:/2019/2019 Q1/test 2019Q1.xlsb',
      'O:/2019/2019 Q2/test 2Q2020.xlsb', 'O:/2019/2019 Q2/test 4Q2023.xlsx']
  extension = '.xlsb'
  print(get_year_quarter(files, extension))
                            file_path         file_name  year  quarter
  0  O:/2019/2019 Q1/test 2019Q1.xlsb  test 2019Q1.xlsb  2019        1
  1  O:/2019/2019 Q2/test 2Q2020.xlsb  test 2Q2020.xlsb  2020        2
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


def filter_year_quarter(
    # input is a data frame with
    # the file path, the file name, the year, and the quarter
    # and an optional `analysis_idx_filter` parameter
    # that defaults to (2021 * 4 + 4) for 2021Q4
    df: pd.DataFrame(str, str, int, int), analysis_idx_filter: int = (2021 * 4 + 4)

    # output is a data frame with
    # the file path, the file name, the year, and the quarter
    # and the analysis index
    # filtered to only include files with indices
    # greater than or equal to the `analysis_idx_filter` parameter
) -> pd.DataFrame(str, str, int, int, int):
  """
  # Description:
  Takes a data frame with the file path, the file name, the year, and the quarter
  and an optional `analysis_idx_filter` parameter
  that defaults to (2021 * 4 + 4) for 2021Q4
  and returns a data frame with the file path, the file name, the year, and the quarter
  filtered to only include files with indices
  greater than or equal to the `analysis_idx_filter` parameter

  # Inputs:
  df: *pandas dataframe* a dataframe with the file path, file name, the year, and the quarter
  analysis_idx_filter: *int* the index to filter the dataframe
      default is (2021 * 4 + 4) for 2021Q4

  # Outputs:
  df: *pandas dataframe* a dataframe with the file path, file name, the year, and the quarter
      filtered to only include files with indices
      greater than or equal to the `analysis_idx_filter` parameter

  # Example:
  files = ['O:/2019/2019 Q1/test 2019Q1.xlsb', 'O:/2019/2019 Q2/test 2Q2020.xlsb', 'O:/2019/2019 Q2/test 4Q2023.xlsb']
  extension = '.xlsb'
  get_year_quarter(files, extension = extension)
                            file_path         file_name  year  quarter
  0  O:/2019/2019 Q1/test 2019Q1.xlsb  test 2019Q1.xlsb  2019        1
  1  O:/2019/2019 Q2/test 2Q2020.xlsb  test 2Q2020.xlsb  2020        2
  2  O:/2019/2019 Q2/test 4Q2023.xlsb  test 4Q2023.xlsb  2023        4

  filter_year_quarter(get_year_quarter(files, extension = extension)) # default analysis_idx_filter = (2021 * 4 + 4) for 2021Q4
                            file_path         file_name  year  quarter
  0  O:/2019/2019 Q2/test 4Q2023.xlsb  test 4Q2023.xlsb  2023        4

  - does not filter out files with indices less than the `analysis_idx_filter` parameter
  - the first two files have indices less than the `analysis_idx_filter` parameter
  - the third file has an index greater than or equal to the `analysis_idx_filter` parameter
  - the third file is the only file that is returned
  """
  # create a column for the analysis index
  # the analysis index is the year * 4 + the quarter
  # the analysis index is used to filter the dataframe
  # to only include files with indices greater than or equal to the `analysis_idx_filter` parameter
  df['analysis_idx'] = df['year'] * 4 + df['quarter']

  # filter the dataframe to only include files with indices greater than or equal to the `analysis_idx_filter` parameter
  df = df[df['analysis_idx'] >= analysis_idx_filter]

  # return the dataframe
  return df


