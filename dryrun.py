import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
import os
import re

def create_xml_subelement_with_list(parent,name,list):
    child = SubElement(parent, name)
    list.append(child)
    
    return child
    
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_citation(citation_csv):
    print("Creating citation")
    #citation_csv , filename = preproc_citation(citation_csv)
    
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
    
    '''
    for i in range(len(citation_csv)):
        Elements[i].text = citation_csv[i][1]
    '''
        
    final = prettify(Citation)

    return final[23:] , "dummy"

def create_compound(compound_csv):
    #compound_csv , ncommon_names, nsamples = preproc_compound(compound_csv)
    print("Creating compound")
    
    Elements = []
    empty = [] #used for elements which shall not be filled out
    Compound = Element('Compound')
    RegNum = create_xml_subelement_with_list(Compound,"RegNum",empty)
    
    nOrgNum = create_xml_subelement_with_list(RegNum,"nOrgNum",Elements)
    
    sStandardInChI = create_xml_subelement_with_list(Compound,"sStandardInChI",Elements)
    sStandardInChIKey = create_xml_subelement_with_list(Compound,"sStandardInChIKey",Elements)
    
    #create designated amount of common name tags
    for i in range(1):
        sCommonName = create_xml_subelement_with_list(Compound,"sCommonName",Elements)
    sSmiles = create_xml_subelement_with_list(Compound,"sSmiles",Elements)
    sFormulaMolec = create_xml_subelement_with_list(Compound,"sFormulaMolec",Elements)
    ion = create_xml_subelement_with_list(Compound,"ion",empty)
    
    nCharge = create_xml_subelement_with_list(ion,"nCharge",Elements)
    
    def create_sample():
        Sample = create_xml_subelement_with_list(Compound,"Sample",empty)
        nSampleNm = create_xml_subelement_with_list(Sample,"nSampleNm",Elements)
        eSource = create_xml_subelement_with_list(Sample,"eSource",Elements)
        purity = create_xml_subelement_with_list(Sample,"purity",empty)
        
        #TODO loop for each purification step
        nStep = create_xml_subelement_with_list(purity,"nStep",Elements)
        nPurityMass = create_xml_subelement_with_list(purity,"nPurityMass",Elements)
        nPurityMassDigits = create_xml_subelement_with_list(purity,"nPurityMassDigits",Elements)
        eAnalMeth = create_xml_subelement_with_list(purity,"eAnalMeth",Elements)
        pass
        
    for i in range(1):
        create_sample()    
    
    '''    
    for i in range(len(compound_csv)):
        print(Elements[i])
        print(compound_csv[i][1])
        Elements[i].text = compound_csv[i][1]
    '''
        
    final = prettify(Compound)
    print(final)

    return final[23:]