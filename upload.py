import google.auth
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Load the Service Account's credentials
SERVICE_ACCOUNT_FILE = 'credential.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Drive API client
service = build('drive', 'v3', credentials=credentials)


def upload_file_to_folder(filename, filepath, mimetype, folder_id):
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File ID: {file.get('id')}")

    # Make the file shareable
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file.get('id'), body=permission, fields='id').execute()

    # Get the shareable link
    link = f"https://drive.google.com/file/d/{file.get('id')}/view?usp=sharing"
    return link


# Example: Upload a file
FOLDER_ID = '1_wjHSlUFazrJh0nWOtPVHTebM7VpaBGg'
file_link = upload_file_to_folder('output.pdf', 'D:\Barcode_airtable\Airtable_barcode\output.pdf', 'application/pdf', FOLDER_ID)
print(f"Shareable link: {file_link}")
