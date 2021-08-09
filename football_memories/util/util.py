import os
import boto3
from botocore.exceptions import ClientError
from flask import (request, flash)
from flask_paginate import get_page_args
from werkzeug.utils import secure_filename
from datetime import datetime
from typing import Tuple

# AWS S3 variables
s3_bucket_name = "ci-ms3-football-memories"
s3_bucket_url = "https://ci-ms3-football-memories.s3.eu-west-1.amazonaws.com/"
client = boto3.client('s3',
                      aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                      aws_secret_access_key=os.environ.get
                      ("AWS_SECRET_ACCESS_KEY"))


def get_month_and_year() -> Tuple[str, str]:
    """
    This function returns the current month and year, for example 07,2021
    :return month, year: current month and year
    """
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    return month, year


def generate_timestamp() -> str:
    """
    This function generates a timestamp
    :return timestamp: Unique timestamp
    """
    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d_%H_%M_%S_")
    return timestamp


def setup_pagination() -> Tuple[int, int, int]:
    """
    This function sets up pagination, so that 3 items can be displayed on
    a page and if there are more than 3 items, pagination will be displayed
    :return offset, per_page, page: Pagination variables
    """
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page',
        offset_parameter='offset')
    per_page = 3
    offset = (page - 1) * 3
    return offset, per_page, page


def store_image_in_aws_s3_bucket(file_to_store: str) -> str:
    """
    This function stores a file in an AWS S3 bucket using boto3
    The filename is in the form timestamp + name of file added by the user
    When the file is successfully stored in the s3 bucket, then image_url is
    returned
    :param file_to_store: Name of file to store in AWS S3 bucket
    :return image_url: Image url of image in AWS S3 bucket
    """
    timestamp = generate_timestamp()
    image = request.files[file_to_store]
    image_file = secure_filename(image.filename)
    image_to_upload = timestamp + image_file
    try:
        s3 = boto3.resource('s3')
        s3.Bucket(s3_bucket_name).put_object(Key=image_to_upload, Body=image)
    except ClientError:
        raise Exception("Exception when uploading the image to AWS S3 bucket")

    image_url = s3_bucket_url + image_to_upload
    return image_url


def is_image_type_allowed(file_name: str) -> Tuple[str, Tuple[str]]:
    """
    This function takes a filename and returns the image type an
    allowed file types of jpg, JPG, png and PNG
    :param file_name: Name of file
    :return image_type, allowed_image_file_types: Image type and list
    of allowed file types
    """
    allowed_image_file_types = ["jpg", "JPG", "png", "PNG"]
    image = request.files[file_name]
    image_type = secure_filename(image.filename).rsplit('.', 1)[1]
    return image_type, allowed_image_file_types
