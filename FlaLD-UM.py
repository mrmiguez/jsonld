import re
import json
from lxml import etree

nameSpace_default = { None: '{http://www.loc.gov/mods/v3}',
                      'oai_dc': '{http://www.openarchives.org/OAI/2.0/oai_dc/}',
                      'dc': '{http://purl.org/dc/elements/1.1/}',
                      'mods': '{http://www.loc.gov/mods/v3}',
                      'dcterms': '{http://purl.org/dc/terms/}',
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

    def simple_lookup(record, elem):
        if record.find('{0}'.format(elem)) is not None:
            results = []
            for item in record.findall('{0}'.format(elem)):
                results.append(item.text)
            return results

    def split_lookup(record, elem, delimiter=';'):
        if record.find('{0}'.format(elem)) is not None:
            results = []
            for item in record.findall('{0}'.format(elem)):
                results.append(item.text.split(delimiter))
            return results

with open('testData/um_um-1.xml') as testData:
    records = OAI_QDC(testData)
    docs = []
    for record in records.record_list:

        if 'deleted' in record.attrib.keys():
            if record.attrib['deleted'] == 'true':
                pass

        else:

            sourceResource = {}

            # sourceResource.alternative
            if OAI_QDC.simple_lookup(record, './/{0}alternative'.format(nameSpace_default['dcterms'])) is not None:
                sourceResource['alternative'] = OAI_QDC.simple_lookup(record, './/{0}alternative'.format(nameSpace_default['dcterms']))

            # sourceResource.collection

            # sourceResource.contributor

            # sourceResource.creator
            if OAI_QDC.simple_lookup(record, './/{0}creator'.format(nameSpace_default['dc'])) is not None:
                sourceResource['creator'] = OAI_QDC.simple_lookup(record, './/{0}creator'.format(nameSpace_default['dc']))

            # sourceResource.date
            if OAI_QDC.simple_lookup(record, './/{0}created'.format(nameSpace_default['dcterms'])) is not None:
                sourceResource['date'] = OAI_QDC.simple_lookup(record, './/{0}created'.format(nameSpace_default['dcterms']))

            # sourceResource.description

            # sourceResource.extent
            if OAI_QDC.simple_lookup(record, './/{0}extent'.format(nameSpace_default['dcterms'])) is not None:
                sourceResource['extent'] = OAI_QDC.simple_lookup(record, './/{0}extent'.format(nameSpace_default['dcterms']))

            # sourceResource.format

            # sourceResource.genre

            # sourceResource.geographic

            # sourceResource.identifier
            if OAI_QDC.simple_lookup(record, './/{0}identifier'.format(nameSpace_default['dc'])) is not None:
                sourceResource['identifier'] = OAI_QDC.simple_lookup(record, './/{0}identifier'.format(nameSpace_default['dc']))

            # sourceResource.language
            if OAI_QDC.simple_lookup(record, './/{0}language'.format(nameSpace_default['dc'])) is not None:
                sourceResource['language'] = { "@id": OAI_QDC.simple_lookup(record, './/{0}language'.format(nameSpace_default['dc'])) }

            # sourceResource.place

            # sourceResource.publisher

            # sourceResource.relation

            # sourceResource.isReplacedBy

            # sourceResource.replaces

            # sourceResource.rights
            rightsURI = re.compile('http://rightsstatements')
            if OAI_QDC.simple_lookup(record, './/{0}rights'.format(nameSpace_default['dc'])) is not None:
                if len(record.findall('.//{0}rights'.format(nameSpace_default['dc']))) > 1:
                    for rights_statement in OAI_QDC.simple_lookup(record, './/{0}rights'.format(nameSpace_default['dc'])):
                        URI = rightsURI.search(rights_statement)
                        if URI:
                            URI_match = URI.string.split(" ")[-1]
                        else:
                            rights_text = rights_statement
                    sourceResource['rights'] = { "@id": URI_match, "text": rights_text }
                else:
                    sourceResource['rights'] = OAI_QDC.simple_lookup(record, './/{0}rights'.format(nameSpace_default['dc']))

            # sourceResource.subject
            if OAI_QDC.simple_lookup(record, './/{0}subject'.format(nameSpace_default['dc'])) is not None:
                sourceResource['subject'] = []
                for element in OAI_QDC.split_lookup(record, './/{0}subject'.format(nameSpace_default['dc'])):
                    for term in element:
                        if len(term) > 0:
                            sourceResource['subject'].append({"name": term.strip(" ") })


            # sourceResource.title
            if OAI_QDC.simple_lookup(record, './/{0}title'.format(nameSpace_default['dc'])) is not None:
                sourceResource['title'] = OAI_QDC.simple_lookup(record, './/{0}title'.format(nameSpace_default['dc']))

            # sourceResource.type
            if OAI_QDC.simple_lookup(record, './/{0}type'.format(nameSpace_default['dc'])) is not None:
                sourceResource['type'] = OAI_QDC.simple_lookup(record, './/{0}type'.format(nameSpace_default['dc']))

            # aggregation.dataProvider
            data_provider = "temp"

            # aggregation.isShownAt

            # aggregation.preview
            preview = "temp"

            # aggregation.provider
            provider = {"name": "TO BE DETERMINED",
                        "@id": "DPLA provides?"}

            docs.append({"@context": "http://api.dp.la/items/context",
                         "sourceResource": sourceResource,
                         "aggregatedCHO": "#sourceResource",
                         "dataProvider": data_provider,
                         "isShownAt": "temp",
                         "preview": preview,
                         "provider": provider})

print(json.dumps(docs, indent=2))