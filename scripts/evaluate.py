from pathlib import Path
import json
from src.evaluation.compare import write_comparison
if __name__=='__main__':
    rows=write_comparison(); print(json.dumps(rows,indent=2) if rows else 'No experiment metrics found; train a model first.')
