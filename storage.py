import datetime
import six

import os
import io

from flask import current_app, send_file
from google.cloud import storage
from werkzeug import secure_filename



def _get_storage_client():
    return storage.Client(
        project=current_app.config['PROJECT_ID'])


def _safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing objects
    in Google Cloud Storage.
    ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
    """
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}.{2}".format(basename, date, extension)


def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    filename = _safe_filename(filename)

    client = _get_storage_client()
    bucket = client.bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url


def download_file(source_blobname, destination_file_name):
    """Downloads a blob from the bucket."""
    
    client = _get_storage_client()
    bucket = client.bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    blob = bucket.blob(source_blobname)

    blob.download_to_filename(destination_file_name)
    print('Blob {} downloaded to {}.'.format(
        source_blobname,
        destination_file_name))

def download_file_from_bucket(url_file):

    url_file_list = url_file.split('/')
    client = _get_storage_client()
    bucket = client.bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    blob = bucket.get_blob(url_file_list[4])

    return send_file(io.BytesIO(blob.download_as_string()), attachment_filename = url_file_list[4], as_attachment=True, mimetype='text/xml')