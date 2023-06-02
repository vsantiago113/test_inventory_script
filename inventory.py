#!/usr/bin/env python3

import argparse
import json
from typing import List, Dict


class ExampleInventory:
    def __init__(self, _list, _host):
        self.inventory = {
            '_meta': {
                'hostvars': {}
            },
            'all': {
                'children': [
                    'ungrouped'
                ]
            }
        }

    def add_hosts(self, _group: str = None, _hosts: List[str] = None, _vars: Dict = None) -> None:
        _hosts = list() if _hosts is None else _hosts
        _vars = dict() if _vars is None else _vars

        if _group not in self.inventory['all']['children']:
            self.inventory['all'].get('children', list()).append(_group)

        self.inventory.setdefault(_group, {})['hosts'] = _hosts

        for _host in _hosts:
            self.inventory['_meta']['hostvars'][_host] = _vars

    def add_host(self, _group: str = None, _host: str = None, _vars: Dict = None) -> None:
        _vars = dict() if _vars is None else _vars

        if _group not in self.inventory['all']['children']:
            self.inventory['all'].get('children', list()).append(_group)

        self.inventory.setdefault(_group, {})['hosts'] = list()
        if _host not in self.inventory[_group].get('hosts', list()):
            self.inventory[_group].get('hosts', list()).append(_host)

        self.inventory['_meta']['hostvars'][_host] = _vars


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line arguments for Ansible Dynamic Inventory.')
    parser.add_argument('--list', action='store_true', help='Return list of hosts.')
    parser.add_argument('--host', type=str, help='Return the requested host.')
    args = parser.parse_args()

    example_inventory = ExampleInventory(args.list, args.host)

    example_inventory.add_hosts(_group='dbservers', _hosts=['10.0.0.5', '10.0.0.1'], _vars={'http_port': 80})
    example_inventory.add_host(_group='test_group', _host='10.0.0.20', _vars={'type': 'switch'})

    if args.list is True:
        print(json.dumps(example_inventory.inventory))
    elif args.host:
        print(json.dumps(example_inventory.inventory['_meta']['hostvars'].get(args.host, dict())))