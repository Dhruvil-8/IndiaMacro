import nbformat

NB_PATH = 'notebooks/01A_frequency_decision_matrix.ipynb'
nb = nbformat.read(NB_PATH, as_version=4)

# Find the cell defining FREQUENCY_CONSTITUTION
# Based on view_file, it's cell 3 (index 2)
target_cell_idx = 2
content = nb.cells[target_cell_idx].source

if "FREQUENCY_CONSTITUTION = {" in content and "'fci':" not in content:
    # Inject fci category before 'trade' or after 'liquidity'
    # We'll inject it alongside 'flow' if it exists, or just append it
    
    new_entry = """    'fci': {
        'series_patterns': ['FCI', 'GSEC_10Y', 'CALL_RATE', 'FX_RESERVES', 'USDINR_VOL'],
        'native_frequency': 'weekly',
        'use_frequency': 'weekly',
        'transformation': 'Z-Score',
        'lag_range': '0-1 weeks',
        'publication_lag_months': 0,
        'economic_role': 'Financial Conditions Nowcaster'
    },
    'trade': {"""
    
    # Try to replace 'trade' again (since we injected 'flow' before 'trade' last time, 
    # 'trade' should still be there as a valid anchor)
    if "'trade': {" in content:
        new_content = content.replace("'trade': {", new_entry)
        nb.cells[target_cell_idx].source = new_content
        nbformat.write(nb, NB_PATH)
        print("Successfully patched 01A with fci category.")
    else:
        print("Could not find anchor 'trade' to inject fci.")
else:
    print("Patch already applied or target not found.")
