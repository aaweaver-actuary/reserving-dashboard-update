"""
Description: This script converts a folder of excel files to a parquet file.
The excel files are first read into a list of dataframes, and then the list of dataframes
is converted to a single dataframe, and then the dataframe is converted to a parquet file.

The excel files only include an excel file with the "output_tbl" sheet, and whose
file name does not have the substring "(not analyzed)" in it.
"""

import os
import pandas as pd

# function that takes a file name as input and returns the dataframe from the "output_tbl" sheet in the excel file
# unless the filename has the substring "(not analyzed)" in it, and then it returns None

import office365
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

# function to take a sharepoint connection and a string representing a folder,
# and return the list of files in the folder


def get_sharepoint_connection(
    site_url: str = 'https://cinfin.sharepoint.com/sites/PandCReserving',
    user_email: str = None,
    password: str = None
) -> office365.sharepoint.client_context.ClientContext:
    """
    # Description:
    This function takes a sharepoint site url,
    and returns the connection to the sharepoint site.

    # Parameters:
        site_url: str
            this is the url of the sharepoint site
            defaults to 'https://cinfin.sharepoint.com/sites/PandCReserving'
        user_email: *str*
            this is the email of the user
            defaults to None
        password: *str*
            this is the password of the user
            defaults to None

    # Returns:
        requests.models.Response
            this is the connection to the sharepoint site
    """
    # create an authentication context object
    # this is used to authenticate the user
    auth_ctx = AuthenticationContext(site_url)

    # step 1: determine what credentials to use
    # if the user email and password are None
    if user_email is None and password is None:
        # use the Windows credentials
        # to aquire the token for the user
        # using the office365 module
        auth_ctx.acquire_token_for_user()

    # if the user email and password are not None
    # we use the user email and password to authenticate
    else:
        # first ensure that both the user email and password are not None
        # if only one of the two is None, then raise an error
        if user_email is None and password is not None:
            raise ValueError(
                f'user_email is None, but password is {password}')
        elif user_email is not None and password is None:
            raise ValueError(
                f'password is None, but user_email is {user_email}')
        else:
            pass

        # use the user email and password to authenticate
        # to aquire the token for the user
        # using the office365 module
        auth_ctx.acquire_token_for_user(user_email, password)

    # create a ClientContext object using the authenticated context
    ctx = ClientContext(site_url, auth_ctx)

    # execute a request to verify that the authentication was successful
    # if the authentication was not successful, then this will raise an error
    # if the authentication was successful, then this will return
    # the html content of the sharepoint site
    web = ctx.web  # this is
    ctx.load(web)
    ctx.execute_query()

    # if successful, then the following will print
    if web:
        print("Authenticated as:", web.properties['Title'])
    # if unsuccessful, then the following will print
    else:
        print("Authentication failed.")

    # return the ClientContext object
    return ctx

# returns an iterable of files in the folder


def get_files_in_folder(
    # takes these inputs:
    client_context: office365.sharepoint.client_context.ClientContext,
    folder: str

    # returns an iterable:
) -> list:
    """
    # Description:
    This function takes a sharepoint connection and a string representing a folder,
    and returns an iterable of files in the folder.

    # Parameters:
        client_context: office365.sharepoint.client_context.ClientContext
            this is the connection to the sharepoint site
        folder: str
            this is the folder name

    # Returns:
        list

    """
    # get the web object from the client context
    web = client_context.web

    # get the folder by the server relative url and then get the files in the folder
    files = client_context.web.get_folder_by_server_relative_url(folder).files

    # note that at this point, the `files` object is a `QueryServiceOperation` object,
    # and not a list of files

    # 3. load the files
    # this line is needed because the `files` object is a `QueryServiceOperation` object
    # and so if we don't load the files, then the `files` object will be empty
    client_context.load(files)

    # 4. execute the query
    # we have to perform this step because the `files` object is a `QueryServiceOperation` object
    # and so if we don't execute the query, then the `files` object will be empty
    client_context.execute_query()

    # now that we have executed the query, the `files` object is a list of files
    # return the list of files
    return files


def get_dataframe_from_file(
    file_name: str
) -> pd.DataFrame:
    """
    # Description:
    This function takes a file name as input and returns the dataframe from the "output_tbl" sheet in the excel file
    unless the filename has the substring "(not analyzed)" in it, and then it returns None.

    # Parameters:
        file_name: str
            this is the file name

    # Returns:
        pd.DataFrame
            this is the dataframe from the "output_tbl" sheet in the excel file
    """
    # if the file name has the substring "(not analyzed)" in it
    if "(not analyzed)" in file_name:
        # return None
        return None
    # otherwise
    else:
        # read the "output_tbl" sheet in the excel file
        temp_df = pd.read_excel(
            # the file name
            file_name,

            # the sheet name
            sheet_name='output_tbl',

            # the engine to use to read the excel file
            # if the file is an ".xlsb" file, then use the "pyxlsb" engine
            # otherwise, use the "openpyxl" engine
            engine='pyxlsb' if file_name.endswith('.xlsb') else "openpyxl"
        )

        # return the dataframe
        return temp_df

# function that loops over all files in the current folder, and if they are
# excel files, read them if they have the "output_tbl" sheet and
# do not have the substring "(not analyzed)" in the file name,
# and then return a list of dataframes


def get_dataframes_from_folder() -> list:
    """
    # Description:
    This function loops over all files in the current folder, and if they are
    excel files, read them if they have the "output_tbl" sheet and
    do not have the substring "(not analyzed)" in the file name,
    and then return a single appended dataframe.

    # Parameters:
        None

    # Returns:
        pandas.DataFrame
            this is the dataframe from the "output_tbl" sheets
            in each excel file in the current folder
    """
    # create an empty list to store the dataframes
    dataframes = []

    # iterate over all files in the current folder
    for file_name in os.listdir():
        # get the dataframe from the file
        temp_df = get_dataframe_from_file(file_name)

        # if the dataframe is not None
        if temp_df is not None:
            # append the dataframe to the list of dataframes
            dataframes.append(temp_df)

    # return the list of dataframes
    return dataframes


def get_dataframes_from_sharepoint(
    # sharepoint connection context
    client_context: office365.sharepoint.client_context.ClientContext,

    # the sharepoint folder
    sharepoint_folder: office365.sharepoint.files.file_collection.FileCollection
) -> pd.DataFrame:
    """
    # Description:
    This function takes a list of sharepoint files and reads them in in the same
    way as the `get_dataframes_from_folder` function, and then returns a single
    dataframe that is the result of appending all the dataframes in the list.

    # Parameters:
        client_context: office365.sharepoint.client_context.ClientContext
            this is the sharepoint connection context
        sharepoint_folder: office365.sharepoint.files.file_collection.FileCollection
            this is the sharepoint folder

    # Returns:
        pandas.DataFrame
            this is the dataframe from the "output_tbl" sheets
            in each excel file in the list of sharepoint files
    """
    # create an empty list to store the dataframes
    dataframes = []

    # iterate over all files in the sharepoint folder
    for file in sharepoint_folder:
        # download the file
        file.download(file.properties['Name'])

        # get the dataframe from the file
        temp_df = get_dataframe_from_file(file.properties['Name'])

        # if the dataframe is not None
        if temp_df is not None:
            # append the dataframe to the list of dataframes
            dataframes.append(temp_df)

    # return the list of dataframes
    return dataframes

# function that converts a data frame to parquet and reuploads it to sharepoint
def dataframe_to_parquet_and_upload_to_sharepoint(
    # the dataframe to convert to parquet
    df: pd.DataFrame,

    # sharepoint connection context
    client_context: office365.sharepoint.client_context.ClientContext,

    # the sharepoint folder
    sharepoint_folder: office365.sharepoint.files.file_collection.FileCollection
    
) -> None:
    # make a temp file to upload
    # convert the dataframe to parquet
    df = df.to_parquet("./data.parquet")
        
    # upload the temporary parquet file to sharepoint
    sharepoint_folder.upload_file("./data.parquet")

    # delete the temporary parquet file
    os.remove("./data.parquet")
    
    
    
# function that gets the client context and sharepoint folder
# needed above 
def get_client_context_and_sharepoint_folder(
    # the sharepoint url
    sharepoint_url: str = "https://cinfin.sharepoint.com/sites/PandCReserving",

    # the sharepoint username
    sharepoint_username: str = None,

    # the sharepoint password
    sharepoint_password: str = None,

    # the sharepoint folder
    sharepoint_folder: str
) -> Tuple[office365.sharepoint.client_context.ClientContext, office365.sharepoint.files.file_collection.FileCollection]:
    """
    # Description:
    This function gets the client context and sharepoint folder needed above.
    Uses the `get_sharepoint_folder` function. 
    Uses the `office365` library.
    
    # Parameters: 
        sharepoint_url: str
            this is the sharepoint url
        sharepoint_username: str
            this is the sharepoint username
            
        sharepoint_password: str
            this is the sharepoint password
        sharepoint_folder: str
            this is the sharepoint folder

    # Returns: 
        Tuple[office365.sharepoint.client_context.ClientContext, office365.sharepoint.files.file_collection.FileCollection]
            this is the sharepoint client context and sharepoint folder
    """
    # returns a ClientContext object representing
    # the sharepoint connection
    client_context = get_sharepoint_client_context(
        # the sharepoint url
        sharepoint_url,

        # the sharepoint username
        sharepoint_username,

        # the sharepoint password
        sharepoint_password
    ) 

    # returns a FileCollection object representing
    # the sharepoint folder
    sharepoint_folder = get_sharepoint_folder(
        # the sharepoint client context
        client_context,

        # the sharepoint folder
        sharepoint_folder
    )

    # return the sharepoint client context and sharepoint folder
    return client_context, sharepoint_folder
  
  # function that puts it all together
  # read the data, append it, and upload it to sharepoint
  def folder_to_parquet(
    # sharepoint folder 
    sharepoint_folder: str = "CIG Link Ratio Files"
    
    # the sharepoint url
    sharepoint_url: str = "https://cinfin.sharepoint.com/sites/PandCReserving",

    # the sharepoint username
    sharepoint_username: str = None,

    # the sharepoint password
    sharepoint_password: str = None,

    # the sharepoint folder
    sharepoint_folder_path: str = "Shared Documents/Dashboard Development/"
) -> None:
    """
    # Description:
    This function puts it all together.
    
    # Parameters:
        sharepoint_folder: str
            this is the folder in sharepoint to upload the data to
            under the 
        sharepoint_url: str
            this is the sharepoint url
        sharepoint_username: str
            this is the sharepoint username
            
        sharepoint_password: str
            this is the sharepoint password
        sharepoint_folder_path: str
            this is the sharepoint folder path

    # Returns: 
        None
    """
    # get the client context and sharepoint folder
    client_context, sharepoint_folder = get_client_context_and_sharepoint_folder(
        # the sharepoint url
        sharepoint_url,

        # the sharepoint username
        sharepoint_username,

        # the sharepoint password
        sharepoint_password,

        # the sharepoint folder
        sharepoint_folder
    )
    
    # get the dataframes from the sharepoint folder
    dataframes = get_dataframes_from_sharepoint(
        # the sharepoint client context
        client_context,

        # the sharepoint folder
        sharepoint_folder
    )
    
    # append the dataframes
    df = pd.concat(dataframes)
    
    # convert the dataframe to parquet and upload it to sharepoint
    dataframe_to_parquet_and_upload_to_sharepoint(
        # the dataframe to convert to parquet
        df,

        # the sharepoint client context
        client_context,

        # the sharepoint folder
        sharepoint_folder
    )
    
    # close the sharepoint connection
    client_context.close()
    
    # return None
    return None
