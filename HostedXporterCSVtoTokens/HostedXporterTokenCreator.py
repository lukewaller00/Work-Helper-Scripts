import os
import configparser
from typing import Dict, Optional

class TokenCreator:
    def __init__(self):
        self.mis_types = {
            'arbor': ['Arbor_WebServiceUrl'],
            'bromcom': ['Bromcom_SchoolId', 'Bromcom_WebServiceUrl'],
            'isams': ['iSAMS_WebServiceUrl'],
            'progresso': ['Progresso_WebServiceUrl', 'Progresso_SchoolID'],
            'pupilasset': ['PupilAsset_WebService', 'PupilAsset_SchoolId']
        }
    
    def get_user_input(self) -> Dict[str, str]:
        """Get all necessary user input for token creation."""
        while True:
            dfe_code = input("Please enter the 7-digit DFE code: ").strip()
            if len(dfe_code) == 7 and dfe_code.isdigit():
                break
            print("Invalid DFE code. Please enter exactly 7 digits.")
        
        lea_code = dfe_code[:3]
        dfes_number = dfe_code[3:]
        
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
        
        # Get MIS-specific information
        mis_info = {}
        print("\nEnter the following required information:")
        for field in self.mis_types[mis_type]:
            mis_info[field] = input(f"Enter {field}: ").strip()
        
        return {
            'lea_code': lea_code,
            'dfes_number': dfes_number,
            'mis_type': mis_type,
            'school_name': school_name,
            'mis_info': mis_info
        }
    
    def create_token_file(self, data: Dict[str, str]) -> None:
        """Create the token.ini file with the provided data."""
        # Create a custom ConfigParser that preserves case
        config = configparser.ConfigParser()
        config.optionxform = str  # This preserves the case of the keys
        
        config['Tokens'] = {
            'LeaCode': data['lea_code'],
            'DfesNumber': data['dfes_number'],
            'SchoolName': data['school_name'],
            'Mis': data['mis_type'],
            'HostedSchoolIdentifier': f"{data['lea_code']}{data['dfes_number']}",
            'AlertApiKey': ''
        }
        
        # Add MIS-specific fields (preserving their exact case)
        for key, value in data['mis_info'].items():
            config['Tokens'][key] = value
        
        # Create directory if it doesn't exist
        folder_name = f"{data['lea_code']}{data['dfes_number']}"
        os.makedirs(folder_name, exist_ok=True)
        
        # Write the token file with custom formatting
        file_path = os.path.join(folder_name, 'token.ini')
        with open(file_path, 'w') as token_file:
            config.write(token_file, space_around_delimiters=False)
            
        # Fix the formatting to remove spaces around equals signs
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Remove spaces around equals signs
        content = content.replace(' = ', '=')
        
        with open(file_path, 'w') as file:
            file.write(content)
        
        print(f"\nToken file created successfully at: {os.path.abspath(file_path)}")

def main():
    print("Welcome to the MIS Token Creator\n")
    creator = TokenCreator()
    
    try:
        # Get user input
        data = creator.get_user_input()
        
        # Create token file
        creator.create_token_file(data)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()