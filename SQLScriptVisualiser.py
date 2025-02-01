import re
import graphviz

# Example SQL scripts (you can load these from files if needed)
scripts = {
    "bromcomattendancehelper.sql": """
        &brocomdetails
        &bromcomschoolinfo
    """,
    "bromcomlearners.sql": """
        &bromcomlearnerdetails
        &bromcomclasses
    """,
    "bromcompersonal.sql": """
        &bromcomstaff
        &bromcomstudents
    """,
    "brocomdetails.sql": """
        SELECT * FROM details_table;
    """,
    "bromcomschoolinfo.sql": """
        SELECT * FROM school_info_table;
    """,
    "bromcomlearnerdetails.sql": """
        SELECT * FROM learner_details_table;
    """,
    "bromcomclasses.sql": """
        SELECT * FROM classes_table;
    """,
    "bromcomstaff.sql": """
        SELECT * FROM staff_table;
    """,
    "bromcomstudents.sql": """
        SELECT * FROM students_table;
    """
}

# Function to extract dependencies from SQL content
def extract_dependencies(sql_content):
    dependencies = []
    # Use regex to find patterns like &script_name
    matches = re.findall(r"&\w+", sql_content)
    for match in matches:
        # Remove the & and append .sql to get the script name
        script_name = match.strip("&") + ".sql"
        dependencies.append(script_name)
    return dependencies

# Function to recursively resolve dependencies
def resolve_dependencies(script, scripts, resolved, graph):
    if script not in scripts:
        return  # Skip if the script is not in the dictionary
    if script in resolved:
        return  # Skip if the script is already resolved

    # Add the script to the resolved set
    resolved.add(script)

    # Extract dependencies for the current script
    dependencies = extract_dependencies(scripts[script])
    for dep in dependencies:
        if dep in scripts:  # Ensure the dependency is in the scripts dictionary
            # Add an edge from the current script to the dependency
            graph.edge(script, dep)
            # Recursively resolve dependencies for the dependency
            resolve_dependencies(dep, scripts, resolved, graph)

# Function to read the starting file
def read_starting_file(file_name):
    try:
        with open(file_name, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None

# Main function
def main():
    # Input: Starting file name
    starting_file = input("Enter the starting file name (e.g., input_script.sql): ").strip()

    # Read the starting file's content
    starting_content = read_starting_file(starting_file)
    if starting_content is None:
        return  # Exit if the file is not found

    # Add the starting file to the scripts dictionary
    scripts[starting_file] = starting_content

    # Create a directed graph
    dot = graphviz.Digraph(comment="SQL Script Flowchart")

    # Resolve dependencies starting from the input file
    resolved_scripts = set()
    resolve_dependencies(starting_file, scripts, resolved_scripts, dot)

    # Add nodes with script contents
    for script in resolved_scripts:
        # Truncate content for readability (optional)
        content = scripts[script]
        truncated_content = content[:50] + "..." if len(content) > 50 else content
        dot.node(script, label=f"{script}\n\n{truncated_content}")

    # Render and save the graph
    dot.render("sql_flowchart", format="png", view=True)
    print("Flowchart generated as 'sql_flowchart.png'.")

# Run the program
if __name__ == "__main__":
    main()
