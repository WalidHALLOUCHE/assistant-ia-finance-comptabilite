import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data_loader import DataLoader
from src.management_commentary import ManagementCommentaryGenerator

print('Starting LLM commentary generation...')

dl = DataLoader()
try:
    budget = dl.load_budget().to_dict('records')
except Exception as e:
    print('ERROR_LOADING_BUDGET', e)
    budget = []

G = ManagementCommentaryGenerator()
try:
    text = G.generate_commentary({}, budget, [], use_llm=True)
    print('---LLM START---')
    print(text)
    print('---LLM END---')
    out = Path(__file__).parent.parent / 'assets' / 'demo_commentaires' / 'generated_llm_commentary.md'
    out.write_text(text, encoding='utf-8')
    print('SAVED:', out)
except Exception as e:
    print('LLM_GENERATION_ERROR', e)
    raise
