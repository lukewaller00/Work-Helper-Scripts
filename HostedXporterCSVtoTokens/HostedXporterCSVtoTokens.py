import pandas as pd
import os

# Load the CSV file
file_path = r"C:\path_to_your_file\865-Arbor-Migrations.csv"
csv_data = pd.read_csv(file_path)

# Define the base directory where folders will be created
base_dir = r"C:\path_to_your_output_directory\Schools"

# Ensure the base directory exists
os.makedirs(base_dir, exist_ok=True)

# Function to generate the tokens based on MIS
def generate_tokens(row):
    common_tokens = f"""LeaCode={row['LEACode']}
DfesNumber={row['DFEsNumber']}
SchoolName={row['SchoolName']}
Mis={row['MIS']}
HostedSchoolIdentifier={row['LEACode']}{row['DFEsNumber']}
AlertApiKey={row['alertapikey'] if pd.notna(row['alertapikey']) else ''}"""

    if row['MIS'].lower() == 'arbor':
        return f"""{common_tokens}
Arbor_WebServiceUrl={row['Arbor_WebServiceUrl']}
"""

    elif row['MIS'].lower() == 'bromcom':
        return f"""[Tokens]
{common_tokens}
Bromcom_WebServiceUrl=https://cloudmis.bromcom.com/Nucleus/WebServices/ThirdParty/TPReadOnlyDataService.asmx
Bromcom_SchoolId={row.get('Bromcom_SchoolId', '')}
"""

    elif row['MIS'].lower() == 'g2':
        return f"""[Tokens]
{common_tokens}
G2_Scope=
G2_Server=
"""

    elif row['MIS'].lower() == 'isams':
        return f"""[Tokens]
{common_tokens}
iSAMS_WebServiceUrl={row['Arbor_WebServiceUrl']}
"""

    elif row['MIS'].lower() == 'progresso':
        return f"""[Tokens]
{common_tokens}
Progresso_WebServiceUrl=https://api.progresso.net/Services/PerCall/
Progresso_SchoolId=
"""

    elif row['MIS'].lower() == 'pupilasset':
        return f"""[Tokens]
{common_tokens}
PupilAsset_WebService=https://secure.pupilasset.com/ajax/assetAjax.php
PupilAsset_SchoolId={row.get('PupilAsset_SchoolId', '')}
"""

    # Handle unknown MIS types
    else:
        print(f"Warning: Unknown MIS '{row['MIS']}' for school '{row['SchoolName']}' (DfesNumber: {row['DFEsNumber']})")
        return None

# Loop over each row in the dataframe to create the folders and Tokens.ini files
for index, row in csv_data.iterrows():
    # Create a directory for each schoolidentifier
    school_folder = os.path.join(base_dir, str(row['schoolidentifier']))
    os.makedirs(school_folder, exist_ok=True)
    
    # Generate the token content based on the MIS field
    tokens_content = generate_tokens(row)
    
    if tokens_content is not None:
        # Path for Tokens.ini file
        tokens_file_path = os.path.join(school_folder, 'Tokens.ini')
        
        # Write the Tokens.ini file
        with open(tokens_file_path, 'w') as tokens_file:
            tokens_file.write(tokens_content)
            print(f"Tokens.ini file created at: {tokens_file_path}")
    else:
        print(f"Skipped creating Tokens.ini for school: {row['SchoolName']} (DfesNumber: {row['DFEsNumber']})")
