import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom
import os
import re

import csv2thermoml as C
import dryrun as D #This script creates empty tagfiles, which is better than nothing

#This is a very preliminary script to transforming chemical markup language (CML) documents
#to ThermoML. Since ThermoML provides way more information and has a different data structure,
#a lot of dummy values will be used for the time being.

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

def create_data_entry(cmldata):

    #data_csv, nCompounds, nVariables, varTypes, nDatapoints, nDatapoints_per_entry = preproc_data_entry(data_csv)
    
    print("Creating Data entry")
    
    Elements = []
    empty = [] #used for elements which shall not be filled out
    PureOrMixtureData = Element('PureOrMixtureData')
    
    #Info about the Dataframe
    nPureOrMixtureDataNumber = create_xml_subelement_with_list(PureOrMixtureData,"nPureOrMixtureDataNumber",Elements)
    
    for n in range(2): #CML probably provides only 2 compounds
     
        Component = create_xml_subelement_with_list(PureOrMixtureData,"Component",empty)
        RegNum = create_xml_subelement_with_list(Component,"RegNum",empty)
        nOrgNum = create_xml_subelement_with_list(RegNum,"nOrgNum",Elements)
        nSampleNm = create_xml_subelement_with_list(Component,"nSampleNm",Elements)
    
    
    
    
    eExpPurpose = create_xml_subelement_with_list(PureOrMixtureData,"eExpPurpose",Elements)
    sCompiler = create_xml_subelement_with_list(PureOrMixtureData,"sCompiler",Elements)
    sContributor = create_xml_subelement_with_list(PureOrMixtureData,"sContributor",Elements)
    dateDateAdded = create_xml_subelement_with_list(PureOrMixtureData,"dateDateAdded",Elements)
    
    #Info about the measured property
    Property =  create_xml_subelement_with_list(PureOrMixtureData,"Property",empty)
    nPropNumber =  create_xml_subelement_with_list(Property,"nPropNumber",Elements)
    PropertyMethodID =  create_xml_subelement_with_list(Property,"Property-MethodID",empty)
    PropertyGroup =  create_xml_subelement_with_list(PropertyMethodID,"PropertyGroup",empty) 
    VolumetricProp  =  create_xml_subelement_with_list(PropertyGroup,"VolumetricProp",empty) 
    ePropName  =  create_xml_subelement_with_list(VolumetricProp,"ePropName",Elements) 
    eMethodName  =  create_xml_subelement_with_list(VolumetricProp,"eMethodName",Elements) 
    PropPhaseID =  create_xml_subelement_with_list(Property,"PropPhaseID",empty)
    ePropPhase = create_xml_subelement_with_list(PropPhaseID,"ePropPhase",Elements)
    ePresentation = create_xml_subelement_with_list(Property,"ePresentation",Elements)
    
    #Uncertainty of the property
    CombinedUncertainty = create_xml_subelement_with_list(Property,"CombinedUncertainty",empty)
    nCombUncertAssessNum = create_xml_subelement_with_list(CombinedUncertainty,"nCombUncertAssessNum",Elements)
    sCombUncertEvaluator = create_xml_subelement_with_list(CombinedUncertainty,"sCombUncertEvaluator",Elements)
    eCombUncertEvalMethod = create_xml_subelement_with_list(CombinedUncertainty,"eCombUncertEvalMethod",Elements)
    nCombUncertLevOfConfid = create_xml_subelement_with_list(CombinedUncertainty,"nCombUncertLevOfConfid",Elements)
    
    #Phase info
    PhaseID = create_xml_subelement_with_list(PureOrMixtureData,"PhaseID",empty)
    ePhase = create_xml_subelement_with_list(PhaseID,"ePhase",Elements)
    
    #Constraints
    Constraint = create_xml_subelement_with_list(PureOrMixtureData,"Constraint",empty) 
    nConstraintNumber = create_xml_subelement_with_list(Constraint,"nConstraintNumber",Elements) 
    ConstraintID = create_xml_subelement_with_list(Constraint,"ConstraintID",empty) 
    ConstraintType = create_xml_subelement_with_list(ConstraintID,"ConstraintType",empty) 
    #TODO: Collect all possible constraints, make them applicable if necessary
    ePressure = create_xml_subelement_with_list(ConstraintType,"ePressure",Elements) 
    ConstraintPhaseID = create_xml_subelement_with_list(Constraint,"ConstraintPhaseID",empty)  
    eConstraintPhase = create_xml_subelement_with_list(ConstraintPhaseID,"eConstraintPhase",Elements)  
    nConstraintValue = create_xml_subelement_with_list(Constraint,"nConstraintValue",Elements)
    nConstrDigits = create_xml_subelement_with_list(Constraint,"nConstrDigits",Elements)
    
    #Variable declaration
    for i in range(3):
        Variable = create_xml_subelement_with_list(PureOrMixtureData,"Variable",empty)
        nVarNumber = create_xml_subelement_with_list(Variable,"nVarNumber",Elements)
        nVarNumber.text = str(i+1)
        VariableID = create_xml_subelement_with_list(Variable,"VariableID",empty)
        VariableType = create_xml_subelement_with_list(VariableID,"VariableType",empty)
        if i == 0:
            eTemperature = create_xml_subelement_with_list(VariableType,"eTemperature",Elements)
            eTemperature.text =  "Temperature, K"
        else:
            eComponentComposition = create_xml_subelement_with_list(VariableType,"eComponentComposition",Elements)
            eComponentComposition.text = "Mole fraction"
            #For component composition only: RegNum of compound as reference
            RegNum = create_xml_subelement_with_list(VariableID,"RegNum",empty) 
            nOrgNum = create_xml_subelement_with_list(RegNum,"nOrgNum",Elements) 
        #Phase info again
        VarPhaseID = create_xml_subelement_with_list(Variable,"VarPhaseID",empty)
        eVarPhase = create_xml_subelement_with_list(VarPhaseID,"eVarPhase",Elements)    
        eVarPhase.text = "liquid"

    nDatapoints = len(cmldata)
    
    for i in range(nDatapoints):
        NumValues = create_xml_subelement_with_list(PureOrMixtureData,"NumValues",empty)

        #loops for each variable
        for j in range(3):
            VariableValue = create_xml_subelement_with_list(NumValues,"VariableValue",empty)
            nVarNumber = create_xml_subelement_with_list(VariableValue,"nVarNumber",Elements)
            nVarNumber.text = str(j+1)
            nVarValue = create_xml_subelement_with_list(VariableValue,"nVarValue",Elements)
            nVarValue.text = str(cmldata[i][-j])
            nVarDigits = create_xml_subelement_with_list(VariableValue,"nVarDigits",Elements)
            nVarDigits.text = str(0) #CML provides no significant digits
        
        #once per datapoint add property value
        PropertyValue = create_xml_subelement_with_list(NumValues,"PropertyValue",empty)
        nPropNumber = create_xml_subelement_with_list(PropertyValue,"nPropNumber",Elements)
        nPropNumber.text = str(1)
        nPropValue = create_xml_subelement_with_list(PropertyValue,"nPropValue",Elements)
        nPropValue.text = str(cmldata[i][2])
        nPropDigits = create_xml_subelement_with_list(PropertyValue,"nPropDigits",Elements)
        nPropDigits.text = str(len(cmldata[i][3].split("."))) #CML provides us with significant digits for the measured value
        CombinedUncertainty = create_xml_subelement_with_list(PropertyValue,"CombinedUncertainty",empty)
        nCombUncertAssessNum = create_xml_subelement_with_list(CombinedUncertainty,"nCombUncertAssessNum",Elements)
        nCombUncertAssessNum.text = str(1)
        nCombExpandUncertValue = create_xml_subelement_with_list(CombinedUncertainty,"nCombExpandUncertValue",Elements)
        nCombExpandUncertValue.text = str(0) #Again dummy values
        
    '''
    for i in range(len(data_csv)):
        print(len(Elements))
        print(len(data_csv))
        print(Elements[i])
        #print(data_csv[i][1])
        Elements[i].text = data_csv[i][1]
    '''
    #No looping since all text is entered above
        
    final = prettify(PureOrMixtureData)
    print(final)

    return final[23:]

def create_thermoml(folderpath,cmlfile,cmldata):
    #Declare header and footer
    header = "<!-- Generated by the NIST, Thermodynamics Research Center (http://www.trc.nist.gov) --> \n \
    <!-- This ThermoML file was generated by thermoml converter (https://github.com/Sentexi/thermoml_converter/) --> \n \
<DataReport xmlns=\"http://www.iupac.org/namespaces/ThermoML\" \n \
            xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" \n \
            xsi:schemaLocation=\"http://www.iupac.org/namespaces/ThermoML http://trc.nist.gov/ThermoML.xsd\">"
            
    footer = "</DataReport>"


    #Creates ThermoML Version
    version_info = C.create_version_info()
    
    #Reads Citation info
    #citation_data  = C.csv_reader(os.path.join(folderpath,'Citation_template.csv'))
    #citation , filename = C.create_citation(citation_data)
    citation , filename = D.create_citation("dummy") #using dummy values for now
    #TODO: Add proper citation data from template
    
    #Cycle through all compound templates
    #dir = os.listdir(folderpath)
    #r = re.compile("[c,C]ompound.*\d")
    #compound_list = list(filter(r.match, dir))
    #print(compound_list)
    #TODO: Create proper compound list, maybe from template
    
    '''
    all_compounds = ''
    
    for compound_dir in compound_list:
        compound_data = csv_reader(os.path.join(folderpath,compound_dir))
        compound = create_compound(compound_data)
        
        all_compounds += compound
    '''
    all_compounds = D.create_compound("dummy") #Again dummy values

    '''
    all_datapoints = ''
    
    dir = os.listdir(folderpath)
    r = re.compile("[d,D]ata.*\d")
    data_list = list(filter(r.match, dir))
    print(data_list)
    
    
    for data_dir in data_list:
        datapoint_data = csv_reader(os.path.join(folderpath,data_dir))
        datapoint = create_data_entry(datapoint_data)
        
        all_datapoints += datapoint
    '''
    
    all_datapoints = create_data_entry(cmldata)
    
    final_name = cmlfile.split(".")[0] + "_thermoml.xml"
    
    C.writefile(header + version_info + citation + all_compounds + all_datapoints + footer, final_name)

if __name__ == "__main__":
    tree = ET.parse('CML_exp_sim.xml')
    root = tree.getroot()
    
    cmldata = []
    
    for exp in root[0][0]:
        #print(exp.tag, exp.attrib)
        DOI = exp[0][0][0].text #this is just for consistency, no need to read in the DOI each time
        ID = exp[0][1][0].text #the datapoint number, starts with 1
        val_density = exp[0][2][0] #the solvent density
        val_error = exp[0][3][0] #the corresponsing error
        
        mol_DES = exp[1][0][0].text #the molar ratio of the DES
        mol_water = exp[1][1][0].text #the molar ratio of water
        T = exp[1][2][0].text #temperature in K
        
        cmldata.append([DOI,ID,val_density,str(val_error),mol_DES,mol_water,T]) #eventually this could be a class
        
    create_thermoml("CML","CML_exp_sim.xml",cmldata)
        
    
        
        