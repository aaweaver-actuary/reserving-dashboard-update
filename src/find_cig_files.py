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
import multiprocessing
import concurrent.futures
import pandas as pd


def find_files_with_extension_in_single_folder(
    # input is a directory and a file extension
    directory: str = 'O:/STAFFHQ/SYMDATA/Actuarial/Reserving Applications/IBNR Allocation', extension: str = '.xlsb'

    # output is a list of the filenames that have the extension
) -> list(str):
    """
    # Description:
    Finds all the files in a directory that have a certain extension
    and returns a list of the full file paths

    # Inputs:
    directory: *str* the directory to search
                default is the directory where the files are stored
    extension: *str* the extension to search for
                default is '.xlsb'

    # Outputs:
    files: *list* a list of the filenames that have the extension
    """
    # Initialize an empty list to store the filenames
    files = []

    # Use os.scandir to iterate over the entries in the directory
    with os.scandir(directory) as entries:

        # Iterate over the entries
        for entry in entries:

            # Check if the entry is a file and has the specified extension
            if entry.is_file() and entry.name.endswith(extension):

                # If it does, append the filename to the list
                files.append(entry.name)

    # Return the list of filenames
    return files


def find_files_with_extension(
    root_directory: str = 'O:/STAFFHQ/SYMDATA/Actuarial/Reserving Applications/IBNR Allocation',
    extension: str = '.xlsb', use_asynchronous: bool = True, use_multiprocessing: bool = True
) -> list(str):
    """
    # Description:
    Finds all the files in a directory that have a certain extension
    starting in the root directory and going through all the subdirectories
    and returns a list of the full file paths of the files that have the extension
    in the root directory and all the subdirectories

    # Inputs:
    root_directory: *str* the root directory to search
                    default is the directory where the files are stored
    extension: *str* the extension to search for
                default is '.xlsb'
    use_asynchronous: *bool* whether to search asynchronously or not
                  default is True
                  If True, uses multiprocessing.Pool.apply_async to run
                  the function asynchronously to each subdirectory
                  If False, uses multiprocessing.Pool.map to run
                  the function synchronously to each subdirectory
    use_multiprocessing: *bool* whether to use multiprocessing or threading
                      default is True
                      If True, uses multiprocessing.Pool
                      to parallelize the search for files
                      If False, uses concurrent.futures.ThreadPoolExecutor
                      to parallelize the search for files

    # Outputs:
    files: *list* a list of the filenames that have the extension

    # Imports:
    multiprocessing
      .Pool()
    concurrent.futures
      .ThreadPoolExecutor()
    os
      .scandir()
      .path.join()
    """

    # Initialize an empty list to store the file paths
    file_paths = []

    # If use_multiprocessing is True, use multiprocessing to parallelize the search for files
    if use_multiprocessing:
      # Use a multiprocessing Pool to parallelize the search for files
      with multiprocessing.Pool() as pool:

        # Use os.scandir to iterate over the entries in the root directory
        with os.scandir(root_directory) as entries:

          # Iterate over the entries
          for entry in entries:

            # If the entry is a file and has the specified extension, append the full file path to the list
            if entry.is_file() and entry.name.endswith(extension):
              file_paths.append(os.path.join(
                  root_directory, entry.name))

            # If the entry is a directory, recursively search through the subdirectory
            elif entry.is_dir():
              file_paths.extend(

                # If use_asynchronous is True, use pool.apply_async to run the function asynchronously to each subdirectory
                if use_asynchronous:
                # Use pool.apply_async to run the function asynchronously to each subdirectory
                pool.apply_async(

                  # The function to run is find_files_with_extension
                  find_files_with_extension
                  , args=(os.path.join(root_directory, entry.name)
                        , extension
                        , use_asynchronous)
                ).get()

                # If use_asynchronous is False, run the function synchronously to each subdirectory
                else:
                # Use pool.map to run the function synchronously to each subdirectory
                pool.map(

                  # The function to run is find_files_with_extension
                  find_files_with_extension
                  , args=(os.path.join(root_directory, entry.name), extension)
                )
              )

    # If use_multiprocessing is False, use threading to parallelize the search for files
    else:
      # Create a ThreadPoolExecutor with the desired number of threads
      with concurrent.futures.ThreadPoolExecutor() as executor:

        # Use os.scandir to iterate over the entries in the root directory
        with os.scandir(root_directory) as entries:

          # Iterate over the entries
          for entry in entries:

            # If the entry is a file and has the specified extension, append the full file path to the list
            if entry.is_file() and entry.name.endswith(extension):
              file_paths.append(os.path.join(
                root_directory, entry.name))

            # If the entry is a directory, recursively search through the subdirectory
            elif entry.is_dir():
              # Submit the function to be run asynchronously to the thread pool
              future = executor.submit(find_files_with_extension, os.path.join(
                root_directory, entry.name), extension)
              # Add the future to a list of futures
              futures.append(future)

          # Iterate over the completed tasks and get the results
          for future in concurrent.futures.as_completed(futures):
            # Append the result of the completed task to the list of file paths
            file_paths.extend(future.result())

    # Return the list of file paths
    return file_paths


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


# get only link ratio filenames from the list of files
# by comparing against an input dataframe of cig filetypes
# called `cig_filetypes` that has the cig filetypes
# that gets filtered to only include cig link ratio file names
# also takes the filtered data frame from the `filter_year_quarter` function
# as input called `df` that gets filtered to only include cig link ratio file names
# the file name is the `stem` from the `filename` column in
# the `cig_filetypes` dataframe plus
# an analysis identifier of the form
# "XQYYYY" where X is the quarter and YYYY is the year
# and the file extension can be any excel file extension
# the form of the filename is: "stem XQYYYY.xlsx"
def get_cig_link_ratio_filenames(
    # input is a data frame with
    # the file path, the file name, the year, and the quarter
    # and a `cig_filetypes` dataframe with columns
    # `filename` and `type`
    # type is the cig filetype that gets filtered to only include
    # 'link ratio' and filename is the file stem for the cig filetype
    df: pd.DataFrame(str, str, int, int, int), cig_filetypes: pd.DataFrame(str, str)

    # output is a data frame with
    # the file path, the file name, the year, and the quarter
    # filtered to only include cig link ratio file names
) -> pd.DataFrame(str, str, int, int, int):
    """
    # Description:
    Takes a data frame with the file path, the file name, the year, and the quarter
    and a `cig_filetypes` dataframe with columns
    `filename` and `type`
    type is the cig filetype that gets filtered to only include 
    'link ratio' and filename is the file stem for the cig filetype
    and returns a data frame with the file path, the file name, the year, and the quarter
    filtered to only include cig link ratio file names

    # Inputs:
    df: *pandas dataframe* a dataframe with the file path, file name, the year, and the quarter
    cig_filetypes: *pandas dataframe* a dataframe with columns
        `filename` and `type`
        type is the cig filetype that gets filtered to only include 
        'link ratio' and filename is the file stem for the cig filetype

    # Outputs:
    df: *pandas dataframe* a dataframe with the file path, file name, the year, and the quarter
        filtered to only include cig link ratio file names

    # Example:
    files = ['O:/2019/2019 Q1/test 2019Q1.xlsb', 'O:/2019/2019 Q2/test 2Q2020.xlsb', 'O:/2019/2019 Q2/test 4Q2023.xlsb']
    extension = '.xlsb'
    cig_filetypes = pd.DataFrame({'filename': ['test'], 'type': ['link ratio']})
    get_cig_link_ratio_filenames(filter_year_quarter(get_year_quarter(files, extension = extension)), cig_filetypes)
                              file_path         file_name  year  quarter
    0  O:/2019/2019 Q2/test 4Q2023.xlsb  test 4Q2023.xlsb  2023        4

    - does not filter out files with indices less than the `analysis_idx_filter` parameter
    - the first two files have indices less than the `analysis_idx_filter` parameter
    - the third file has an index greater than or equal to the `analysis_idx_filter` parameter
    - the third file is the only file that is returned
    """
    # filter cig_filetypes to only include 'link ratio' file types
    cig_filetypes = cig_filetypes[cig_filetypes['type'] == 'link ratio']

    # filter the dataframe to only include cig link ratio file names
    df = df[df['file_name'].str.contains('|'.join(cig_filetypes['filename']))]

    # return the dataframe
    return df
