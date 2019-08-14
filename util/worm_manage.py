import os
import sys
import requests
import paramiko


def send_command(ip, user, passwd, command):
    pass


def get_ip(username):
    url = "https://www.stem-iaa.org/vm/ip/" + username
    request = requests.get(url=url)
    data = request.json()
    if data["error"]:
        raise Exception(data["error"])
    return data["ip"]


if __name__ == '__main__':
    admin_username = sys.argv[1]
    admin_password = sys.argv[2]
    accounts_file_path = sys.argv[3]
    execute_file_path = sys.argv[4]

    accounts_file = open(accounts_file_path, "r")
    accounts_file.readline()

    for line in accounts_file:
        line_split = [item.strip() for item in line.split(",")]
        first_name = line_split[0]
        last_name = line_split[1]
        username = line_split[2]
        try:
            ip = get_ip(username)
            if ip:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                ssh_client.connect(hostname=ip, username=admin_username, password=admin_password)

                ftp_client = ssh_client.open_sftp()
                ftp_client.put(execute_file_path, "worm_execute.sh")
                ftp_client.close()

                print("\nVM: " + username)
                stdin, stdout, stderr = ssh_client.exec_command("sudo bash ./worm_execute.sh", get_pty=True)
                stdin.write(admin_password + "\n")
                print("STDOUT")
                print(stdout.read().decode("utf-8"))
                print("STDERR")
                print(stderr.read().decode("utf-8"))
                print("---------------------------------------------------\n")
            else:
                print("vm for " + username + " is offline.")
        except Exception as e:
            print(e)

