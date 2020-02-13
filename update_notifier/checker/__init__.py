import logging

from importlib import import_module
from json import load, dump
from pathlib import Path

from .update_checker import UpdateChecker, UpdateCheckerException
from ..config import config, get_enabled_update_checkers


def get_versions():
    path = config['PATHS']['Versions']

    try:
        with open(path, 'r') as json_file:
            versions = load(json_file)
    except FileNotFoundError:
        update_checkers = _get_enabled_update_checkers()
        versions = {u.name: u.version for u in update_checkers}
        _dump_versions(versions)
        return None
    else:
        return versions


def _dump_versions(versions):
    path = config['PATHS']['Versions']

    if not versions:
        raise ValueError('Versions must not be None.')
    elif type(versions) is not dict:
        raise TypeError('Versions must be of type dict.')

    with open(path, 'w') as json_file:
        dump(versions, json_file)


def get_updates():
    versions = get_versions()

    if versions is None:
        return []

    update_checkers = _get_enabled_update_checkers()
    updates = filter(lambda u: u.is_new_update(versions), update_checkers)
    updates = list(updates)
    logging.info('Found %d updates.', len(updates))

    for u in updates:
        versions[u.name] = u.version

    _dump_versions(versions)

    return updates


def load_available_checkers():
    filename = __file__
    path: Path = Path(filename).resolve().parents[0]
    path = path / 'checkers'

    for f in path.glob('*.py'):
        name = f.stem

        if name.startswith('__'):
            continue

        import_module('.checkers.' + name, __package__)

    available_checkers = UpdateChecker.__subclasses__()

    return available_checkers


def _get_enabled_update_checkers():
    update_checkers = load_available_checkers()
    logging.debug('Found %d available checkers.', len(update_checkers))

    enabled_checkers_names = config['GENERAL']['EnabledUpdateCheckers']
    enabled_checkers_names = get_enabled_update_checkers(enabled_checkers_names)

    enabled_checkers = []
    for u in update_checkers:
        if u.__name__ in enabled_checkers_names:
            try:
                enabled_checkers.append(u())
            except UpdateCheckerException as e:
                logging.warning(u.__name__ + ' raised ' + e.__class__.__name__)

    logging.debug('Found %d enabled checkers.', len(enabled_checkers))

    return enabled_checkers
