import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data_loader import DataLoader
from src.management_commentary import ManagementCommentaryGenerator

dl = DataLoader()
try:
    budget = dl.load_budget().to_dict('records')
except Exception as e:
    print('ERROR_LOADING_BUDGET', e)
    budget = []

gen = ManagementCommentaryGenerator()
text = gen.generate_commentary({}, budget, [], use_llm=False)
print('---COMMENTARY START---')
print(text)
print('---COMMENTARY END---')
# Save
out = Path(__file__).parent / 'generated_rules_commentary.md'
out.write_text(text, encoding='utf-8')
print('SAVED:', out)
