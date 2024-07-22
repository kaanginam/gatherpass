import os 
from azure.storage.blob import ContainerClient
import logging
import json
class AzureBlobSaver:
    def __init__(self, conn_str, container_name):
        
        self.conn_str = conn_str
        
        self.container_client = ContainerClient.from_connection_string(conn_str, container_name)
    def upload(self, directory, upfile, data):
        blob_client = self.container_client.get_blob_client(directory + upfile)
        logging.info("Uploading file")

        blob_client.upload_blob(data.encode(), overwrite=True)
        logging.info("Upload completed")
    def open_from_container(self, container_name, blob):
        return