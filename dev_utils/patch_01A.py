import nbformat

NB_PATH = 'notebooks/01A_frequency_decision_matrix.ipynb'
nb = nbformat.read(NB_PATH, as_version=4)

# Find the cell defining FREQUENCY_CONSTITUTION
# Based on view_file, it's cell 3 (index 2) - "FREQUENCY_CONSTITUTION = {"
target_cell_idx = 2
content = nb.cells[target_cell_idx].source

if "FREQUENCY_CONSTITUTION = {" in content and "'flow':" not in content:
    # Inject flow category before 'trade'
    new_entry = """    'flow': {
        'series_patterns': ['FPI', 'FDI', 'PORTFOLIO INVESTMENT', 'Net Portfolio', 'Flow', 'Investment In India'],
        'native_frequency': 'monthly',
        'use_frequency': 'monthly',
        'transformation': 'Z-Score',
        'lag_range': '1-3 months',
        'publication_lag_months': 1,
        'economic_role': 'Structural Liquidity Regime'
    },
    'trade': {"""
    
    new_content = content.replace("'trade': {", new_entry)
    nb.cells[target_cell_idx].source = new_content
    nbformat.write(nb, NB_PATH)
    print("Successfully patched 01A with flow category.")
else:
    print("Patch already applied or target not found.")
