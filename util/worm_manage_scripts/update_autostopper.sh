cd /home/stemiaa/AutoStopper
git pull

systemctl stop autostopper.service
systemctl disable autostopper.service
systemctl enable autostopper.service
systemctl start autostopper.service
