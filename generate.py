#!/usr/bin/env python3

"""Generate package.json with all npm packages as dependencies"""

import json
import datetime
import urllib3

# Alt: https://skimdb.npmjs.com/registry/_all_docs
URL = "https://replicate.npmjs.com/_all_docs"

# npm package.json as a dict
PACKAGE_JSON = {
    "name": "everything-npm",
    # Use current date for version
    "version": f"{datetime.datetime.now():%Y.%m.%d}",
    "description": "Install every single npm packages",
    "main": "index.js",
    "scripts": {
        "test": 'echo "Error: no test specified" && exit 1',
    },
    "repository": {
        "type": "git",
        "url": "https://github.com/xiaoyu2006/everything-npm.git",
    },
    "author": [
        {
            "name": "Yi Cao",
            "email": "me@ycao.top",
            "url": "https://ycao.top",
        }
    ],
    "keywords": [
        "npm",
        "everything",
    ],
    "license": "MIT",
    "bugs": {
        "url": "https://github.com/xiaoyu2006/everything-npm/issues",
    },
    "homepage": "https://github.com/xiaoyu2006/everything-npm",
}


def fetch(url: str) -> str:
    """Fetch data from url, enabling brotli compression"""
    http = urllib3.PoolManager()
    r = http.request("GET", url, headers={"Accept-Encoding": "br"})
    return r.data.decode("utf-8")


def to_dependencies(json: dict) -> dict[str, str]:
    """Convert json to dependencies dict"""
    rows = json["rows"]
    result = {}
    for row in rows:
        name = row["key"]
        result[name] = "*"
    return result


def main():
    """Main entry"""
    data = fetch(URL)
    json_data = json.loads(data)
    print(f"Total packages: {json_data['total_rows']}")
    PACKAGE_JSON["dependencies"] = to_dependencies(json_data)
    with open("package.json", "w") as f:
        json.dump(PACKAGE_JSON, f)


if __name__ == "__main__":
    main()
