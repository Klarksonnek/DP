#!/usr/bin/env bash

rm -rf /opt/notifier

mkdir /opt/notifier
mkdir /opt/notifier/env_dp
cp -r ../env_dp/*.py /opt/notifier/env_dp/.

mkdir /opt/notifier/notifier
cp co2-notifier.py /opt/notifier/notifier/co2_notifier.py

cp co2-notifier.desktop /usr/share/applications/.
update-desktop-database
