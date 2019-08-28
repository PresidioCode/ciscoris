"""
Class to interface with cisco ucm ris api.
Author: Jeff Levensailor
Version: 0.0.5
Dependencies:
 - zeep: https://python-zeep.readthedocs.io/en/master/

Links:
 - https://developer.cisco.com/docs/sxml/#risport70-api-reference
"""

import sys
import pathlib
import os

from requests import Session 
from requests.auth import HTTPBasicAuth 
import re
import urllib3 
from zeep import Client, Settings, Plugin 
from zeep.transports import Transport 
from zeep.cache import SqliteCache 
from zeep.plugins import HistoryPlugin 
from zeep.exceptions import Fault 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ris(object):
    
    """

    """

    def __init__(self, username, password, cucm, cucm_version):
        """
        :param username: ris username
        :param password: ris password
        :param cucm: UCM IP address
        :param cucm_version: UCM version

        example usage:
        >>> from ris import RIS
        >>> ucm = RIS('ris_user', 'ris_pass', '192.168.200.10', '11.5')
        """
        wsdl = 'https://'+cucm+':8443/realtimeservice2/services/RISService70?wsdl'
        session = Session() 
        session.verify = False 
        session.auth = HTTPBasicAuth(username, password) 
        settings = Settings(strict=False, xml_huge_tree=True) 
        transport = Transport(session=session, timeout=10, cache=SqliteCache()) 
        ris_client = Client(wsdl, settings=settings, transport=transport) 



        self.wsdl = wsdl
        self.username = username
        self.password = password
        self.cucm = cucm
        self.cucm_version = cucm_version
        self.UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
        self.client = ris_client.create_service("{http://schemas.cisco.com/ast/soap}RisBinding", f"https://{cucm}:8443/realtimeservice2/services/RISService70")

    def get_devices(self, **args):
        def parse(registered):
            if registered['CmNodes'] is not None:
                for node in registered.CmNodes:
                    for item in node[1][0].CmDevices:
                        for dev in item[1]:
                            if dev['Status'] == "Registered":
                                return dev
            else: 
                return
        try:
            return self.client.selectCmDeviceExt("", args)['SelectCmDeviceResult']
        except Fault as e:
            return e

    def checkRegistration(self, phones, subs):
        CmSelectionCriteria = {
            "MaxReturnedDevices": "1000",
            "DeviceClass": "Phone",
            "Model": 255,
            "Status": "Registered",
            "NodeName": "",
            "SelectBy": "Name",
            "SelectItems": {
                "item": {
                    "Item": ""
                }
            },
            "Protocol": "Any",
            "DownloadStatus": "Any"
        }
        for sub in subs:
            CmSelectionCriteria['NodeName'] = sub
            CmSelectionCriteria['SelectItems']['item']['Item'] = ",".join(phones)
            reg = self.get_devices(**CmSelectionCriteria)
            return reg