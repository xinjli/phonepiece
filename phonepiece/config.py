import platform
from pathlib import Path
import logging


class PhonePieceConfig:

    root_path = Path(__file__).parent

    # data path
    data_path = root_path / 'data'
    data_str = str(data_path)

    logger = logging.getLogger('phonepiece')