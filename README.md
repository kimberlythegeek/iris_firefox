# iris_firefox

![Travis (.com)](https://img.shields.io/travis/com/mozilla/iris_firefox)
![GitHub](https://img.shields.io/github/license/mozilla/iris_firefox)
![GitHub repo size](https://img.shields.io/github/repo-size/mozilla/iris_firefox)
![GitHub issues](https://img.shields.io/github/issues/mozilla/iris_firefox)

Iris Firefox is a suite of tests specific to Firefox, using the [Mozilla Iris](https://github.com/mozilla/iris) test framework.

For more detailed information and troubleshooting tips, please [view our wiki](https://github.com/mozilla/iris_firefox/wiki).

## Installation

### System Requirements

 - [Firefox](https://www.mozilla.org/en-US/firefox/new/)
 - [Docker](https://docs.docker.com/v17.12/install/)

#### Setup

```
docker build . -t iris_firefox
```

### Usage

The basic usage is as follows:
```
# Run image tagged 'iris_firefox'
docker run -it iris_firefox /bin/bash
iris firefox -n [args]
```

For detailed examples of using Iris Firefox, see our [wiki and documentation](https://github.com/mozilla/iris_firefox/wiki/Basic-Workflow).

## Contributing

To contribute to the Iris Firefox project, more details are available on our [wiki](https://github.com/mozilla/iris_firefox/wiki/Contributions).

### Enable Pre-Commit Hooks

Iris has pre-commit hooks for flake8 linting and [black code formatting](https://pypi.org/project/black/). These hooks will run black and flake8 *prior to* committing your changes.

This means that black will format all python files in-place, and flake8 will lint your code for any errors.
If there are flake8 violations, *your changes will not be committed*. The list of ignored rules is documented in the
`tox.ini` file. There should be a compelling reason to do so before adding to this list.

```
# Install including pre-commit
pip install pre-commit
# Install pre-commit hooks defined in .pre-commit-config.yaml
pre-commit install
```

That's it! Here's an example of how it works:
```
# make some changes
git add -A
git commit -m 'detailed commit message'
[WARNING] Unstaged files detected.
[INFO] Stashing unstaged files to /Users/ksereduck/.cache/pre-commit/patch1570121459.
black....................................................................Passed
Flake8...................................................................Failed
hookid: flake8

targets/firefox/bug_manager.py:11:1: E402 module level import not at top of file
targets/firefox/bug_manager.py:12:1: E402 module level import not at top of file
targets/firefox/bug_manager.py:14:1: E402 module level import not at top of file
targets/firefox/bug_manager.py:15:1: E402 module level import not at top of file
targets/firefox/bug_manager.py:16:1: E402 module level import not at top of file

[INFO] Restored changes from /Users/ksereduck/.cache/pre-commit/patch1570121459.
```
