from lxml import etree
import requests
from bs4 import BeautifulSoup

def get_web_permissions():
    """Scrape permissions from the Community Brands support page"""
    url = "https://support.communitybrands.uk/s/article/Xporter-Enable-Access-in-Bromcom"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        permissions = set()
        
        # Extract permissions from all table cells
        for td in soup.select('td[class*="xl"]'):
            # Clean and split multi-line entries
            text = td.get_text(separator=' ', strip=True)
            for line in text.split('\n'):
                cleaned = line.strip('• ').strip()
                if cleaned and cleaned != ' ' and not cleaned.isspace():
                    permissions.add(cleaned)
        
        return permissions

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
            "Addresses", "PersonMedicalConditions", "AdministrationDoctorTelephones",
            "PersonMedicalEvents", "AssessmentAssociationAssessmentTypes",
            # ... (rest of original hardcoded permissions)
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