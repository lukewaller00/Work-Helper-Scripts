from lxml import etree
import requests
from bs4 import BeautifulSoup

def get_web_permissions():
    """Scrape permissions from the Community Brands support page"""
    url = "https://support.communitybrands.uk/s/article/Xporter-Enable-Access-in-Bromcom"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Save raw response to file
        with open('response_dump.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Saved response to response_dump.html")
        
        print("Attempting to pull permissions from support page")
        soup = BeautifulSoup(response.text, 'html.parser')
        permissions = set()


        # Find the main permissions table
        table = soup.find('table')
        if not table:
            print("No table found in the page")
            return None

        # Extract all cells from all rows
        for row in table.find_all('tr'):
            for cell in row.find_all('td'):
                # Extract clean text from nested spans
                text = cell.get_text(strip=True)
                if text and not text.isspace():
                    permissions.add(text)

        print(f"Found {len(permissions)} permissions in table")
        return permissions
    
    except Exception as e:
        print(f"Error fetching permissions: {e}")
        return None
        
    
    except Exception as e:
        print(f"Error fetching permissions: {e}")
        return None

def parse_xml_permissions(xml_path):
    """Parse permissions from XML with proper namespace handling"""
    try:
        # Define XML namespaces
        namespaces = {
            'diffgr': 'urn:schemas-microsoft-com:xml-diffgram-v1',
            'msdata': 'urn:schemas-microsoft-com:xml-msdata'
        }
        
        tree = etree.parse(xml_path)
        entities = tree.xpath('//diffgr:diffgram//Table/EntityName/text()', 
                            namespaces=namespaces)
        return set(entities)
        
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return None

def main():
    # Get permissions from website
    web_permissions = get_web_permissions()
    if not web_permissions:
        print("Using fallback permissions list")
        web_permissions = {
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

    # Get permissions from XML
    xml_path = "BromcomPermissionChecker\\findEntitiesBySchoolID.xml"
    xml_permissions = parse_xml_permissions(xml_path)
    if not xml_permissions:
        return

    # Compare permissions
    missing_in_xml = web_permissions - xml_permissions
    extra_in_xml = xml_permissions - web_permissions

    print("\n=== Permission Validation Results ===")
    
    if missing_in_xml:
        print(f"\n[!] Missing {len(missing_in_xml)} required permissions:")
        for perm in sorted(missing_in_xml):
            print(f"  - {perm}")
    else:
        print("\n[✓] All required permissions present in XML")
        
    if extra_in_xml:
        print(f"\n[!] Found {len(extra_in_xml)} unexpected permissions:")
        for perm in sorted(extra_in_xml):
            print(f"  - {perm}")
    else:
        print("\n[✓] No unexpected permissions found")

if __name__ == "__main__":
    main()