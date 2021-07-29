import os
import boto3
from botocore.exceptions import NoCredentialsError
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, Blueprint, session, abort)
from flask_paginate import Pagination, get_page_args
from werkzeug.utils import secure_filename
from datetime import datetime

if os.path.exists("env.py"):
    import env

s3_bucket_name = "ci-ms3-football-memories"
s3_bucket_url = "https://ci-ms3-football-memories.s3.eu-west-1.amazonaws.com/"
client = boto3.client('s3', 
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

def getMonthAndYear():
    """
    TBC
    """
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    return month, year

def generateTimestamp():
    """
    TBC
    """
    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d_%H_%M_%S_")
    return timestamp

def setupPagination():
    """
    TBC
    """
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page',
        offset_parameter='offset')
    per_page = 3
    offset = (page - 1) * 3
    return offset, per_page, page


def storeImageAWSS3Bucket(file_to_store):
    """
    TBC
    """
    timestamp = generateTimestamp()
    image = request.files[file_to_store]
    image_file = secure_filename(image.filename)
    image_to_upload = timestamp + image_file
    s3 = boto3.resource('s3')
    s3.Bucket(s3_bucket_name).put_object(Key=image_to_upload, Body=image)
    image_url = s3_bucket_url + image_to_upload
    return image_url

def isAllowedImageFileType(file_name):
    """
    TBC
    """
    allowedImageFileTypes = ["jpg","JPG","png","PNG","gif","GIF"]
    image = request.files[file_name]
    image_type = secure_filename(image.filename).rsplit('.',1)[1]
    return image_type, allowedImageFileTypes