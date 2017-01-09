import json
from lxml import etree

nameSpace_default = { None: '{http://www.loc.gov/mods/v3}',
                      'oai_dc': '{http://www.openarchives.org/OAI/2.0/oai_dc/}',
                      'dc': '{http://purl.org/dc/elements/1.1/}',
                      'mods': '{http://www.loc.gov/mods/v3}',
                      'dcterms': '{http://purl.org/dc/terms}',
                      'xlink': '{http://www.w3.org/1999/xlink}',
                      'repox': '{http://repox.ist.utl.pt}',
                      'oai_qdc': '{http://worldcat.org/xmlschemas/qdc-1.0/}'}

class OAI_QDC:

    def __init__(self, input_file=None):
        """
        General constructor class.
        :param input_file: file or directory of files to be accessed.
        """
        if input_file is not None:
            self.input_file = input_file
            self.tree = etree.parse(self.input_file)
            self.root = self.tree.getroot()

        record_list = []

        if self.root.nsmap is not None:
            self.nsmap = self.root.nsmap

        if 'oai_dc' in self.nsmap:
            for oai_record in self.root.iterfind('.//{0}record'.format(nameSpace_default['oai_dc'])):
                #                record = OAI(oai_record)    # OOP testing
                #                record_list.append(record)  #
                record_list.append(oai_record)  # actually working line
            self.nsroot = 'oai_dc'
            self.set_spec = self.root.find('.//{0}setSpec'.format(nameSpace_default['oai_dc'])).text
            oai_id = self.root.find('.//{0}header/{0}identifier'.format(nameSpace_default['oai_dc'])).text
            oai_urn = ""
            for part in oai_id.split(':')[:-1]:
                oai_urn = oai_urn + ':' + part
            self.oai_urn = oai_urn.strip(':')

        elif 'repox' in self.nsmap:
            for oai_record in self.root.iterfind('.//{0}record'.format(nameSpace_default['repox'])):
                #                record = OAI(oai_record)    # OOP testing
                #                record_list.append(record)  #
                record_list.append(oai_record)  # actually working line
            self.nsroot = 'repox'
            self.set_spec = self.root.attrib['set']
            oai_id = self.root.find('./{0}record'.format(nameSpace_default['repox'])).attrib['id']
            oai_urn = ""
            for part in oai_id.split(':')[:-1]:
                oai_urn = oai_urn + ':' + part
            self.oai_urn = oai_urn.strip(':')

        self.record_list = record_list

with open('testData/um_um-1.xml') as testData:
    records = OAI_QDC(testData)
    print(len(records.record_list))