import json
from pyld import jsonld
from pymods import MODS, FSUDL

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