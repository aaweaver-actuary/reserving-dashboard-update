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


def get_files_in_folder(
    client_context: office365.sharepoint.client_context.ClientContext,
    folder: str
) -> list:
    """
    # Description: 
    This function takes a sharepoint connection and a string representing a folder,
    and returns the list of files in the folder.

    # Parameters: 
        client_context: office365.sharepoint.client_context.ClientContext
            this is the connection to the sharepoint site
        folder: str
            this is the folder name

    # Returns: 
        list
            this is the list of files in the folder
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
