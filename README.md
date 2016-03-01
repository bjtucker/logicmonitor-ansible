# logicmonitor module

Ansible module to allow control of your LogicMonitor account via
Ansible PlayBooks.

### Installation
To install this module, place it the configured Ansible library directory.
This directory can be configured by editing ansible.cfg and setting
```
library = [path/to/library/folder]
```
This directory can also be configured by setting the ANSIBLE_LIBRARY
environment variable.
```
export ANSIBLE_LIBRARY=~/ansible-modules-core:~/ansible-modules-extras[path/to/library/folder]
```

### Ansible Module Specifications

```
module: logicmonitor
short_description: Manage your LogicMonitor account through Ansible Playbooks
description:
    - LogicMonitor is a hosted, full-stack,
      infrastructure monitoring platform.
    - This module manages hosts, host groups, and collectors within your
      LogicMonitor account.
version_added: "2.1"
author: Ethan Culler-Mayeno, Jeff Wozniak
notes: You must have an existing LogicMonitor account for this module to      
       function.
requirements:
    - An existing LogicMonitor account
    - Currently supported operating systems:
        - Linux
options:
    target:
        description:
            - The type of LogicMonitor object you wish to manage.
            - "Collector" Perform actions on a LogicMonitor collector
            - "Host" Perform actions on a host device
            - "Hostgroup"  Perform actions on a LogicMonitor host group
            - NOTE Host and Hostgroup tasks should always be performed via
              local_action. There are no benefits to running these tasks on
              the remote host and doing so will typically cause problems.
            - NOTE Collector tasks require superuser access for
              starting/stopping services. Be sure to run these tasks as root
              or set 'become: yes' for the task.
        required: true
        default: null
        choices: ['collector', 'host', 'datasource', 'hostgroup']
        version_added: "1.0"
    action:
        description:
            - The action you wish to perform on target
            - "Add" Add an object to your LogicMonitor account
            - "Remove" Remove an object from your LogicMonitor account
            - "Update" Update properties, description, or groups
              (target=host) for an object in your LogicMonitor account
            - "SDT" Schedule downtime for an object in your
              LogicMonitor account
        required: true
        default: null
        choices: ['add', 'remove', 'update', 'sdt']
        version_added: "1.0"
    company:
        description:
            - The LogicMonitor account company name. If you would log in to
              your account at "superheroes.logicmonitor.com" you would
              use "superheroes"
        required: true
        default: null
        choices: null
        version_added: "1.0"
    user:
        description:
            - A LogicMonitor user name. The module will authenticate and
              perform actions on behalf of this user
        required: true
        default: null
        choices: null
        version_added: "1.0"
    password:
        description:
            - The password of the specified LogicMonitor user
        required: true
        default: null
        choices: null
        version_added: "1.0"
    collector:
        description:
            - The fully qualified domain name of a collector in your
              LogicMonitor account.
            - This is required for the creation of a LogicMonitor host
              (target=host action=add)
            - This is required for updating, removing or scheduling downtime
              for hosts if 'displayname' isn't specified
              (target=host action=update action=remove action=sdt)
        required: false
        default: null
        choices: null
        version_added: "1.0"
    hostname:
        description:
            - The hostname of a host in your LogicMonitor account, or the
              desired hostname of a device to manage.
            - Optional for managing hosts (target=host)
        required: false
        default: 'hostname -f'
        choices: null
        version_added: "1.0"
    displayname:
        description:
            - The display name of a host in your LogicMonitor account or the
              desired display name of a device to manage.
            - Optional for managing hosts (target=host)
        required: false
        default: 'hostname -f'
        choices: null
        version_added: "1.0"
    description:
        description:
            - The long text description of the object in your
              LogicMonitor account
            - Optional for managing hosts and host groups
              (target=host or target=hostgroup; action=add or action=update)
        required: false
        default: ""
        choices: null
        version_added: "1.0"
    properties:
        description:
            - A dictionary of properties to set on the LogicMonitor
              host or host group.
            - Optional for managing hosts and host groups  
              (target=host or target=hostgroup; action=add or action=update)
            - This parameter will add or update existing properties in your
              LogicMonitor account or
        required: false
        default: {}
        choices: null
        version_added: "1.0"
    groups:
        description:
            - A list of groups that the host should be a member of.
            - Optional for managing hosts
              (target=host; action=add or action=update)
        required: false
        default: []
        choices: null
        version_added: "1.0"
    id:
        description:
            - ID of the datasource to target
            - >
                Required for management of LogicMonitor datasources
                (target=datasource)
            required: false
            default: null
            choices: null
            version_added: "2.1"
    fullpath:
        description:
            - The fullpath of the host group object you would like to manage
            - Recommend running on a single Ansible host
            - Required for management of LogicMonitor host groups
              (target=hostgroup)
        required: false
        default: null
        choices: null
        version_added: "1.0"
    alertenable:
        description:
            - A boolean flag to turn alerting on or off for an object
            - Optional for managing all hosts (action=add or action=update)
        required: false
        default: true
        choices: [true, false]
        version_added: "1.0"
    starttime:
        description:
            - The time that the Scheduled Down Time (SDT) should begin
            - Optional for managing SDT (action=sdt)
            - Y-m-d H:M
        required: false
        default: Now
        choices: null
        version_added: "1.0"
    duration:
        description:
            - The duration (minutes) of the Scheduled Down Time (SDT)
            - Optional for putting an object into SDT (action=sdt)
        required: false
        default: 30
        choices: null
        version_added: "1.0"
```

### Additional info
While Ansible may consider a given parameter optional for the purposes of
executing the LogicMonitor module, additional parameters may be required for a
particular target action. For convenience, those additional requirements are
documented below.
```
Target: Collector
    Action: Add
    Available OPTIONAL parameters:
        alertenable

    Action: sdt
        Available OPTIONAL parameters:
            starttime
            duration

Target: Host
    Action: Add
        Additional REQUIRED parameters:
            collector

        Available OPTIONAL parameters:
            hostname
            displayname
            description
            properties
            groups
            alertenable

    Action: Remove
        Available OPTIONAL parameters:
            hostname
            displayname
            collector (REQUIRED if displayname not specified)

    Action: Update

        Available OPTIONAL parameters:
            hostname
            displayname
            collector (REQUIRED if displayname not specified)
            description
            properties
            groups
            alertenable

    Action: sdt
        Available OPTIONAL parameters:
            hostname
            displayname
            collector (REQUIRED if displayname not specified)
            starttime
            duration

Target: Hostgroup
    Action: Add
        Additional REQUIRED parameters:
            fullpath

        Available OPTIONAL parameters:
            properties
            description
            alertenable

    Action: Remove
        Additional REQUIRED parameters:
            fullpath

    Action: Update
        Additional REQUIRED parameters:
            fullpath

        Available OPTIONAL parameters:
            properties
            description
            alertenable


    Action: sdt
        Additional REQUIRED parameters:
            fullpath

        Available OPTIONAL parameters:
            starttime
            duration
```

# Examples
# example of adding a new LogicMonitor collector to these devices
```
---
- hosts: collectors
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: Deploy/verify LogicMonitor collectors
    become: yes
    logicmonitor:
        target=collector
        action=add
        company={{ company }}
        user={{ user }}
        password={{ password }}
```

#example of adding a list of hosts into monitoring
```
---
- hosts: hosts
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: Deploy LogicMonitor Host
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=host
        action=add
        collector='mycompany-Collector'
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        groups="/servers/production,/datacenter1"
        properties="{'snmp.community':'commstring','dc':'1', 'type':'prod'}"
```

#example of putting a datasource in SDT
```
---
- hosts: localhost
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: SDT a datasource
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=datasource
        action=sdt
        id='123'
        duration=3000
        starttime='2017-03-04 05:06'
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
```

#example of creating a hostgroup
```
---
- hosts: localhost
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: Create a host group
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=hostgroup
        action=add
        fullpath='/servers/development'
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        properties="{'snmp.community':'commstring', 'type':'dev'}"
```

#example of putting a list of hosts into SDT
```
---
- hosts: hosts
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: SDT hosts
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=host
        action=sdt
        duration=3000
        starttime='2016-11-10 09:08'
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        collector='mycompany-Collector'
```

#example of putting a host group in SDT
```
---
- hosts: localhost
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: SDT a host group
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=hostgroup
        action=sdt
        fullpath='/servers/development'
        duration=3000
        starttime='2017-03-04 05:06'
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
```

#example of updating a list of hosts
```
---
- hosts: hosts
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: Update a list of hosts
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=host
        action=update
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        collector='mycompany-Collector'
        groups="/servers/production,/datacenter5"
        properties="{'snmp.community':'commstring','dc':'5'}"
```

#example of updating a hostgroup
```
---
- hosts: hosts
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: Update a host group
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=hostgroup
        action=update
        fullpath='/servers/development'
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        properties="{'snmp.community':'newcomm', 'type':'dev', 'status':'test'}"
```

#example of removing a list of hosts from monitoring
```
---
- hosts: hosts
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: Remove LogicMonitor hosts
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=host
        action=remove
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        collector='mycompany-Collector'
```

#example of removing a host group
```
---
- hosts: hosts
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: Remove LogicMonitor development servers hostgroup
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=hostgroup
        action=remove
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        fullpath='/servers/development'
  - name: Remove LogicMonitor servers hostgroup
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=hostgroup
        action=remove
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        fullpath='/servers'
  - name: Remove LogicMonitor datacenter1 hostgroup
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=hostgroup
        action=remove
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        fullpath='/datacenter1'
  - name: Remove LogicMonitor datacenter5 hostgroup
    # All tasks except for target=collector should use local_action
    local_action: >
        logicmonitor
        target=hostgroup
        action=remove
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        fullpath='/datacenter5'
```

### example of removing a new LogicMonitor collector to these devices
```
---
- hosts: collectors
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: Remove LogicMonitor collectors
    become: yes
    logicmonitor:
        target=collector
        action=remove
        company={{ company }}
        user={{ user }}
        password={{ password }}
```

#complete example
```
---
- hosts: localhost
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: Create a host group
    local_action: >
        logicmonitor
        target=hostgroup
        action=add
        fullpath='/servers/production/database'
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        properties="{'snmp.community':'commstring'}"
  - name: SDT a host group
  local_action: >
    logicmonitor
    target=hostgroup
    action=sdt
    fullpath='/servers/production/web'
    duration=3000
    starttime='2012-03-04 05:06'
    company='{{ company }}'
    user='{{ user }}'
    password='{{ password }}'

- hosts: collectors
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: Deploy/verify LogicMonitor collectors
    logicmonitor:
        target: collector
        action: add
        company: {{ company }}
        user: {{ user }}
        password: {{ password }}
  - name: Place LogicMonitor collectors into 30 minute Scheduled downtime
    logicmonitor: target=collector action=sdt company={{ company }}
        user={{ user }} password={{ password }}
  - name: Deploy LogicMonitor Host
    local_action: >
        logicmonitor
        target=host
        action=add
        collector=agent1.ethandev.com
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        properties="{'snmp.community':'commstring', 'dc':'1'}"
        groups="/servers/production/collectors, /datacenter1"

- hosts: database-servers
  remote_user: '{{ username }}'
  vars:
    company: 'mycompany'
    user: 'myusername'
    password: 'mypassword'
  tasks:
  - name: deploy logicmonitor hosts
    local_action: >
        logicmonitor
        target=host
        action=add
        collector=monitoring.dev.com
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
        properties="{'snmp.community':'commstring', 'type':'db', 'dc':'1'}"
        groups="/servers/production/database, /datacenter1"
  - name: schedule 5 hour downtime for 2012-11-10 09:08
    local_action: >
        logicmonitor
        target=host
        action=sdt
        duration=3000
        starttime='2012-11-10 09:08'
        company='{{ company }}'
        user='{{ user }}'
        password='{{ password }}'
```
