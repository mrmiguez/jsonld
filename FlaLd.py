import json
from pymods import MODS, FSUDL

"""
# TODO
# -ore:aggregation
# -sourceResource.description
"""

def write_json_ld(docs):
    with open('testData/fsu_nap01-1.json', 'w') as jsonOutput:
        json.dump(docs, jsonOutput, indent=2)


testData = MODS('testData/fsu_nap01-1.xml')
docs = []
for record in testData.record_list:
    sourceResource = {}

    # sourceResource.collection
    if MODS.collection(record) is not None:
        collection = MODS.collection(record)
        sourceResource['collection'] = { "name": collection['title'], "host": collection['location'] }
        if 'url' in collection.keys():
            sourceResource['collection']['_:id'] = collection['url']

    # sourceResource.contributor todo

    # sourceResource.creator
    if MODS.name_constructor(record) is not None:
        sourceResource['creator'] = []
        for name in MODS.name_constructor(record):
            if name['roleText'] == 'Creator':
                if 'valueURI' in name.keys():
                    sourceResource['creator'].append({ "@id": name['valueURI'],
                                                       "name": name['text'] })
                else:
                    sourceResource['creator'].append({ "name": name['text'] })
            elif name['roleCode'] == 'cre':
                if 'valueURI' in name.keys():
                    sourceResource['creator'].append({ "@id": name['valueURI'],
                                                       "name": name['text'] })
                else:
                    sourceResource['creator'].append({ "name": name['text'] })

    # sourceResource.date
    if MODS.date_constructor(record) is not None:
        date = MODS.date_constructor(record)
        if ' - ' in date:
            sourceResource['date'] = { "displayDate": date,
                                       "begin": date[0:4],
                                       "end": date[-4:] }
        else:
            sourceResource['date'] = { "displayDate": date,
                                       "begin": date,
                                       "end": date }

    # sourceResource.description
    if MODS.abstract(record) is not None:
        if len(MODS.abstract(record)) > 1:
            sourceResource['description'] = []
            for description in MODS.abstract(record):
                sourceResource['description'].append(description)
        else:
            sourceResource['description'] = MODS.abstract(record)

    # sourceResource.extent
    if MODS.extent(record) is not None:
        if len(MODS.extent(record)) > 1:
            sourceResource['extent'] = []
            for extent in MODS.extent(record):
                sourceResource['extent'].append(extent)
        else:
            sourceResource['extent'] = MODS.extent(record)[0]

    # sourceResource.format (i.e. Genre)
    if MODS.genre(record) is not None:
        if len(MODS.genre(record)) > 1:
            sourceResource['format'] = []
            for format in MODS.genre(record):
                format_elem = {}
                for key, value in format.items():
                    if 'term' == key:
                        format_elem['name'] = value
                    elif 'valueURI' == key:
                        format_elem['@id'] = value
                sourceResource['format'].append(format_elem)
        else:
            format_elem = {}
            for key, value in MODS.genre(record)[0].items():
                if 'term' == key:
                    format_elem['name'] = value
                elif 'valueURI' == key:
                    format_elem['@id'] = value
            sourceResource['format'] = format_elem



    # sourceResource.geographic todo

    # sourceResource.identifier
    sourceResource['identifier'] = { "@id": FSUDL.purl_search(record),
                                     "text": FSUDL.local_identifier(record) }

    # sourceResource.language
    if MODS.language(record) is not None:
        language_list = []
        for language in MODS.language(record):
            if len(language) > 1:
                language_dict = { "name": language['text'],
                                  "iso_639_3": language['code'] }
            else:
                language_dict = { "name": language['text'] }
            language_list.append(language_dict)
        sourceResource['language'] = language_list

    # sourceResource.rights
    if len(MODS.rights(record)) > 1:
        sourceResource['rights'] = {"@id": MODS.rights(record)['URI'],
                                    "text": MODS.rights(record)['text']}
    else:
        sourceResource['rights'] = MODS.rights(record)['text']

    #sourceResource.subject
    if MODS.subject(record) is not None:
        sourceResource['subject'] = []
        for subject in MODS.subject(record):
            if 'authority' in subject.keys():

                # LCSH subjects
                if 'lcsh' == subject['authority']:
                    subject_term = ""
                    for child in subject['children']:
                        subject_term = subject_term + '--' + child['term']
                    sourceResource['subject'].append({"@id": subject['valueURI'],
                                                      "name": subject_term.strip('.,-') })

                # LCNAF subjects
                elif ('naf' or 'lcnaf') == subject['authority']:
                    sourceResource['subject'].append({"@id": subject['valueURI'],
                                                      "name": subject['text'] })

    # sourceResource.title
    sourceResource['title'] = MODS.title_constructor(record)[0]

    # sourceResource.type
    sourceResource['type'] = MODS.type_of_resource(record)

    docs.append({"@context": "http://api.dp.la/items/context",
                 "sourceResource": sourceResource})

#write_json_ld(docs)

print(json.dumps(docs, indent=2))

""" Unimplemented writer
with open('testData/fsu_nap01-1.jsonld', 'w') as jsonOutput:
    docs = []
    for record in testData.record_list:
        sourceResource = {}
        print(MODS.title_constructor(record)[0])
        docs.append(sourceResource)
"""