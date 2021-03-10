import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
import os

def create_xml_subelement_with_list(parent,name,list):
    child = SubElement(parent, name)
    list.append(child)
    
    return child
    
def writefile(input):
    with open('output.xml', 'w') as file:
        file.write(input)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def csv_reader(file):
    csv_data = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            csv_data.append(row)
    return csv_data
    
def create_version_info():
    print("Creating version info")
    Versions = Element('Versions')
    nVersionMajor = SubElement(Versions, "nVersionMajor")
    nVersionMajor.text = "2"
    nVersionMinor = SubElement(Versions, "nVersionMinor")
    nVersionMinor.text = "0"
    
    final = prettify(Versions)

    return final
    
def preproc_citation(citation_csv):
    print("Preprocessing citation")
    #Preprocesses csv input, some data mangling and some stuff used twice in ThermoML
    
    #extract author names
    author1 = citation_csv[1][1]
    author2 = citation_csv[2][1]

    #Replace author names with three letter codes
    citation_csv[1][1] = author1[:3]
    citation_csv[2][1] = author2[:3]
    
    #Insert actual author names
    citation_csv.insert(6, ["entry",author1])
    citation_csv.insert(7, ["entry",author2])
    return citation_csv

def create_citation(citation_csv):
    print("Creating citation")
    citation_csv = preproc_citation(citation_csv)
    
    Elements = []
    empty = [] #used for elements which shall not be filled out

    Citation = Element('Citation')
    TRCRefID = create_xml_subelement_with_list(Citation,"TRCRefID",empty)
    
    yrYrPub = create_xml_subelement_with_list(TRCRefID,"yrYrPub",Elements)
    sAuthor1 = create_xml_subelement_with_list(TRCRefID,"sAuthor1",Elements)
    sAuthor2 = create_xml_subelement_with_list(TRCRefID,"sAuthor2",Elements)
    nAuthorn = create_xml_subelement_with_list(TRCRefID,"nAuthorn",Elements)
    
    eType = create_xml_subelement_with_list(Citation,"eType",Elements)
    eSourceType = create_xml_subelement_with_list(Citation,"eSourceType",Elements)
    sAuthor = create_xml_subelement_with_list(Citation,"sAuthor",Elements)
    sAuthor = create_xml_subelement_with_list(Citation,"sAuthor",Elements)
    sPubName = create_xml_subelement_with_list(Citation,"sPubName",Elements)
    yrPubYr = create_xml_subelement_with_list(Citation,"yrPubYr",Elements)
    dateCit = create_xml_subelement_with_list(Citation,"dateCit",Elements)
    sTitle = create_xml_subelement_with_list(Citation,"sTitle",Elements)
    sAbstract = create_xml_subelement_with_list(Citation,"sAbstract",Elements)
    sDOI = create_xml_subelement_with_list(Citation,"sDOI",Elements)
    sIDNum = create_xml_subelement_with_list(Citation,"sIDNum",Elements)
    sVol = create_xml_subelement_with_list(Citation,"sVol",Elements)
    sPage = create_xml_subelement_with_list(Citation,"sPage",Elements)
    
    for i in range(len(citation_csv)):
        Elements[i].text = citation_csv[i][1]
        
    final = prettify(Citation)

    return final[23:]
    
def preproc_compound(compound_csv):
    print("Preprocessing compound")
    
    #we need to extract the common names
    #-2 because the first is the documentation and the second is the first common name
    ncommon_names = len(compound_csv[3])-2
    common_names = compound_csv[3]
    
    #same for number of samples
    #TODO: Find a description for samples AND purification steps
    nsamples = 1

    for i in range(ncommon_names):
        compound_csv.insert(3,["common_name_entry",common_names[i+2]])
    
    return compound_csv , ncommon_names, nsamples
        
def create_compound(compound_csv):
    compound_csv , ncommon_names, nsamples = preproc_compound(compound_csv)
    print("Creating compound")
    
    Elements = []
    empty = [] #used for elements which shall not be filled out
    Compound = Element('Compound')
    RegNum = create_xml_subelement_with_list(Compound,"RegNum",empty)
    
    nOrgNum = create_xml_subelement_with_list(RegNum,"nOrgNum",Elements)
    
    sStandardInChI = create_xml_subelement_with_list(Compound,"sStandardInChI",Elements)
    sStandardInChIKey = create_xml_subelement_with_list(Compound,"sStandardInChIKey",Elements)
    
    #create designated amount of common name tags
    for i in range(ncommon_names):
        sCommonName = create_xml_subelement_with_list(Compound,"sCommonName",Elements)
    sSmiles = create_xml_subelement_with_list(Compound,"sSmiles",Elements)
    sFormulaMolec = create_xml_subelement_with_list(Compound,"sFormulaMolec",Elements)
    ion = create_xml_subelement_with_list(Compound,"ion",empty)
    
    nCharge = create_xml_subelement_with_list(ion,"nCharge",Elements)
    
    def create_sample():
        Sample = create_xml_subelement_with_list(Compound,"Sample",empty)
        nSampleNm = create_xml_subelement_with_list(Sample,"nSampleNm",Elements)
        eSource = create_xml_subelement_with_list(Sample,"eSource",Elements)
        purity = create_xml_subelement_with_list(Sample,"purity",Elements)
        
        nStep = create_xml_subelement_with_list(purity,"nStep",Elements)
        nPurityMass = create_xml_subelement_with_list(purity,"nPurityMass",Elements)
        nPurityMassDigits = create_xml_subelement_with_list(purity,"nPurityMassDigits",Elements)
        eAnalMeth = create_xml_subelement_with_list(purity,"eAnalMeth",Elements)
        pass
        
    for i in range(nsamples):
        create_sample()    
        
    for i in range(len(compound_csv)):
        Elements[i].text = compound_csv[i][1]
        
    final = prettify(Compound)
    print(final)

    return final[23:]


    

if __name__ == "__main__":
    version_info = create_version_info()
    citation_data = csv_reader(os.path.join('CSV','Citation_template.csv'))
    citation = create_citation(citation_data)
    #TODO: Cycle through Compounds
    compound_data = csv_reader(os.path.join('CSV','Compound_template.csv'))
    compound = create_compound(compound_data)    
    writefile(version_info + citation + compound)
    
    