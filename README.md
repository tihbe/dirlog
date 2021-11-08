Dirlog
=======
Utility library for logging files in a self generated directory.

## Usage

### Creating a directory

In the terminal:
```bash
dirlog --create experiment_name
```

In the code:
```python
import dirlog

dirlog.createdir()  # Optional call
help(dirlog.createdir)  # Self-documented code
```
```
> createdir(dir_name: str = None, exp_name: str = None) -> str
>     Create a directory if not previously created or specified as argument.
>
>     Args:
>         dir_name (str, optional): Directory path (e.g. to continue experiment). Defaults to timestamp + exp_name.
>         exp_name (str, optional): Experiment name. Defaults to python file name.
> 
>     Returns:
>         str: Path to newly created logging directory.
```

### Saving configurations
```python
dirlog.sconf({"parameter_1": 3}) # Optional dict as firt argument
dirlog.sconf(parameter_2=2) # Named arguments work too
```

### Saving results
```python
dirlog.sres({"result_1": 3}) # Same API as configurations
dirlog.sres(result_2=2)
```

### Saving logs
```python
import logging
logger = logging.getLogger()
dirlog.slogs(logger)
```

### Saving anything else.

Just join the path to add anything to the logging directory when saving.
```python
import numpy as np
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
plt.savefig(dirlog.joinpth("my_figure.png"))
np.save(dirlog.joinpth("my_nparray.npy"), np.linspace(0, 10, 2))
```

## Changing the base directory
You can change the default base logging directory by creating a dotfile `~/.dirlog` with content:

```
experiments_directory = "path/to/any/directory"
```
It is recommended to set this path to a backed-up folder (e.g. git repo, MS OneDrive, Google Drive, etc).