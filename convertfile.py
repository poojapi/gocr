from os import listdir
from os.path import isfile, join
import os 
import requests
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from apiclient.http import MediaFileUpload
from googleapiclient.discovery import build

class DriveClient(object):
    def connect(self):
        creds = False
        SCOPES = 'https://www.googleapis.com/auth/drive'
        if os.path.exists('token.pickle') and os.path.getsize("token.pickle") > 0:  
            with open('token.pickle', 'rb') as token:
                unpickler = pickle.Unpickler(token)
        # if file is not empty scores will be equal
        # to the value unpickled
                creds = unpickler.load()
    # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                 creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
                
        service = build('drive', 'v3', credentials=creds)
        return service

    def create(self, metadata):
        file = service.files().create(body = metadata).execute()
        return file['id']

    def copy_file(self, service, origin_file_id, copy_title):
        copied_file = {'title': copy_title, "mimeType":"application/vnd.google-apps.document"}
        try:
            return service.files().copy(
            fileId=origin_file_id, body=copied_file).execute()
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None

    def print_file_content(self, service, file_id):
        try:
            request = service.files().export(fileId=file_id, mimeType="text/plain").execute()
            print(request.decode("utf-8"))
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)


filename = "meghadutam.pdf"

burst = "pdfseparate " + filename + " "+ filename[:-4]+"/pg-%04d.pdf"

os.system(burst)

meta = {'name': filename, 'mimeType': 'application/vnd.google-apps.folder'}

client = DriveClient()
service = client.connect()

folder = client.create(meta)

onlyfiles = [f for f in listdir(filename[:-4]) if isfile(join(filename[:-4], f))]

for file in onlyfiles:
	# for file in directory:
	file_metadata = {
	    'name': file[:-4],
	    'mimeType': 'application/vnd.google-apps.document',
	    'parents': [folder]
	}
	media = MediaFileUpload(filename[:-4] + '/' + file,
	                        mimetype='application/pdf',
	                        resumable=True)
	file = service.files().create(body=file_metadata,
	                                    media_body=media,
	                                    ocrLanguage="sa").execute()
	print(file['id'])
#file.SetContentFile(os.path.join('.', 'file-p1-p10.pdf'))

#file = client.copy_file(service, "17HxrK3aH-aLsaQRNpFT4CHlAHyoYhs4-", "zxss")
#client.print_file_content(service, file['id'])