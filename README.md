# AWS IAM User Management Script

**Author:** Wasim

## Overview

This Python script allows you to manage AWS IAM (Identity and Access Management) users. It provides functionality to create , attach policies, list existing users and delete IAM users. The script uses the `boto3` library to interact with AWS services.

## Features

- **Create IAM Users**: Generate a new IAM user with a random password and set up a login profile.
- **Attach Policies**: Attach predefined IAM policies to users.
- **Delete IAM Users**: Remove users, including detaching policies and deleting login profiles.
- **List Users**: Retrieve and list all existing IAM users.

## Prerequisites

- **Python 3**: Ensure you have Python 3 installed.
- **boto3**: AWS SDK for Python. Install it using pip:
  ```bash
  pip install boto3
- **AWS CLI**: Configure your AWS credentials using AWS CLI or environment variables
  ```bash
    aws configure
