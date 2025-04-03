import re

def modify_composition_file(input_file_path, output_file_path):
    # Read the input file
    with open(input_file_path, 'r') as file:
        file_content = file.readlines()

    # Locate the header line containing the species names
    header_line_index = next((i for i, line in enumerate(file_content) if 'c12' in line.lower()), None)
    if header_line_index is None:
        raise ValueError("The header line containing species names was not found.")

    # Extract column indices for the specified species
    header_line = file_content[header_line_index]
    columns = header_line.split()
    target_species = [
        "he4", "c12", "c13", "n13", "n14", "n15",
        "o16", "o17", "o18", "f19", "ne20", "ne22", "mg24", "si28","x30","x32"
    ]
    target_indices = {species: columns.index(species) for species in target_species if species in columns}

    # Define the value to set
    zero_value = "0.0000000000000000D+00"
    half_value = "0.5000000000000000D+00"

    # Modify the numerical data lines while preserving spacing
    modified_content = file_content.copy()
    for i in range(header_line_index + 1, len(modified_content)):
        line = modified_content[i]
        if re.match(r'^\s*\d+', line):  # Check if the line starts with a number (data line)
            # Use regex to split while preserving spacing
            parts = re.split(r'(\s+)', line)
            # Update values for the specified species
            for species, index in target_indices.items():
                if species in ["o18", "mg24"]:  # Set o16 and ne20 to 0.5
                    parts[2 * index] = half_value
                else:  # Set all others to 0
                    parts[2 * index] = zero_value
            # Reconstruct the line with original spacing
            modified_content[i] = "".join(parts)

    # Save the modified content to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(modified_content)

# Usage
input_file_path = "heated_ONe.mod"  # Replace with your input file path
output_file_path = "replaced_ONe.mod"  # Replace with your desired output file path
modify_composition_file(input_file_path, output_file_path)

print(f"Modified file saved to: {output_file_path}")

