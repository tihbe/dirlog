"""Helper functions to parse dirlog results"""
import re
import os
from datetime import datetime
from . import _get_globals, _get_dev_mode


def list_experiments(project: str, since: datetime = None, before: datetime = None) -> None:
    exp_name = re.sub(r"\s+", "-", project)  # Remove whitespaces
    exp_name = re.sub(r"[^\w\s]", "", exp_name)  # Remove non letters/digits
    exp_dir = "" if _get_dev_mode() else _get_globals().get("experiments_directory", "")
    exp_dir = os.path.join(exp_dir, exp_name)

    # Get all directories
    try:
        experiments_list = os.listdir(exp_dir)
    except FileNotFoundError:
        import sys

        print("Project experiment directory not found: %s" % exp_dir, file=sys.stderr)
        return []

    if since is not None:
        experiments_list = [p for p in experiments_list if datetime.strptime(p[:19], "%Y-%m-%d-%H-%M-%S") > since]
    if before is not None:
        experiments_list = [p for p in experiments_list if datetime.strptime(p[:19], "%Y-%m-%d-%H-%M-%S") <= before]

    experiments_list = [os.path.join(exp_dir, p) for p in experiments_list]
    return experiments_list


def create_df(experiments):
    """Load configs and results into a panda dataframe"""
    from pandas import DataFrame as df
    import toml

    objects = []
    for p in experiments:
        try:
            configs_file_path = os.path.join(p, "configs.toml")
            configs = toml.load(configs_file_path) if os.path.exists(configs_file_path) else {}
            results_file_path = os.path.join(p, "results.toml")
            results = toml.load(results_file_path) if os.path.exists(results_file_path) else {}
            configs.update(results)
            configs["experiment_path"] = p
            objects.append(configs)
        except toml.decoder.TomlDecodeError:
            print(f"Error decoding file in {p}")
    return df(objects)
