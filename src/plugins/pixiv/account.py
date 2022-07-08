import base64
import json
import requests
import os

from .pixiv_site.get_header import *

path = os.getcwd()

class GetVervfi():
    def __new__(self):
        verifi = GetVervfi.GetVerifiCodeImg()
        return verifi

    def GetVerifiCodeImg():
        url = 'https://pix.ipv4.host/verificationCode'
        headers = get_verification_code_header()
        verifi = requests.get(url, headers=headers).json()
        image_base64 = verifi['data']['imageBase64']
        byte_data = base64.b64decode(image_base64)
        with open(f'{path}/src/plugins/pixiv/tmp.png', 'wb') as f:
            f.write(byte_data)
            f.close()
        return verifi['data']['vid']
