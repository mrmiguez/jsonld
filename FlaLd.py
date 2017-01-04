import json
from pyld import jsonld
from pymods import MODS, FSUDL

testData = MODS('testData/FSU_WW2_14_0037_08.xml')
docs = []
for record in testData.record_list:
    sourceResource = {}

    # sourceResource.creator

    # sourceResource.date
    if MODS.date_constructor(record) is not None:
        date = MODS.date_constructor(record)
        if ' - ' in date:
            sourceResource['date'] = { "displayDate": date, "begin": date[0:4], "end": date[-4:] }
        else:
            sourceResource['date'] = { "displayDate": date, "begin": date, "end": date }

    # sourceResource.extent

    # sourceResource.format (i.e. Genre)

    # sourceResource.geographic

    # sourceResource.identifier

    # sourceResource.rights
    if len(MODS.rights(record)) > 1:
        sourceResource['rights'] = {"@id": MODS.rights(record)['URI'], "text": MODS.rights(record)['text']}
    else:
        sourceResource['rights'] = MODS.rights(record)['text']

    #sourceResource.subject
    if MODS.subject(record) is not None:
        sourceResource['subject'] = []
        for subject in MODS.subject(record):
            if subject['authority'] is not None:

                # LCSH subjects
                if 'lcsh' == subject['authority']:
                    subject_term = ""
                    for child in subject['children']:
                        subject_term = subject_term + '--' + child['term']
                    sourceResource['subject'].append({"@id": subject['valueURI'], "name": subject_term.strip('.,-')})

                # LCNAF subjects

    # sourceResource.title
    sourceResource['title'] = MODS.title_constructor(record)[0]

    # sourceResource.type
    sourceResource['type'] = MODS.type_of_resource(record)

    docs.append({"@context": "http://api.dp.la/items/context", "sourceResource": sourceResource})

#compacted = jsonld.compact(docs, "http://api.dp.la/items/context")
#expanded = jsonld.expand(docs)

print(json.dumps(docs, indent=2))

""" Unimplemented writer
with open('testData/fsu_nap01-1.jsonld', 'w') as jsonOutput:
    docs = []
    for record in testData.record_list:
        sourceRecource = {}
        print(MODS.title_constructor(record)[0])
        docs.append(sourceRecource)
"""