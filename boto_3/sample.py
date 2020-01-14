import os
import requests

# cwd = os.getcwd()
# print(cwd)
# os.chdir("C:/Users/Gautam/PycharmProjects")
# print(os.getcwd())
# os.chdir(cwd)
# print(os.getcwd())
# environ_variable = os.environ
# modified_time = os.stat("moviedata.json").st_mtime
'''
makedirs - for multiple layers of directories.
mkdir - for single layer
'''

# for root, directories, files in os.walk("C:/Users/Gautam/PycharmProjects/boto_3"):
#     print(root)
#     print(directories)
#     print(files)

# print(os.environ.get('USERPROFILE'))
# ext = os.path.splitext("/user/tst.txt")
# new_path = os.path.join('C:/Users/Gautam/PycharmProjects', "cdk_examples")

from requests.auth import AuthBase


class TokenAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        r.headers['X-TokenAuth'] = f'{self.token}'  # Python 3.6+
        return r


token_auth = TokenAuth('12345abcde-token')

# response.raise_for_status()
# """raises an error if the status is more than 400"""
"""
Make use sessions in order maintain connection for a period of time.
Use retries and timeout for better performance - check real python site
response properties of put, post methods are checked using response.requests.content[ETC]
"""

