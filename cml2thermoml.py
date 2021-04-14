import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
import os
import re

import csv2thermoml as C
import dryrun as D #This script creates empty tagfiles, which is better than nothing

#This is a very preliminary script to transforming chemical markup language (CML) documents
#to ThermoML. Since ThermoML provides way more information and has a different data structure,
#a lot of dummy values will be used for the time being.

def create_data_entry(data_csv):

    data_csv, nCompounds, nVariables, varTypes, nDatapoints, nDatapoints_per_entry = preproc_data_entry(data_csv)
    
    print("Creating Data entry")
    
    Elements = []
    empty = [] #used for elements which shall not be filled out
    PureOrMixtureData = Element('PureOrMixtureData')
    
    #Info about the Dataframe
    nPureOrMixtureDataNumber = create_xml_subelement_with_list(PureOrMixtureData,"nPureOrMixtureDataNumber",Elements)
    
    for n in range(nCompounds):
     
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
    for i in range(nVariables-1):
        Variable = create_xml_subelement_with_list(PureOrMixtureData,"Variable",empty)
        nVarNumber = create_xml_subelement_with_list(Variable,"nVarNumber",Elements)
        VariableID = create_xml_subelement_with_list(Variable,"VariableID",empty)
        VariableType = create_xml_subelement_with_list(VariableID,"VariableType",empty)
        #TODO: Choose between temperature, composition, or any other ThermoML tags
        print(nVariables)
        if varTypes[i] == "Temperature, K":
            eTemperature = create_xml_subelement_with_list(VariableType,"eTemperature",Elements)
        else:
            eComponentComposition = create_xml_subelement_with_list(VariableType,"eComponentComposition",Elements)
            #For component composition only: RegNum of compound as reference
            RegNum = create_xml_subelement_with_list(VariableID,"RegNum",empty) 
            nOrgNum = create_xml_subelement_with_list(RegNum,"nOrgNum",Elements) 
        #Phase info again
        VarPhaseID = create_xml_subelement_with_list(Variable,"VarPhaseID",empty)
        eVarPhase = create_xml_subelement_with_list(VarPhaseID,"eVarPhase",Elements)    

    
    for i in range(nDatapoints):
        NumValues = create_xml_subelement_with_list(PureOrMixtureData,"NumValues",empty)

        #loops for each variable
        for j in range(nDatapoints_per_entry):
            VariableValue = create_xml_subelement_with_list(NumValues,"VariableValue",empty)
            nVarNumber = create_xml_subelement_with_list(VariableValue,"nVarNumber",Elements)
            nVarValue = create_xml_subelement_with_list(VariableValue,"nVarValue",Elements)
            nVarDigits = create_xml_subelement_with_list(VariableValue,"nVarDigits",Elements)
        
        #once per datapoint add property value
        PropertyValue = create_xml_subelement_with_list(NumValues,"PropertyValue",empty)
        nPropNumber = create_xml_subelement_with_list(PropertyValue,"nPropNumber",Elements)
        nPropValue = create_xml_subelement_with_list(PropertyValue,"nPropValue",Elements)
        nPropDigits = create_xml_subelement_with_list(PropertyValue,"nPropDigits",Elements)
        CombinedUncertainty = create_xml_subelement_with_list(PropertyValue,"CombinedUncertainty",empty)
        nCombUncertAssessNum = create_xml_subelement_with_list(CombinedUncertainty,"nCombUncertAssessNum",Elements)
        nCombExpandUncertValue = create_xml_subelement_with_list(CombinedUncertainty,"nCombExpandUncertValue",Elements)
        
    
    for i in range(len(data_csv)):
        print(len(Elements))
        print(len(data_csv))
        print(Elements[i])
        #print(data_csv[i][1])
        Elements[i].text = data_csv[i][1]
        
    final = prettify(PureOrMixtureData)
    print(final)

    return final[23:]

def create_thermoml(folderpath,cmlfile):
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
    
    all_datapoints = ''
    
    final_name = cmlfile.split(".")[0] + "_thermoml.xml"
    
    C.writefile(header + version_info + citation + all_compounds + all_datapoints + footer, final_name)

if __name__ == "__main__":
    create_thermoml("CML","CML_exp_sim.xml")