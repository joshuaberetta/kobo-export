#!/usr/bin/env python3

import json
import requests
from datetime import datetime

from formpack import FormPack
from formpack.schema.fields import (
    IdCopyField,
    NotesCopyField,
    SubmissionTimeCopyField,
    TagsCopyField,
    ValidationStatusCopyField,
)


COPY_FIELDS = (
    IdCopyField,
    '_uuid',
    SubmissionTimeCopyField,
    ValidationStatusCopyField,
    NotesCopyField,
    '_status',
    '_submitted_by',
    '__version__',
    TagsCopyField,
)


def get_config():
    with open('config.json', 'r') as f:
        config = json.loads(f.read())
    config['options']['copy_fields'] = COPY_FIELDS
    return config


def get_headers(token):
    return {
        'Authorization': f"Token {token}"
    }


def get_params(limit=None):
    params = {
        'format': 'json'
    }
    if limit is not None:
        params['limit'] = limit
    return params


def get_submissions(url, params, headers):
    def get_submissions_rec(results=[], url=None):
        if 'fields' not in url:
            res = requests.get(
                url=url,
                params=params,
                headers=headers
            )
            res.raise_for_status()
        else:
            res = requests.get(url=url, headers=headers)
            res.raise_for_status()
        data = res.json()
        results += data['results']
        next_ = data['next']

        if next_ is not None:
            get_submissions_rec(results, next_)
    
    results = []
    get_submissions_rec(results=results, url=url)
    return results


def get_asset_versions(config):
    res = requests.get(
        url=f"{config['kf_url']}/api/v2/assets/{config['asset_uid']}.json",
        headers=get_headers(config['token'])
    )
    res.raise_for_status()
    asset_data = res.json()

    asset_name = asset_data['name']
    deployed_versions = asset_data['deployed_versions']['results']

    asset_versions = []
    for i, dp in enumerate(reversed(deployed_versions)):
        if config['versions'] and dp['uid'] not in config['versions']:
            continue
        res = requests.get(
            url=dp['url'],
            headers=get_headers(config['token']),
        )
        res.raise_for_status()
        asset_content = res.json()['content']
        asset_versions.append({
            'version': dp['uid'],
            'content': asset_content
        })

    return asset_name, asset_versions


def main():
    config = get_config()
    submissions = get_submissions(
        url=f"{config['kf_url']}/api/v2/assets/{config['asset_uid']}/data.json",
        params=get_params(config['limit']),
        headers=get_headers(config['token'])
    )
    # breakpoint()
    asset_name, asset_versions = get_asset_versions(config)
    pack = FormPack(
        versions=asset_versions,
        title=asset_name,
        id_string=config['asset_uid']
    )
    # breakpoint()
    options = {
        **config['options'],
        'versions': pack.versions.keys()
    }

    export = pack.export(**options)

    filename = "{asset_uid}-{dt}.xlsx".format(
        asset_uid=config['asset_uid'],
        dt=str(datetime.now()).replace(' ', '_')
    )
    export.to_xlsx(
        filename=filename,
        submissions=submissions
    )


if __name__  == '__main__':
    main()