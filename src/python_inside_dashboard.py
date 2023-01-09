"""
Description:
This script is used to connect to a SharePoint site and get
the HTML content of the site. This script is used to show
how to connect to a SharePoint site from
inside the dashboard. Because the script is running
inside the dashboard, it will use the Windows credentials.
After getting the list of files in the SharePoint folder,
gathers all "output_tbl" sheets from each excel file in
the SP folder

Author: Andy Weaver
"""

# pylint: disable=import-error
# "python.analysis.disabled": ["reportMissingImports"]
# pylint: disable=invalid-name
# module imports:
import itertools
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

# function that takes the list of files and the sharepoint connection
# and returns a list of dataframes from the "output_tbl" sheets in each excel file
def get_dataframes_from_files(
    files: list,
    client_context: office365.sharepoint.client_context.ClientContext
) -> list:
    """
    # Description: 
    This function takes the list of files and the sharepoint connection
    and returns a list of dataframes from the "output_tbl" sheets in each excel file.

    # Parameters: 
        files: list
            this is the list of files in the folder
        client_context: office365.sharepoint.client_context.ClientContext
            this is the connection to the sharepoint site

    # Returns: 
        list
            this is the list of dataframes from the "output_tbl" sheets in each excel file
    """
    # create an empty list to store the dataframes
    dataframes = []
    
    # generate an iterator for the excel files in the folder
    # with file extensions of ".xlsx", ".xlsb", and ".xlsm"
    # using the `itertools` module
    files_in_folder = itertools.chain(
        files.get_by_file_extension('.xlsx'),
        files.get_by_file_extension('.xlsb'),
        files.get_by_file_extension('.xlsm')
    )
      
    # iterate through the excel files
    # reading the "output_tbl" sheet into a dataframe
    # and appending the dataframe to the list of dataframes
    for file in files_in_folder:
        # get the file name
        file_name = file.properties['Name']

        # get the file url
        
        
        # read the "output_tbl" sheet in the excel file
        temp_df = pd.read_excel(
            # the file url
            file.properties['ServerRelativeUrl'],
            
            # the sheet name
            sheet_name='output_tbl',
            
            # the engine to use to read the excel file
            # if the file is an ".xlsb" file, then use the "pyxlsb" engine
            # otherwise, use the "openpyxl" engine
            engine='pyxlsb' if file.properties['Name'].endswith('.xlsb') else "openpyxl"
        )
        
        # append the dataframe to the list of dataframes
        dataframes.append(temp_df)
        
    