"""
Class to interface with cisco ucm ris api.
Author: Jeff Levensailor
Version: 1.0.0
Dependencies:
 - suds-jurko: https://bitbucket.org/jurko/suds

Links:
 - https://developer.cisco.com/docs/sxml/#risport70-api-reference
"""

import ssl
import urllib

from suds.transport.https import HttpAuthenticated
from suds.client import Client

from suds.xsd.doctor import Import
from suds.xsd.doctor import ImportDoctor


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
        self.username = username
        self.password = password
        self.wsdl = 'https://'+cucm+':8443/realtimeservice2/services/RISService70?wsdl'
        self.cucm = cucm
        self.cucm_version = cucm_version


        tns = 'http://schemas.cisco.com/ast/soap/'
        imp = Import('http://schemas.xmlsoap.org/soap/encoding/', 'http://schemas.xmlsoap.org/soap/encoding/')
        imp.filter.add(tns)

        t = HttpAuthenticated(username=self.username, password=self.password)
        t.handler = urllib.request.HTTPBasicAuthHandler(t.pm)
        
        ssl_def_context = ssl.create_default_context()
        ssl_def_context.check_hostname = False
        ssl_def_context.verify_mode = ssl.CERT_NONE

        t1 = urllib.request.HTTPSHandler(context=ssl_def_context)
        t.urlopener = urllib.request.build_opener(t.handler, t1)

        self.client = Client(self.wsdl, location='https://{0}:8443/realtimeservice2/services/RISService70'.format(cucm), faults=False,
                             plugins=[ImportDoctor(imp)],
                             transport=t)

    def get_devices(self, **args):

        def parse(registered):
            if registered['CmNodes'] is not None:
                for node in registered.CmNodes:
                    for item in node[1][0].CmDevices:
                        for dev in item[1]:
                            if dev['Status'] == "Registered":
                                return dev
            else: return

        resp = self.client.service.selectCmDeviceExt("", args)
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        if resp[0] == 200:
            result['success'] = True
            result['response'] = parse(resp[1]['SelectCmDeviceResult'])
            return result
        else:
            result['response'] = 'Unknown error'
            result['error'] = resp[1].faultstring
            return result

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
            if reg['success']:
                return reg['response']