import glob
import json
from FlaLD import FlaLD_DC, FlaLD_MODS, FlaLD_QDC

def write_json_ld(docs):
    with open('testData/all-sample.json', 'a') as jsonOutput:
        json.dump(docs, jsonOutput, indent=2)

for file in glob.glob('testData/*-sample.xml'):
    #print(file) #test
    if 'fiu' in file:
        #print('fiu', file)
        write_json_ld(FlaLD_DC(file)) # write test
        #print(json.dumps(FlaLD_DC(file), indent=2)) # dump test
    elif 'fsu' in file:
        #print('fsu', file)
        write_json_ld(FlaLD_MODS(file))  # write test
    elif 'umiami' in file:
        #print('um', file)
        write_json_ld(FlaLD_QDC(file))  # write test