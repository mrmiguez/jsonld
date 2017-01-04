import json
from pyld import jsonld
from pymods import MODS, FSUDL

context = {
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcmitype": "http://purl.org/dc/dcmitype/",
            "dcterms": "http://purl.org/dc/terms/",
            "dpla": "http://dp.la/terms/",
            "edm": "http://www.europeana.eu/schemas/edm/",
            "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
            "lcsh": "http://id.loc.gov/authorities/subjects/",
            "ore": "http://www.openarchives.org/ore/terms/",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "@vocab": "http://purl.org/dc/elements/1.1/",
            "sourceResource": "dpla:SourceResource",
            "aggregatedCHO": {
              "@id": "edm:aggregatedCHO",
              "@type": "@id"
            },
            "collection": {
              "@id": "dcterms:isPartOf",
              "@type": "dcmitype:Collection"
            },
            "extent": "dcterms:extent",
            "temporal": {
              "@id": "dcterms:temporal",
              "@type": "edm:TimeSpan"
            },
            "spatial": {
              "@id": "dcterms:spatial",
              "@type": "dpla:Place"
            },
            "coordinates": "geo:lat_long",
            "city": "dpla:city",
            "county": "dpla:county",
            "region": "dpla:region",
            "state": "dpla:state",
            "country": "dpla:country",
            "stateLocatedIn": "edm:currentLocation",
            "dataProvider": "edm:dataProvider",
            "edmRights": "edm:rights",
            "hasView": {
              "@id": "edm:hasView",
              "@type": "edm:WebResource"
            },
            "intermediateProvider": "dpla:intermediateProvider",
            "isShownAt": {
              "@id": "edm:isShownAt",
              "@type": "@id"
            },
            "object": {
              "@id": "edm:object",
              "@type": "@id"
            },
            "provider": {
              "@id": "edm:provider",
              "@type": "edm:Agent"
            },
            "date": {
              "@type": "edm:TimeSpan"
            },
            "begin": {
              "@id": "edm:begin",
              "@type": "xsd:date"
            },
            "end" : {
              "@id": "edm:end",
              "@type": "xsd:date"
            },
            "displayDate": "skos:prefLabel",
            "name": "skos:prefLabel",
            "iso639": "skos:altLabel",
            "iso639_3": "skos:altLabel",
            "admin": None,
            "id": None,
            "_id": None,
            "ingestionSequence": None,
            "ingestDate": None,
            "ingestType": None,
            "object_status": None,
            "originalRecord": None,
            "score": None,
            "specType": "edm:hasType",
            "valid_after_enrich": None,
            "validation_message": None
          }

testData = MODS('testData/fsu_nap01-1.xml')
docs = []
for record in testData.record_list:
#    print(record) #test trace
    sourceResource = {}
    sourceResource['title'] = MODS.title_constructor(record)[0]
    if MODS.date_constructor(record) is not None:
        date = MODS.date_constructor(record)
        if ' - ' in date:
            sourceResource['date'] = { "displayDate": date, "begin": date[0:4], "end": date[-4:] }
        else:
            sourceResource['date'] = { "displayDate": date, "begin": date, "end": date }
    sourceResource['type'] = MODS.type_of_resource(record)
#    sourceResource['rights'] = #not yet implemented in pymods
    if MODS.subject(record) is not None:
        sourceResource['subject'] = []
        for subject in MODS.subject(record):
#            print(subject) #test trace
            if subject['authority'] is not None:
                if 'lcsh' == subject['authority']:
                    subject_term = ""
                    for child in subject['children']:
                        subject_term = subject_term + '--' + child['term']
                    sourceResource['subject'].append({"@id": subject['valueURI'], "name": subject_term.strip('.,-')})
    docs.append({"sourceResource": sourceResource})

#compacted = jsonld.compact(docs, context)

print(json.dumps(docs, indent=2))

"""
with open('testData/fsu_nap01-1.jsonld', 'w') as jsonOutput:
    docs = []
    for record in testData.record_list:
        sourceRecource = {}
        print(MODS.title_constructor(record)[0])
        docs.append(sourceRecource)
"""