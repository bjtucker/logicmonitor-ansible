from setuptools import setup

setup(name='logicmonitor_ansible',
      version='1.0.0',
      description='LogicMonitor for Ansible Module',
      long_description='LogicMonitor is a cloud-based, full stack, IT \
          infrastructure monitoring solution that allows you to manage your \
          infrastructure from the cloud. This module provides easy \
          integration with Ansible playbooks.',
      url='https://github.com/logicmonitor/logicmonitor-ansible',
      keywords='LogicMonitor cloud monitoring infrastructure ansible',
      author='LogicMonitor',
      author_email='jeff.wozniak@logicmonitor.com',
      license='MIT',
      packages=['logicmonitor_ansible'],
      install_requires=[],
      zip_safe=False)
