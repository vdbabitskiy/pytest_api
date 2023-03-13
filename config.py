import yaml

from core.utils import get_root_path

with open(f'{get_root_path()}/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

TIME_OUT_TOTALL = config['TIME_OUT_TOTALL']
TIME_OUT_CONNECTION = config['TIME_OUT_CONNECTION']
API_URL = config['API_URL']