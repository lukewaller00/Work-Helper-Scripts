from lxml import etree

# Define the Bromcom permissions list you supplied


bromcom_permissions ={
    "Addresses",
    "PersonMedicalConditions",
    "AdministrationDoctorTelephones",
    "PersonMedicalEvents",
    "AssessmentAssociationAssessmentTypes",	
    "PersonParamedicalSupportTypes",
    "AssessmentAssociationSubjects",	
    "PersonPhotos",
    "AssessmentAssociationTerms",	
    "PersonTelephones",
    "AssessmentAssociationYearGroups",
    "PupilPremiums",
    "AssessmentGradeSetGrades",	
    "RoomCovers",
    "AssessmentGradeSets",	
    "Schools",
    "AssessmentGradeSetVersions",	
    "SENStudentNeeds",
    "AssociationAssessmentMarksets",	
    "SENStudents",
    "AssociationAssessmentMarksetVersions",	
    "Staff",
    "AssociationAssessmentMarksheets",	
    "StaffContracts",
    "AssociationAssessmentResults",	
    "StaffCovers",
    "AssociationAssessmentTemplateColumns",	
    "StudentAdditionalInformation",
    "AssociationAssessmentTemplates",	
    "StudentContacts",
    "Attendances",
    "StudentDetentions",
    "BehaviourEventAdjustments",
    "StudentEnrolments",
    "BehaviourEventCategories",
    "StudentExclusions",
    "BehaviourEventLinks",
    "StudentImportedCTFAssessments",
    "BehaviourEventRecords",
    "StudentLearning",
    "BehaviourEvents",	
    "StudentMeals",
    "BehaviourStudentActions",	
    "StudentMiscellaneousInformation",
    "CalendarModels",
    "StudentParentalConsent",
    "Calendars",
    "StudentProtectionRegister",
    "Classes",
    "Students",
    "CollectionAssociates",
    "StudentSchoolTransportInformation",
    "CollectionExecutives",	
    "StudentSiblings",
    "CollectionExecutivesRoleTypes",	
    "StudentsInCare",
    "Collections",
    "StudentSurgeries",
    "Disabilities",
    "StudentSurgeryDoctors",
    "Emails",
    "SubjectClasses",
    "EmployeeContacts",	
    "TimeTable",
    "EmployeeRoles",
    "YearGroupClasses",
    "Ethnicities", 
    "HouseClasses",	 
    "Languages", 
    "Locations",
    "MealTypes",
    "MedicalConditions",	 
    "People", 
    "PersonAddresses",	 
    "PersonCommunications"
}

# Specify the path to your XML file
xml_file_path = "BromcomPermissionChecker\\findEntitiesBySchoolID.xml"

# Set up a parser with error handling
parser = etree.XMLParser(recover=True)

try:
    # Parse the XML file with error recovery
    with open(xml_file_path, 'rb') as file:
        root = etree.parse(file, parser)

    # Extract EntityNames from the XML file
    xml_entity_names = set()
    for table in root.findall(".//Table"):
        entity_name_element = table.find("EntityName")
        if entity_name_element is not None:
            entity_name = entity_name_element.text
            xml_entity_names.add(entity_name)

    
    # Compare the XML entity names against the Bromcom permissions list
    missing_in_xml = bromcom_permissions - xml_entity_names
    missing_in_bromcom = xml_entity_names - bromcom_permissions

    # Print the comparison results
    print("\nComparison Results:")
    if missing_in_xml:
        print("Missing Account Permissions:")
        print("\n".join(sorted(missing_in_xml)))
    else:
        print("Permission Check Successful")

    if missing_in_bromcom:
        print("Additional Account Permissions:")
        print("\n".join(sorted(missing_in_bromcom)))
    else:
        print("No additional Bromcom permissions.")

except etree.XMLSyntaxError as e:
    print(f"Parsing error encountered: {e}")
except FileNotFoundError:
    print(f"File not found: {xml_file_path}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
