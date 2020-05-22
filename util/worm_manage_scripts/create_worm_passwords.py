import os

if __name__ == '__main__':
    accounts_file = open("roster.csv", "r")
    accounts_file.readline()

    for line in accounts_file.readlines():
        line_split = [item.strip() for item in line.split(",")]
        username = line_split[2]
        worm_pass = line_split[4]

        os.system('echo -e "' + worm_pass + '\n' + worm_pass + '" | passwd "' + username + '";')
