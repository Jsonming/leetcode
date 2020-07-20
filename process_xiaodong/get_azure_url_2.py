from datetime import datetime, timedelta

from azure.storage.blob import generate_blob_sas
from datetime import datetime, timedelta

AZURE_ACC_NAME = 'datamallwangpan'
AZURE_PRIMARY_KEY = "kmz/CvWMaWq9jTG7M2nD8KOrzfc13Z7q4fJe6IygGF3e2JIdNjCu7a4FrsMyBtWr0g5lsM9CjEsjqsBRbSBetw=="
AZURE_CONTAINER = "mycontainer"
AZURE_BLOB = "blobname.txt"
expiry = datetime.utcnow() + timedelta(hours=1)

blobSharedAccessSignature = BlobSharedAccessSignature(AZURE_ACC_NAME, AZURE_PRIMARY_KEY)

sasToken = blobSharedAccessSignature.generate_blob(AZURE_CONTAINER, AZURE_BLOB, expiry=expiry, permission="r")

print(sasToken)
