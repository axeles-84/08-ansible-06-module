#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Creates a text file with the given content
description:
  - Creates a text file at the path specified by I(path)
    with the content specified by I(content).
options:
  path:
    description: Absolute path to the file on the remote host.
    required: true
    type: str
  content:
    description: Content to write to the file.
    required: true
    type: str
author:
  - Your Name
'''

EXAMPLES = r'''
- name: Create test file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/example.txt
    content: "Hello, world!\n"
'''

RETURN = r'''
path:
  description: Path to the created file.
  type: str
  returned: always
  sample: /tmp/example.txt
'''

from ansible.module_utils.basic import AnsibleModule
import os


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='str', required=True),
            content=dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )

    path = module.params['path']
    content = module.params['content']
    changed = False

    file_exists = os.path.exists(path)
    current_content = None

    if file_exists and os.path.isfile(path):
        try:
            with open(path, 'r') as f:
                current_content = f.read()
        except IOError:
            current_content = None

    if not file_exists or current_content != content:
        changed = True
        if not module.check_mode:
            try:
                parent = os.path.dirname(path)
                if parent and not os.path.isdir(parent):
                    os.makedirs(parent, exist_ok=True)
                with open(path, 'w') as f:
                    f.write(content)
            except IOError as e:
                module.fail_json(msg="Failed to write '%s': %s" % (path, e))

    module.exit_json(changed=changed, path=path)


if __name__ == '__main__':
    main()