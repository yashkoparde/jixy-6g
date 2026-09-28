from pathlib import Path
import logging, random, yaml
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def load_config(path=None):
    with open(path or ROOT / 'config.yaml', encoding='utf-8') as f:
        return yaml.safe_load(f)

def resolve(path):
    p = Path(path)
    return p if p.is_absolute() else ROOT / p

def seed_everything(seed=42):
    random.seed(seed); np.random.seed(seed)
    try:
        import tensorflow as tf
        tf.keras.utils.set_random_seed(seed)
    except ImportError:
        pass

def get_logger(name, filename='application.log'):
    log_dir = ROOT / 'logs'; log_dir.mkdir(exist_ok=True)
    logger = logging.getLogger(name); logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(log_dir / filename, encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))
        logger.addHandler(handler)
    return logger
