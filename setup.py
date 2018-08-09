import os
from setuptools import setup, find_packages
from setuptools.command.install import install


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def config():
    try:
        open('/etc/ilp-agent.conf')
    except IOError:
        with open('/etc/ilp-agent.conf', 'w') as f:
            f.write("[server]"
                    "\nip = 127.0.0.1"
                    "\nport = 8000"
                    "\ndebug = True"
                    "\n[agent]"
                    "\ninterval = 60"
                    )


class InstallCommand(install):
    def run(self):
        config()
        install.run(self)


setup(
    name="ilp_monitoring_agent",
    version="0.0.1",
    author="N3TC4T",
    author_email="netcat.av@gmail.com",
    description="Interledger Peer monitoring agent",
    license="MIT",
    keywords="interledger agent peer monitoring",
    url="http://packages.python.org/ilp_monitor_agent",
    scripts=['bin/ilp-agent'],
    packages=find_packages(),
    install_requires=[
        'requests', 'six',
    ],
    long_description=read('README.md'),
    cmdclass={
        'install': InstallCommand,
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
