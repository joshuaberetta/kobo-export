# kobo-export

Locally generate exports from your KoboToolbox project.

_Note that this is currently under early development and will likely break very easily -- please open an issue if you find problems._

## Setup

1. Clone this repo locally.

```bash
git clone https://github.com/joshuaberetta/kobo-export.git
```

2. Create virtual environment and install python requirements.

```bash
python3 -m venv venv && source venv/bin/activate
pip3 install -r requirements.txt
```

3. Copy the `config-sample.json` file to `config.json` and enter your project details:
    - `limit`: Number of submissions included in each page of the response -- reduce this for large surveys or and/or slow internet connections.
    - `versions`: If set to `[]`, then all versions will be included, otherwise specify a list of version UIDs and the output will include only the submissions that were collected with those versions.
    - `options`: Various export options that are normally available through the UI.

**Example**

```json
{
    "kf_url": "https://kf.kobotoolbox.org",
    "token": "2131fap23dg4fc6355c8d1sga119c504d55dd8ca078",
    "asset_uid": "a9BZUA8jhQesaUJp21qyB",
    "limit": 10000,
    "versions": [
        "vd3Zyj4uHQ6bZhBurJe9yi",
        "vJJbvAKXriqT5DgQu2k2Cd"
    ],
    "options": {
        "group_sep": "/",
        "multiple_select": "both",
        "lang": "English (en)",
        "hierarchy_in_labels": false,
        "force_index": true,
        "tag_cols_for_header": ["hxl"],
        "filter_fields": [],
        "xls_types_as_text": false,
        "include_media_url": true
    }
}
```

## Usage

Currently all configuration is done through the `config.json` file and it doesn't accept arguments.

```bash
python3 export.py
```