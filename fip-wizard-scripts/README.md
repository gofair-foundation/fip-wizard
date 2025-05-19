# FIP Wizard Python Scripts

## Installation

1. Install Python 3.11 or later, including `pip` and `venv`: https://www.python.org/downloads/ (or via your package manager)
2. Create virtual environment and activate it:

```bash
python -m venv env

.\env\Scripts\activate  # Windows

source env/bin/activate  # Linux / MacOS
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Configuration with `.env`

To avoid the need to set environment variables in your shell, you can create a `.env` file in the current directory (see `example.env`) with the following content:

```env
# FIP Wizard API URL
# see: https://guide.fair-wizard.com/en/production/applications/data-management-planner/profile/about.html
WIZARD_API_URL=

# FIP Wizard API Key
# see: https://guide.fair-wizard.com/en/production/applications/data-management-planner/profile/settings/api-keys.html
WIZARD_API_KEY=
```

### FIP Wizard Curators Group

This script is designed to be run from the command line and updates all projects to add the FIP Wizard curators group.

```bash
python fip_wizard_curators_group.py
```

Make sure you have `WIZARD_API_URL` and `WIZARD_API_KEY` envvars set (preferrably in a `.env` file) to point to the FIP Wizard API and your API key. The script will read these values from the environment variables.

API Key can be obtained as described in the [FAIR Wizard documentation](https://guide.fair-wizard.com/en/production/applications/data-management-planner/profile/settings/api-keys.html). The changes are made then on behalf of the user who created the API key (user must be `admin`).
