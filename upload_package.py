# Python script for uploading package to Python index (PyPI)
# Created on 25.06.2022 by Bartlomiej Duda

import os
import shutil
import subprocess


try:
    shutil.rmtree('./dist')
except FileNotFoundError as error:
    pass

try:
    shutil.rmtree('./ReverseBox.egg-info')
except FileNotFoundError as error:
    pass

try:
    shutil.rmtree('./reversebox/ReverseBox.egg-info')
except FileNotFoundError as error:
    pass

repository_url = os.environ['REPOSITORY_URL']
reversebox_username = os.environ['REVERSEBOX_USERNAME']
reversebox_password = os.environ['REVERSEBOX_PASSWORD']


subprocess.call("python setup.py sdist", shell=True)
subprocess.call(f"twine upload --repository-url {repository_url} dist/*  "
                f"--username {reversebox_username} --password {reversebox_password}", shell=True)
