import os
import configparser
from typing import Dict, List, Optional

class TokenCreator:
    def __init__(self):
        self.mis_types = {
            'arbor': ['Arbor_WebServiceUrl'],
            'bromcom': ['Bromcom_SchoolId', 'Bromcom_WebServiceUrl'],
            'isams': ['iSAMS_WebServiceUrl'],
            'progresso': ['Progresso_WebServiceUrl', 'Progresso_SchoolID'],
            'pupilasset': ['PupilAsset_WebService', 'PupilAsset_SchoolId']
        }

    def parse_config_file(self, filepath: str) -> List[Dict[str, str]]:
        schools = []
        current_school = {}
        
        with open(filepath, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
            
        for line in lines:
            if line.startswith('[School]'):
                if current_school:
                    schools.append(current_school)
                current_school = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                current_school[key.strip()] = value.strip()
                
        if current_school:
            schools.append(current_school)
            
        return schools
    
    def get_user_input(self) -> Dict[str, str]:
        while True:
            dfe_code = input("Please enter the 7-digit DFE code: ").strip()
            if len(dfe_code) == 7 and dfe_code.isdigit():
                break
            print("Invalid DFE code. Please enter exactly 7 digits.")
        
        print("\nAvailable MIS types:")
        for i, mis in enumerate(self.mis_types.keys(), 1):
            print(f"{i}. {mis.title()}")
        
        while True:
            try:
                mis_choice = int(input("\nSelect MIS type (enter number): "))
                if 1 <= mis_choice <= len(self.mis_types):
                    break
                print("Invalid choice. Please select a number from the list.")
            except ValueError:
                print("Please enter a valid number.")
        
        mis_type = list(self.mis_types.keys())[mis_choice - 1]
        school_name = input("\nEnter school name: ").strip()
        
        mis_info = {}
        print("\nEnter the following required information:")
        for field in self.mis_types[mis_type]:
            mis_info[field] = input(f"Enter {field}: ").strip()
        
        return {
            'dfe_code': dfe_code,
            'school_name': school_name,
            'mis_type': mis_type,
            **mis_info
        }
    
    def create_token_file(self, data: Dict[str, str]) -> None:
        config = configparser.ConfigParser()
        config.optionxform = str
        
        config['Tokens'] = {
            'LeaCode': data['dfe_code'][:3],
            'DfesNumber': data['dfe_code'][3:],
            'SchoolName': data['school_name'],
            'Mis': data['mis_type'],
            'HostedSchoolIdentifier': data['dfe_code'],
            'AlertApiKey': ''
        }
        
        for key in self.mis_types[data['mis_type']]:
            if key in data:
                config['Tokens'][key] = data[key]
        
        folder_name = "HostedXporterCSVtoTokens/Schools/"+data['dfe_code']
        os.makedirs(folder_name, exist_ok=True)
        
        file_path = os.path.join(folder_name, 'Tokens.ini')
        with open(file_path, 'w') as token_file:
            config.write(token_file, space_around_delimiters=False)
            
        with open(file_path, 'r') as file:
            content = file.read()
        content = content.replace(' = ', '=')
        with open(file_path, 'w') as file:
            file.write(content)
        
        print(f"Token created for {data['school_name']}")

def main():
    creator = TokenCreator()
    print("MIS Token Creator\n")
    print("1. Interactive Mode")
    print("2. Batch Mode (from schools.txt)")
    
    while True:
        try:
            mode = int(input("\nSelect mode: "))
            if mode in [1, 2]:
                break
            print("Please select 1 or 2")
        except ValueError:
            print("Please enter a valid number")
    
    try:
        if mode == 1:
            data = creator.get_user_input()
            creator.create_token_file(data)
        else:
            schools = creator.parse_config_file('HostedXporterCSVtoTokens\schools.txt')
            for school in schools:
                creator.create_token_file(school)
    except KeyboardInterrupt:
        print("\nOperation cancelled")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()