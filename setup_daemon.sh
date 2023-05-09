#!/bin/sh

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")


if python3.10 --version 2>&1; then
	echo Python 3.10 detected
else
	echo Python 3.10 not found! Exiting...
	exit 1
fi

if [ ! -d "$SCRIPTPATH/.venv/" ]; then
	echo creating python virtual env
	python3.10 -m venv $SCRIPTPATH/.venv
fi

echo Installing dependencies...
$SCRIPTPATH/.venv/bin/python -m pip install -r $SCRIPTPATH/req.txt

echo Creating richiebot service daemon
echo "[Unit]
Description=Richiebot VK daemon service
[Service]
User=root
WorkingDirectory=$SCRIPTPATH
ExecStart=$SCRIPTPATH/.venv/bin/python richiebot.py
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee --append /etc/systemd/system/richiebot.service

echo Reloading systemctl daemon
sudo systemctl daemon-reload

echo Starting a richiebot service
sudo systemctl start richiebot.service

echo Done! Richiebot is running
