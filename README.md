logicmonitor-ansible
====================

Ansible module to allow control of your LogicMonitor account via Ansible PlayBooks.

---
module: logicmonitor
short_description: Manage your LogicMonitor account through Ansible Playbooks
description:
    - LogicMonitor is a hosted, full-stack, infrastructure monitoring platform.
    - This module manages hosts, host groups, and collectors within your LogicMonitor account.
version_added: "1.0"
author: Ethan Culler-Mayeno
notes: You must have an existing LogicMonitor account for this module to function.
requirements:
    - An existing LogicMonitor account
    - Currently supported operating systems:
        - Linux
options:
    target:
        description:
            - The LogicMonitor object you wish to manage.
        required: true
        default: null
        choices: ['collector', 'host', 'hostgroup']
        version_added: "1.0"
    action:
        description:
            - The action you wish to perform on target
        required: true
        default: null
        choices: ['add', 'remove', 'sdt']
        version_added: "1.0"
    company:
        description:
            - The LogicMonitor account company name. If you would log in to your account at "superheroes.logicmonitor.com" you would use "superheroes"
        required: true
        default: null
        choices: null
        version_added: "1.0"
    user:
        description:
            - A LogicMonitor user name. The module will authenticate and perform actions on behalf of this user
        required: true 
        default: null
        choices: null
        version_added: "1.0"
    password:
        description:
            - The password or md5 hash of the password for the chosen LogicMonitor User
            - If an md5 hash is used, the digest flag must be set to true
        required: true
        default: null
        choices: null
        version_added: "1.0"
    digest:
        description:
            - Boolean flag to tell the module to treat the password as plaintext or md5 digest
            - If an md5 hash is used, the digest flag must be set to true
        required: false
        default: false
        choices: [true, false]
        version_added: "1.0"
    collector:
        description:
            - The fully qualified domain name of a collector in your LogicMonitor account.
            - This is required for the creation of a LogicMonitor host (target=host action=add)
        required: false
        default: null
        choices: null
        version_added: "1.0"
    hostname:
        description:
            - The hostname of a host in your LogicMonitor account, or the desired hostname of a device to add into monitoring.
            - Required for managing hosts (target=host)
        required: false
        default: 'hostname -f'
        choices: null
        version_added: "1.0"
    displayname:
        description:
            - the display name of a host in your LogicMonitor account or the desired display name of a device to add into monitoring.
        required: false
        default: 'hostname -f'
        choices: null
        version_added: "1.0"
    description:
        description:
            - The long text description of the object in your LogicMonitor account
            - Used when managing hosts and host groups (target=host or target=hostgroup)
        required: false
        default: ""
        choices: null
        version_added: "1.0"
    properties:
        description:
            - A dictionary of properties to set on the LogicMonitor host or hostgroup.
            - Used when managing hosts and host groups (target=host or target=hostgroup)
            - This module will overwrite existing properties in your LogicMonitor account
        required: false
        default: {}
        choices: null
        version_added: "1.0"
    groups:
        description:
            - The set of groups that the host should be a member of.
            - Used when managing LogicMonitor hosts (target=host)
        required: false
        default: []
        choices: null
        version_added: "1.0"
    fullpath:
        description:
            - The fullpath of the hostgroup object you would like to manage
            - Recommend running on a single ansible host
            - Required for management of LogicMonitor host groups (target=hostgroup) 
        required: false
        default: null
        choices: null
        version_added: "1.0"
    alertenable:
        description:
            - A boolean flag to turn on and off alerting for an object
        required: false
        default: true
        choices: [true, false]
        version_added: "1.0"
    starttime:
        description:
            - The starttime for putting an object into Scheduled Down Time (maintenance mode)
            - Required for putting an object into SDT (action=sdt)
        required: false
        default: null
        choices: null
        version_added: "1.0"
    duration:
        description:
            - The duration (minutes) an object should remain in Scheduled Down Time (maintenance mode)
            - Required for putting an object into SDT (action=sdt)
        required: false
        default: 30
        choices: null
        version_added: "1.0"

Examples
#example of adding a new LogicMonitor collector to these devices
```
---

- hosts: collectors
  user: root
  vars:
    company: 'yourcompany'
    user: 'mario'
    password: 'itsame.Mario!'
    digest: False
  tasks:
  - name: Deploy/verify LogicMonitor collectors
    logicmonitor: target=collector action=add company={{ company }} user={{ user }} password={{ password }}
```

#example of adding a host into monitoring
```
---
- hosts: collectors
  user: root
  vars:
    company: 'yourcompany'
    user: 'mario'
    password: 'itsame.Mario!'
    digest: False
  tasks:
  - name: Deploy LogicMonitor Host
    local_action:
      logicmonitor:
        target: host
        action: add
        collector: agent1.ethandev.com
        company: '{{ company }}'
        user: '{{ user }}'
        password: '{{ password }}'
        properties:
          snmp.community: 'n3wc0mm'
        groups:
          - '/test/asdf'
          - '/ans/ible'
```

#sdt a host
```
- hosts: hosts
  user: root
  vars:
    company: 'youcompany'
    user: 'Luigi'
#    password: 'ImaLuigi,number1!'
    password: 'c82dbb33bef9e7382b9f39c2233a458b'
    digest: True
  tasks:
  - name: schedule 5 hour downtime for 2012-11-10 09:08
    logicmonitor:
      target: host
      action: sdt
      duration: 3000
      starttime: '2012-11-10 09:08'
      company: '{{ company }}'
      user: '{{ user }}'
      password: '{{ password }}'
```

#example of creating a hostgroup
```
- hosts: somemachine.superheroes.com
  user: root
  vars:
    company: 'yourcompany'
    user: 'mario'
    password: 'itsame.Mario!'
    digest: False
  tasks:
  - name: Create a host group
    logicmonitor:
      target: hostgroup
      action: add
      fullpath: '/worst/name/ever'
      company: '{{ company }}'
      user: '{{ user }}'
      password: '{{ password }}'
      properties:
        snmp.community: 'n3wc0mm'
```'

#example of putting a hostgroup in SDT
```
- hosts: somemachine.superheroes.com
  user: root
  vars:
    company: 'yourcompany'
    user: 'mario'
    password: 'itsame.Mario!'
    digest: False
  tasks:
  - name: SDT a host group
    logicmonitor:
      target: hostgroup
      action: sdt
      fullpath: '/arrays'
      duration: 3000
      starttime: '2012-03-04 05:06'
      company: '{{ company }}'
      user: '{{ user }}'
      password: '{{ password }}'
```

#complete example
```
---
- hosts: somemachine.superheroes.com
  user: root
  vars:
    company: 'yourcompany'
    user: 'mario'
    password: 'itsame.Mario!'
    digest: False
  tasks:
  - name: Create a host group
    logicmonitor:
      target: hostgroup
      action: add
      fullpath: '/worst/name/ever'
      company: '{{ company }}'
      user: '{{ user }}'
      password: '{{ password }}'
      properties:
        snmp.community: 'n3wc0mm'
  - name: SDT a host group
    logicmonitor:
      target: hostgroup
      action: sdt
      fullpath: '/arrays'
      duration: 3000
      starttime: '2012-03-04 05:06'
      company: '{{ company }}'
      user: '{{ user }}'
      password: '{{ password }}'
      
- hosts: collectors
  user: root
  vars:
    company: 'yourcompany'
    user: 'mario'
    password: 'itsame.Mario!'
    digest: False
  tasks:
  - name: Deploy/verify LogicMonitor collectors
    logicmonitor: target=collector action=add company={{ company }} user={{ user }} password={{ password }}
  - name: Place LogicMonitor collectors into 30 minute Scheduled downtime
    logicmonitor: target=collector action=sdt company={{ company }} user={{ user }} password={{ password }}
  - name: Deploy LogicMonitor Host
    local_action:
      logicmonitor:
        target: host
        action: add
        collector: agent1.ethandev.com
        company: '{{ company }}'
        user: '{{ user }}'
        password: '{{ password }}'
        properties:
          snmp.community: 'n3wc0mm'
        groups:
          - '/test/asdf'
          - '/ans/ible'

- hosts: hosts
  user: root
  vars:
    company: 'youcompany'
    user: 'Luigi'
#    password: 'ImaLuigi,number1!'
    password: 'c82dbb33bef9e7382b9f39c2233a458b'
    digest: True
  tasks:
  - name: deploy logicmonitor hosts
    logicmonitor:
      target: host
      action: add
      collector: rock.ethandev.com
      company: '{{ company }}'
      user: '{{ user }}'
      password: '{{ password }}'
      properties:
        snmp.community: 'newcomm'
      groups:
        - '/test/asdf'
        - '/ans/ible'
  - name: schedule 5 hour downtime for 2012-11-10 09:08
    logicmonitor:
      target: host
      action: sdt
      duration: 3000
      starttime: '2012-11-10 09:08'
      company: '{{ company }}'
      user: '{{ user }}'
      password: '{{ password }}'

```