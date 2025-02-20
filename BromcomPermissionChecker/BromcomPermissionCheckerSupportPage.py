from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_web_permissions():
    """Scrape permissions from the Community Brands support page using Selenium"""
    url = "https://support.communitybrands.uk/s/article/Xporter-Enable-Access-in-Bromcom"
    
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to load
        
        html = driver.page_source
        
        # Save raw response for debugging
        with open('selenium_response.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("Saved fully loaded response to selenium_response.html")
        
        soup = BeautifulSoup(html, "html.parser")
        permissions = set()
        
        table = soup.find('table')
        if not table:
            print("No table found in the page")
            return None
        
        for row in table.find_all('tr'):
            for cell in row.find_all('td'):
                text = cell.get_text(strip=True)
                if text:
                    permissions.add(text)
        
        
        print(permissions)

        print(f"Found {len(permissions)} permissions in table")
        return permissions
    
    finally:
        driver.quit()

def parse_xml_permissions(xml_path):
    """Parse permissions from XML with proper namespace handling"""
    try:
        namespaces = {
            'diffgr': 'urn:schemas-microsoft-com:xml-diffgram-v1',
            'msdata': 'urn:schemas-microsoft-com:xml-msdata'
        }
        
        tree = etree.parse(xml_path)
        entities = tree.xpath('//diffgr:diffgram//Table/EntityName/text()', namespaces=namespaces)
        return set(entities)
        
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return None

def main():
    web_permissions = get_web_permissions()
    if not web_permissions:
        print("Using fallback permissions list")
        web_permissions = {"Addresses", "PersonMedicalConditions", "PersonTelephones", "Students", "Staff"}
    
    xml_path = "BromcomPermissionChecker/findEntitiesBySchoolID.xml"
    xml_permissions = parse_xml_permissions(xml_path)
    if not xml_permissions:
        return
    
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
