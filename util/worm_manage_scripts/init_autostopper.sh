
cd /home/stemiaa/
git clone https://github.com/stem-iaa/AutoStopper.git
cd AutoStopper

echo "$1" > vm_name.txt;

cp autostopper.service /etc/systemd/system/.

systemctl enable autostopper.service
systemctl start autostopper.service
