# Stem-IAA Portal

The Stem-IAA Portal was created to provide a way for students, instructors, and mentors to interact in various ways over the duration of a course. It is meant to supplement an Education Management System, rather than replace it. Importantly, however, mentors of the course do not have access to the EMS, and thus features are provided in the portal to assist with this.

The following topics are discussed in this documentation:

- [Portal setup](#portal-setup)
- [Portal usage guide](#portal-usage)
- [Flask/static hosting information](#hosting-information)
- [Virtual machine information](#virtual-machines)


## Portal Setup

Before running, create a new file `config.json` in the root directory for the project. In this file, provide the following information:

- "secret": A complex random value sent to the flask app for cryptography.
- "SQLALCHEMY_DATABASE_URI": The URI pointing to the database to use for the portal. Example: `sqlite:///worm.db`
- "azure": A new dictionary with the following values found in the azure account:
    - "client_id"
    - "secret"
    - "tenant"
    - "subscription_id"

Then, launch the portal via:
```
export FLASK_APP=app.py
flask run --host=0.0.0.0
```

## Portal Usage

Pre-login, the portal serves a single static page describing the content of the course. In future courses, this page and simply be swapped for a page describing a different course. The same login button should be kept, however, which allows students/mentors/instructors to login to their accounts. The initial administrator account can be initialized via the [create admin script](util/create_admin.py). Subsequent accounts can be created on the /register page. This is intended to be performed ahead of time by an administrator; there is no way to create an account without an administrator account, and as such students can not create their own accounts.

After logging in, the user is taken to their `Profile` page. The profile is visible to all other users in their cohort. Visible elements on a profile can be changed by clicking the `Edit` button at the top right, changing the content, and then clicking `Save`. In edit mode, the profile picture can be changed by clicking on it. The `Content` section is intended to be used by students to demonstrate the projects they are creating from the course. However, the content page exists on mentor and instructor accounts as well, in case there are other reasons to use it. To view other profiles, use the search feature in the navbar.

Information set during account creation can also be changed via the username dropdown -> Account option. The settings available to set will change depending on the type of account (student/mentor/instructor). For example, students don't have permission to change their username after it's been assigned. If a locked setting needs to be changed, an administrator can navigate to the student/mentor's profile and click the `Settings` button for the profile at the top right.
 
 The `Course Information` page can be accessed at the top right of the profile page, or in the username dropdown menu. This page is intended for students to view information about the course, such as the login for the EMS, login and hosting information for the applications and static content, and contact information for their instructors/TAs/mentors. Additionally, the page allows students to launch and connect to their virtual machines used for course work. Software downloads are also listed for students working on their own machines locally. These first three pages are the only ones that concern students.
 
 The `Solutions` page allows for instructors to post solutions to coursework and mentors to view the solutions. The posted solutions are protected by account role, and are not viewable by students. If logged into a mentor or instructor account, the solutions page can be viewed via the username dropdown -> Solutions. Solutions are categorized by the cohort they belong to. Solutions are read only for mentors, and read/write for instructors. If logged into an instructor account, a new solution can be added at the top by typing the name of the solution and clicking `Create`. Within a solution, the description for the assignment can be provided and any corresponding source code files can be attached. When viewing the solution, the file can be clicked and a syntax-highlighted preview will display. The file can also be downloaded. Solutions can be removed by instructors by clicking `Delete` in the solutions page for a cohort.
 
 The `Administration` page (username dropdown -> Administration) provides two features: registering new users and managing cohorts.
 
 New users are added in the user registration page. An instructor account must navigate to this page and fill out the information, choose the role, and click `Register User`. There currently is a bug where the role must be pressed each time after adding a user, even if the role appears to be selected. A list of mentors/mentees can be provided at the time of registration, though this can also be added after all of the accounts are set up in each of the user's settings pages.
 
 There is currently no way to delete a user via the interface. This can be done via SQLAlchemy relatively easily, however. For example (relative to the project root directory):
 
 ```python
from model.User import db, User
to_remove = User.query.filter_by(username="sam").first()
db.session.delete(to_remove)
db.session.commit()
```
 
 Cohorts can be added/deleted/managed via the `Manage cohorts` button on the `Administration` page. Existing cohorts are displayed on this page, and can be renamed or deleted. Additionally, an `Is Active` toggle allows a cohort to be removed from view so as to not clutter pages that would otherwise show every enrolled cohort. It is still possible for users to view old cohort information with this toggle checked. A new cohort can be added by typing in a name and clicking `Create` at the top. After clicking on a cohort after it has been created, a page is shown which allows the specific cohort to be managed. On this screen, new users can be added and removed from a cohort. To add a user, start typing their name/username and click it from the autocompleted list. To remove a user, click the x at the top right of their profile picture.
 
 Lastly, the user can logout of their account via the username dropdown -> Logout feature.
 
 
 ## Hosting Information
 
 Several technologies were used to setup the hosting service for students. The goal was to provide each student with a custom domain name associated with their username, such as `sam.w3.stem-iaa.org` for static content, and `sam.flask.stem-iaa.org` for flask specific content, which was the web application framework taught in the course. 
 
 To accomplish this, [openresty](https://openresty.org/en/) (from [nginx](https://www.nginx.com/)) and [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/) were used. Both of these libraries should be installed on the hosting server.
 
 Openresty was chosen over a standard version of nginx due to the added ability to write lua in routing network traffic. This is how the custom URLs were created from the student usernames. The nginx scripts to accomplish this can be found in the [nginx_sites folder of the worm Github repo](https://github.com/stem-iaa/worm/tree/master/nginx_sites). Additionally, custom landing pages were created from each of the routes. The landing pages can be found [here](https://github.com/stem-iaa/worm/tree/master/worm_html).
 
 The nginx setup assumes a uwsgi ini file is created for each user. This has been automated by creating .ini files when a new user is added to the hosting server. The `/usr/local/sbin/adduser.local` was updated to execute the [create_w3.py](https://github.com/stem-iaa/worm/blob/master/create_w3.py) script, which generates ini files for each user in the `w3` group. This script can also be run manually after adding all the users.
 
 For reference, an example of a auto-generated .ini script for a hosted user looks like the following:
 
 ```
[uwsgi]
socket = /tmp/flask_socks/sam.sock
pythonpath = python3
callable = app
vhost = true
py-autoreload = 3
plugins = python3
manage-script-name = true
chdir = /home/sam/www/flask
mount = /=app.py
touch-reload = /home/sam/www/flask_reload
module = app
```
 
The `touch-reload` parameter is enabled so that students can have multiple different flask applications in their www directory in their home folder, and switch the `flask` symlink to the one they want to host at any given time. After doing this, they can execute `touch flask_reload` to have the change be updated on the hosting server. `py-autoreload` is enabled so that they do not have to touch reload when making changes to their existing flask app.
 
 If hosting the portal with nginx/uwsgi, a very similar script as the previous can be created depending on the system-dependent locations. The .ini used for our hosting is provided [here](https://github.com/stem-iaa/worm/blob/master/portal.ini).
 
 ### OpenResty install on Ubuntu
- Install dependencies:
  ```
  apt-get install libpcre3-dev libssl-dev perl make build-essential curl
  ```
- Install OpenResty:
  ```
  wget -qO - https://openresty.org/package/pubkey.gpg | sudo apt-key add -
  sudo apt-get -y install software-properties-common
  sudo add-apt-repository -y "deb http://openresty.org/package/ubuntu $(lsb_release -sc) main"
  sudo apt-get update
  sudo apt-get install openresty
  ```
 
## Virtual Machines
 
 The virtual machines provided to students were slightly modified standard ubuntu machines. The modifications made to these instances are as follows.
 
 First, we provided a method for students to log in to their machines via VNC. We used [TightVNC](https://www.tightvnc.com/) as our VNC server, and [noVNC](https://novnc.com/info.html) as the client that was integrated with the portal. Both of these should be installed on the VM and then set to auto run on startup via the service scripts found in the [vm-setup repo](https://github.com/stem-iaa/vm-setup).
 
 Additionally, we wrote a script to automatically shut down the virtual machines when low cpu usage was deducted. This script can be found in the [AutoStopper repo](https://github.com/stem-iaa/AutoStopper). The threshold for cpu usage should be played with since a good value may be different than what we found on our chosen azure instance. The [autostopper.service](https://github.com/stem-iaa/AutoStopper/blob/master/autostopper.service) script is provided to run the AutoStopper on startup.
 
 The method we used to create the virtual machines was to setup one instance with all of the software (including any applications students will need, such as IDEs/FTP clients, etc), and then clone the instance in azure for each student. After the instances have been created, we used the [worm_manage.py](https://github.com/stem-iaa/portal/blob/master/util/worm_manage.py) script to make further changes. This script iterates over each of the student's VMs and executes a provided bash script. Since the instances are all the same, a method for updating the VMs is to log in to an arbitrary VM, make the change/download an update via the command line, save the bash history to a file and then deploy the script to all other instances via the worm_manage.py script.
 
 ## Virtual Machine Setup
 
 ### Azure Setup
 
Create the instance
- Go to Azure home -> virtual machines
- Click Add
- Create a new resource group
- Enter the machine name and select the desired region
- Select the Debian 9 Image and choose the desired size. D2s_v3 is recommended.
- Choose ‘Password’ as the authentication type
- Enter the desired login credentials

Disk configuration
- At the top, click ‘Disks’ next to ‘Basics’
- Click ‘Create and attach a new disk’
- Choose ‘Standard SSD’ as the disk type
- Enter the desired disk size, at least 30GB is recommended
- Choose ‘None’ as the source type and click ‘OK’

Network configuration
- Click ‘Networking’ at the top
- Choose ‘Advanced’ for the NIC network security group
- Create a new network security group
- Ensure SSH (port 22 TCP) is open, and open it if it isn’t
- Add inbound rule. This will be the port for VNC connections
- Choose the following:
  - Source: any
  - Source port ranges: *
  - Destination: any
  - Destination port ranges: 5901
- The rest can be left except the name, which can be changed to 5901
- Do the same for port 80, if desired (for HTTP servers)
- Click ‘Add’
- Click ‘OK’ for the security group

Deploy
- Click ‘Download a template for automation’
- Then click ‘Add to library’
- Click the X at the top right to go back
- Then click ‘Create’

Connecting
- Wait for the server to startup if recently deployed, or click on an instance and then click ‘Start’ if it is stopped
- Click connect at the top left
- Copy the ssh command and enter it into a terminal
- Type the login information provided in the instance setup
- You should then be able to connect to the instance

### VNC Setup

#### Install/setup

- Install the following in a new bash shell:
  ```
  sudo apt-get update
  sudo apt-get install tightvncserver gnome gnome-panel gnome-system-tools xfce4-goodies
  ```
- Then create a new password to login to VNC with:
  ```
  vncserver
  ```
- Then kill the server that was started so it can be configured:
  ```
  vncserver -kill :1
  ```
- Then open ~/.vn/xstartup in an editor
- Comment out /etc/X11/Xsession and add the following:
  ```
  gnome-session --session=gnome-classic
  gnome-panel &
  gnome-settings-daemon &
  metacity &
  nautilus &
  ```
- Then execute `vncserver` again and it should be ready to login to at url:1 (for port 5901)

#### VNC Server Auto Launch on Startup

- Create a new file: /etc/systemd/system/vncserver@.service and add the following:
  ```
  [Unit]
  Description=Start TightVNC server at startup
  After=syslog.target network.target

  [Service]
  Type=forking
  User=sammy
  Group=sammy
  WorkingDirectory=/home/sammy

  PIDFile=/home/sammy/.vnc/%H:%i.pid
  ExecStartPre=-/usr/bin/vncserver -kill :%i > /dev/null 2>&1
  ExecStart=/usr/bin/vncserver -depth 24 -geometry 1280x800 :%i
  ExecStop=/usr/bin/vncserver -kill :%i

  [Install]
  WantedBy=multi-user.target
  ```
- The geometry and depth settings can be changed depending on the internet latency and display resolution of the connecting client
- Then execute the following:
  ```
  sudo systemctl daemon-reload
  sudo systemctl enable vncserver@1.service
  vncserver -kill :1
  sudo systemctl start vncserver@1
  localectl set-locale LANG="en_US.UTF-8"
  ```
- Restart the VM, then connect as usual to port :1

### Student VM Applications

#### Python3
- Python3 is already installed on the Ubuntu image, but pip can be installed via `sudo apt-get install python3-pip`

#### PyCharm Community
- Download pycharm here: https://www.jetbrains.com/pycharm/download/
- Extract the tar.gz
- Navigate to the bin directory in the extracted folder and note the full path to ‘pycharm.sh’
- Navigate to ~/.local/share/applications
- Create a new file called pycharm.desktop and enter the following:
  ```
  [Desktop Entry]
  Name=pycharm
  Exec=/path/to/pycharm/bin/pycharm.sh
  Icon=/path/to/pycharm/bin/pycharm.png
  Terminal=false
  Type=Application
  Categories=Development;
  ```
- Access pycharm via the menu bar or by running pycharm.sh

#### Firefox-esr 
- set www.google.com as home page. Uncheck all other notifications and such): 
  ```
  sudo apt install firefox-esr
  ```

#### Atom
- Open a browser on the VM, go to https://atom.io/ and download the .deb
- `cd` to `~/Downloads` and `sudo apt-get install` the .deb that was downloaded
- Execute the following:
  ```
  cd /usr/lib/x86_64-linux-gnu/
  sudo cp libxcb.so.1 libxcb.so.1.bak
  sudo sed -i 's/BIG-REQUESTS/_IG-REQUESTS/' libxcb.so.1
  ```
- Access Atom via the menu bar or by typing atom in a terminal

#### FileZilla
- Open a browser on the VM and go to https://filezilla-project.org/
- Download the FileZilla client and extract the compressed folder
- Navigate to the FileZilla3 directory and note the full path to it
- Create a new filezilla.desktop file in ~/.local/share/applications and add the following:
  ```
  [Desktop Entry]
  Name=FileZilla
  Exec=/path/to/FileZilla3/bin/filezilla
  Icon=/path/to/FileZilla3/share/icons/hicolor/scalable/apps/filezilla.svg
  Terminal=false
  Type=Application
  Categories=Network;FileTransfer;
  ```
- Open /etc/apt/sources.list and add ‘deb http://ftp.de.debian.org/debian sid main’ to the end
- Then, execute the following:
  ```
  sudo apt-get update
  sudo apt-get upgrade libc6
  ```
- Access FileZilla via the menu bar (under network) or by running the filezilla executable in FileZilla3/bin

#### IDLE3
- Install via ‘sudo apt-get install idle3’
- Set as default application to open .py
- Access IDLE via menu bar or by typing idle in a terminal




  




