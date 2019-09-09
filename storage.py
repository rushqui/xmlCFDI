import datetime
import six

import os

from flask import current_app
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


# def create_file(filename, file_content):
#     """Create a file.
#     The retry_params specified in the open call will override the default
#     retry params for this particular file handle.
#     Args:
#       filename: filename.
#     """
#     filename = _safe_filename(filename)
#     bucket = '/' + current_app.config['CLOUD_STORAGE_BUCKET']
#     filename_gcs = bucket + '/' + filename

#     write_retry_params = gcs.RetryParams(backoff_factor=1.1)
#     gcs_file = gcs.open(filename_gcs,
#                         f'w',
#                         content_type='text/xml',
#                         # options={'x-goog-meta-foo': 'foo',
#                         #          'x-goog-meta-bar': 'bar'},
#                         retry_params=write_retry_params)
#     gcs_file.write(file_content)
#     # gcs_file.write('f'*1024*4 + '\n')
#     gcs_file.close()
    
#     return filename