# RC Mission Commander
RC Mission Commander Software

![test](https://github.com/Electronya/rc-mission-commander/actions/workflows/test.yml/badge.svg)
[![coverage](https://codecov.io/gh/Electronya/rc-mission-commander/branch/develop/graph/badge.svg?token=WEAWM1E3HZ)](https://codecov.io/gh/Electronya/rc-mission-commander)

## Setup
```
git clone git@github.com:Electronya/rc-mission-commander.git
cd rc-mission-commader
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ln -s ../../rc-mission-common/src/pkgs/messages src/pkgs/messages
ln -s ../../rc-mission-common/src/pkgs/mqttClient src/pkgs/mqttClient
```
