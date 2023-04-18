import logging
import os
import re

import constants as c
import pandas as pd
import numpy as np
import json
import warnings
from hashlib import sha256
from pathlib import Path
from airflow.decorators import task
warnings.filterwarnings('ignore')


@task
def extraction(filename):
    """
    Created common extraction routine to call from application dataset1 and 2.
    :param filename: application dataset
    :return: json formatted raw data
    """
    file = "".join([c.input_path, filename])
    logging.info("Processing for File, {} ".format(file))
    df = pd.read_csv(file)
    df = df.to_json(orient="records")
    return json.loads(df)


def split_name(input_name):
    """
    Split first and last name by ignoring the salutation list
    :param input_name: name
    :return: first and last name
    """
    names = re.compile(r'\s+').split(input_name)
    if names[0] in c.name_prefix_list:
        del names[0]
    if names[-1] in c.name_suffix_list:
        del names[-1]

    return [names[0], names[-1]] if len(names) >= 2 else ["", input_name.strip()]


def format_date(col):
    date_formats = ["%d/%m/Y", "%m/%d/Y", "%Y/%m/d", "%d %B, %Y", "%d/%m/%Y %H:%M:%S", "%B-%y", "%d %B, %Y"]
    for x in date_formats:
        col = pd.to_datetime(col, errors="ignore", format=f"{x}")

    # To remove errors in the columns like strings or numbers
    col = pd.to_datetime(col, errors="coerce")
    return col


def is_valid_phone_no(phone_no: str):
    """
    Application mobile number is 8 digits
    :param phone_no: phone number
    :return:
    """
    d = len(re.compile(r'\d').findall(phone_no))
    return d == 8


def is_valid_email(email: str):
    """
    Applicant has a valid email (email ends with @emailprovider.com or @emailprovider.net)
    :param email: email
    :return:
    """
    return email.split(".")[-1] in c.valid_email_list


def shahash(dob):

    return "_" + sha256(dob.encode('utf-8')).hexdigest()[:5]


@task
def transformation(data_frame):
    """
    Performs cleansing and transformation of raw data process the applications with valid
        1. mobile number (8)
        2. Age criteria(18)
        3. Valid Emails
    :param data_frame: Extracted data frame from input file
    :return: transformed data frame
    """
    df = pd.json_normalize(data_frame)

    # Remove any rows which do not have a name field (null or "")
    df['name'].replace('', np.nan, inplace=True)
    df.dropna(subset=['name'], inplace=True)

    # As the dataset have prefixes, suffixes like the following, should be removed before processing
    # suffix like PHD, DDS can be ignored as we are splitting by leading elements
    df["first_name"], df["last_name"] = zip(*df['name'].apply(lambda x: split_name(x)))

    # Formatting date to standard format
    df['fmt_date_of_birth'] = format_date(df.date_of_birth)

    # encounter -space in between mobile number , so removing space
    df.mobile_no = df.mobile_no.str.replace(" ", "")

    # validate mobile number has 8 digit
    df["successful_applicant"] = is_valid_phone_no(df.mobile_no)

    logging.info("Applicants with Valid mobile number: {}".format((df[df["successful_applicant"]] == True).count()[1]))

    # Formatting date to standard format
    df_min_age_date = pd.to_datetime(c.min_age_date, format="%Y-%m-%d")

    df["above_18"] = ((df_min_age_date - df.fmt_date_of_birth).astype('<m8[Y]') > c.age_criteria)
    df["successful_applicant"] = (df.successful_applicant & df.above_18)

    logging.info("Applicants with Valid Age limit: {}".format((df[df["successful_applicant"]] == True).count()[1]))

    # Applicant with valid Email Address
    df["successful_applicant"] = (df.successful_applicant & is_valid_email(df['email']))

    logging.info("Applicants with Valid Email:{}".format((df[df["successful_applicant"]] == True).count()[1]))

    df["date_of_birth"] = df["fmt_date_of_birth"].dt.strftime("%Y%m%d")
    df["membership_id"] = df["last_name"] + df['date_of_birth'].apply(lambda x: shahash(x))
    df = df.to_json(orient="records")

    return json.loads(df)


@task
def load(transformed_df, file_name):
    """
    Load the successful and unsuccessful application in respective folders
    :param transformed_df: transformed dataframe
    :param file_name: file name to be stored
    :return: None - > save as csv file
    :return: None - > save as csv file
    """
    df = pd.json_normalize(transformed_df)
    successful_df = df.loc[df['successful_applicant'] == True].loc[:, c.final_col_list]
    failed_df = df.loc[df['successful_applicant'] == False].loc[:, c.final_col_list]

    logging.info("Number of successful Application: {}".format(successful_df.count()[1]))
    logging.info("Number of unsuccessful Application {}".format(failed_df.count()[1]))

    success_path = "".join([c.output_path, c.success_dir])
    failed_path = "".join([c.output_path, c.failed_dir])

    Path(success_path).mkdir(parents=True, exist_ok=True)
    Path(failed_path).mkdir(parents=True, exist_ok=True)

    success_file = "/".join([success_path, file_name])
    successful_df.to_csv(success_file, index=False)

    failed_file = "/".join([failed_path, file_name])
    failed_df.to_csv(failed_file, index=False)


@task
def delete_file(file_name):
    """
    Delete the file after successful operation
    :param file_name: file name to be deleted
    :return:
    """
    if os.path.isfile(file_name):
        os.remove(file_name, )
