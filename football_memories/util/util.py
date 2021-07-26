import os
import boto3
from flask import (request)
from flask_paginate import get_page_args
from werkzeug.utils import secure_filename
from datetime import datetime

if os.path.exists("env.py"):
    import env

# AWS S3 variables
s3_bucket_name = "ci-ms3-football-memories"
s3_bucket_url = "https://ci-ms3-football-memories.s3.eu-west-1.amazonaws.com/"
client = boto3.client('s3', 
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

def getMonthAndYear():
    """
    This function returns the current month and year, for example 07,2021
    """
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    return month, year

def generateTimestamp():
    """
    This function generates a timestamp
    """
    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d_%H_%M_%S_")
    return timestamp

def setupPagination():
    """
    This function sets up pagination, so that 3 items can be displayed on a page
    and if there are more than 3 items, pagination will be displayed
    """
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page',
        offset_parameter='offset')
    per_page = 3
    offset = (page - 1) * 3
    return offset, per_page, page


def storeImageAWSS3Bucket(file_to_store):
    """
    This function stores a file in an AWS S3 bucket using boto3
    The filename is in the form timestamp + name of file added by the user
    When the file is succesfully stored in the s3 bucket, then image_url is
    returned
    """
    timestamp = generateTimestamp()
    image = request.files[file_to_store]
    image_file = secure_filename(image.filename)
    image_to_upload = timestamp + image_file
    s3 = boto3.resource('s3')
    s3.Bucket(s3_bucket_name).put_object(Key=image_to_upload, Body=image)
    image_url = s3_bucket_url + image_to_upload
    return image_url