import nbformat

NB_PATH = 'notebooks/01A_frequency_decision_matrix.ipynb'
nb = nbformat.read(NB_PATH, as_version=4)

# Find the cell defining FREQUENCY_CONSTITUTION
target_cell_idx = 2
content = nb.cells[target_cell_idx].source

if "FREQUENCY_CONSTITUTION = {" in content and "'monetary':" not in content:
    new_entry = """    'monetary': {
        'series_patterns': ['IMPULSE', 'MULTIPLIER', 'FISCAL_DOMINANCE', 'CD_RATIO'],
        'native_frequency': 'monthly',
        'use_frequency': 'monthly',
        'transformation': 'Z-Score',
        'lag_range': '1-2 months',
        'publication_lag_months': 1,
        'economic_role': 'Credit Cycle Leader'
    },
    'trade': {"""
    
    # Try to replace 'trade' again as anchor
    if "'trade': {" in content:
        new_content = content.replace("'trade': {", new_entry)
        nb.cells[target_cell_idx].source = new_content
        nbformat.write(nb, NB_PATH)
        print("Successfully patched 01A with monetary category.")
    else:
        print("Could not find anchor 'trade' to inject monetary.")
else:
    print("Patch already applied or target not found.")
