# Linked account updater
This is a utility to update linked account expiration dates accross Alma institution zones.

## Settings
Settings are set in the `linked_account_update/settings.py` file. You need to have Users read/write keys for the IZ you want to update patrons in, and at least read-only keys for the IZs you want updates from. You can also have the script get settings from the os environment instead by setting SETTINGS_FROM_ENV to True.

## Directory structure
`linked_acccount_update` - this is the update script module directory.
`data` - this is a scratch directory to hold your report data
`tests` - tests written with pytest

## installation
Before installing, make sure you have python 3 installed. This was developed in python 3.6. 
```
#set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# install the module and requirements
pip install -e .
pip install -r requirements.txt
```
## testing
After configuring your API keys, run
```
pytest -v
```
If you have API keys configured in the `settings.py` file, you can test them by removing the --ignore flag.
