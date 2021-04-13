# Azure Tag CLI Toolkit

This simple Python application can be interacted from the CLI. It allows the update of keys, values, adding and deleting tags. Changes will be made across all subscriptions the service principal used has permissions to.

## Pre-requisites

Create a [service principal](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals) with ['Tag Contributor'](https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#tag-contributor) across the subscriptions you are required to make changes to.

## Installation

+ Ensure you have [Python3](https://www.python.org/), [pip3](https://pip.pypa.io/en/stable/) and [venv](https://docs.python.org/3/library/venv.html) installed.
+ Use pip to install requests

```bash
pip install requests
```

Run ```python3 main.py``` and follow through the instructions!

## Contributing

Pull requests are welcome and new features are welcome!

## License

[MIT](https://choosealicense.com/licenses/mit/)