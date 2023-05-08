from phonepiece.config import *
from phonepiece.bin.download_model import download_model
from phonepiece.lang import normalize_lang_id
import pip
import importlib

def import_with_auto_install(package, package_name):
    try:
        return importlib.import_module(package)
    except ImportError:
        pip.main(['install', package_name])
    return importlib.import_module(package)


def load_lang_dir(lang_id, model_name='latest'):
    """
    make sure lang_dir is properly downloaded or loaded

    :param lang_id: a 3 char or 2 char iso id
    :param model_name: model name or a customized path
    :type lang_id_or_path:
    :return:
    :rtype:
    """

    # normalize language id (e.g: 2 char 639-1 -> 3 char 639-3)
    lang_id = normalize_lang_id(lang_id)

    # windows does not allow the following directory name, which coincides with language id
    # we give them a _ prefix to avoid naming issue on windows
    if lang_id in ['prn', 'con', 'aux', 'null']:
        lang_id = '_' + lang_id

    # check whether a customized path is used or not
    if (Path(model_name) / lang_id).exists():
        lang_dir = Path(model_name) / lang_id
    else:
        lang_dir = PhonePieceConfig.data_path / 'model' / model_name / lang_id

        # if not exists, we try to download the model
        if not lang_dir.exists():
            download_model(model_name)

        if not lang_dir.exists():
            print(f"warning: could not download or read {lang_id} inventory, using eng instead")
            lang_dir = PhonePieceConfig.data_path / 'model' / model_name / 'eng'

    return lang_dir