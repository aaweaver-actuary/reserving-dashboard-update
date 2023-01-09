' this module contains functions and subroutines that support connecting to 
' a Sharepoint folder, downloading files, and uploading files

' first a function that returns a connection to a Sharepoint folder
' this function is called by the other functions in this module
' it is not called directly by the user

' define a global sharepoint connection variable
' this variable is used to connect to, read from, and modify a Sharepoint folder
sp_connection = GetSharepointConnection(SharepointURL, SharepointUsername, SharepointPassword)


' takes a Sharepoint URL and returns a connection to the Sharepoint folder
' the parameter is the URL of the Sharepoint folder, and defaults to
' "http://cinfin.sharepoint.com/sites/PandCReserving"
Private Function  GetSharepointConnection(optional _
    SharepointURL as string = "http://cinfin.sharepoint.com/sites/PandCReserving") as object
    ' this function returns a connection to a Sharepoint folder
    ' it is called by the other functions in this module
    ' it is not called directly by the user
    ' the function takes one argument
    ' SharepointURL: the URL of the Sharepoint folder

    ' the function returns an object that can be used to connect to the 
    ' Sharepoint folder
    ' the function is based on the following article:
    ' http://www.eggheadcafe.com 

    Set SharepointConnection = CreateObject("Microsoft.XMLHTTP")

    ' get the windows authentication for the current user:
     

    ' set the credentials using windows authentication:
    ' uses the credentials of the currently signed-in user
    SharepointConnection.SetCredentials "", "", 0
    


    ' SharepointConnection.SetCredentials SharepointUsername, SharepointPassword, 1
    
    SharepointConnection.Open "GET", SharepointURL, False 
    SharepointConnection.send
    Set SharepointConnection = SharepointConnection.ResponseStream

    ' return the connection to the Sharepoint folder
    GetSharepointConnection = SharepointConnection
End Function

    
    ' return the connection to the Sharepoint folder
    GetSharepointConnection = SharepointConnection
End Function
    
