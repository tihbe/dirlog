"""Core functions of the dirlog library."""
import os
import toml
import logging as _logging
from pathlib import Path
from inspect import getcallargs

_DIRNAME = None
_DEVMODE = False


def createdir(dir_name: str = None, exp_name: str = None) -> str:
    """Create a directory if not previously created or specified as argument.

    Args:
        dir_name (str, optional): Directory path (e.g. to continue experiment). Defaults to timestamp + exp_name.
        exp_name (str, optional): Experiment name. Defaults to python file name.

    Returns:
        str: Path to newly created logging directory.
    """
    global _DIRNAME
    if _DIRNAME is not None:
        return _DIRNAME
    if dir_name is not None:
        Path(dir_name).mkdir(exist_ok=True)
        _DIRNAME = dir_name
        return dir_name
    from datetime import datetime
    from inspect import stack
    import re

    if exp_name is None:
        for f in stack()[1:]:
            if f.filename[0] != "<" and f.filename != __file__:
                exp_name = os.path.basename(f.filename).replace(".py", "")
        if exp_name is None:
            exp_name = "untitled"

    parent_dir = "" if _DEVMODE else _get_globals().get("experiments_directory", "")
    exp_dir = re.sub(r"\s+", "-", exp_name)  # Remove whitespaces
    exp_dir = re.sub(r"[^\w\s]", "", exp_dir)  # Remove non letters/digits
    bstring = "_dev_%s" if _DEVMODE else datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%%s")
    dir_name = os.path.join(parent_dir, exp_dir, bstring % exp_name)
    i = 2

    while os.path.exists(dir_name) and not _DEVMODE:
        dir_name = os.path.join(parent_dir, exp_dir, bstring % exp_name + "_" + str(i))
        i += 1

    Path(dir_name).mkdir(parents=True, exist_ok=True)
    _DIRNAME = dir_name
    return dir_name


def _get_globals():
    global_config_file = os.path.expanduser("~/.dirlog")
    if os.path.exists(global_config_file):
        with open(global_config_file, "r") as f_hndl:
            return toml.load(f_hndl)
    return {}


def set_dev_mode():
    """make a dev_{experiment_name} folder instead of using the timestamp"""
    global _DEVMODE
    _DEVMODE = True


def _get_dev_mode():
    return _DEVMODE


def getdir():
    return _DIRNAME


def save_to_file(filename, data={}, **nargs):
    """Save object data to filename in the log directory as toml, append data if file previously exists"""
    path = joinpth(filename)
    data.update(nargs)  # We can call either sconf(dict) or sconf(key=value)
    if os.path.exists(path):
        # Append to existing toml
        previous_data = toml.load(open(path, "r"))
        previous_data.update(data)
        data = previous_data
    toml.dump(data, open(path, "w"))


def sconf(configs={}, **nargs):
    """Alias for save_to_file(configs.toml, ...)"""
    return save_to_file("configs.toml", configs, **nargs)


def sres(results={}, **nargs):
    """Alias for save_to_file(results.toml, ...)"""
    return save_to_file("results.toml", results, **nargs)


def sargs(func):
    """Decorator to save function arguments into the config file"""

    def wrap(*args, **nargs):
        sconf({func.__name__: getcallargs(func, *args, **nargs)})
        return func(*args, **nargs)

    return wrap


def sstate(**ndarrays):
    """Func for saving ndarrays to dirlog directory"""
    import numpy as np

    for name, ndarray in ndarrays.items():
        np.save(jp(name), ndarray, allow_pickle=True)


def gstate(name):
    """Func for loading ndarray from dirlog directory"""
    import numpy as np

    return np.load(f"{jp(name)}.npy")


def joinpth(path: str) -> str:
    """Add experiment directory to path"""
    dir_name = createdir()  # Create directory if setdir wasn't already called
    return os.path.join(dir_name, path)


jp = joinpth  # Alias


def slogs(logger: _logging.Logger, filename: str = "logs.txt", level=_logging.DEBUG, stream: bool = True) -> None:
    """Set logging level of logger and register a new handler to dump logs on disk"""
    logger.setLevel(level)
    fh = _logging.FileHandler(joinpth(filename))
    fh.setLevel(level)
    formatter = _logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if stream:
        sh = _logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)


def init(configs={}, logger=None, filename="logs.txt", level=_logging.DEBUG, dev_mode=False, stream=True):
    """Conveninent wrapper around slogs, sconf and set_dev_mode in one call
    It is not mandatory to call init for dirlog"""
    if dev_mode:
        set_dev_mode()
    if logger is not None:
        slogs(logger, filename, level, stream)
    sconf(configs)
