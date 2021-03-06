import paramiko
import time
import argparse
import logging

from multiprocessing import Pool

logging.basicConfig()

class Engine(object):
    file_path = None
    target = ''
    userlist = ['root']
    calc_times = []

    req_time = 0.0
    num_pools = 10

    def __init__(self, target, filepath=None, req_time=0.0):
        self.req_time = req_time
        self.target = target
        self.file_path = filepath
        if self.file_path:
            self.load_users(filepath)

    def load_users(self, filepath):
        data = []
        with open(filepath, 'r') as f:
            data = f.read().splitlines()
        self.userlist = data

    def execute(self):
        for user in self.userlist:
            self.attack(user)

    def attack(self, user):
        # TODO Add the CVE-2016-6210 code here
        # Unix quirk: Replace time.clock() with time.time()
        ssh = paramiko.SSHClient()
        total = 0
        time.sleep(self.req_time)
        ssh.close()

        self.print_results(user, total)

    def print_results(self, user, total):
        self.calc_times.append(total)
        avg = reduce(lambda x, y: x + y, self.calc_times) / len(self.calc_times)
        flag = '*' if total > avg else ''
        print('%s:\t\t%s\t%s' % (user, total, flag))

def main(ip_addr, filename=None, req_time=0.0):
    if ip_addr == '' or not ip_addr:
        print('No target IP specified')
        return
    if filename == '':
        filepname = None
    engine = Engine(target=ip_addr, filepath=filename, req_time=req_time)
    engine.execute()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple automated script for CVE 2016-6210 -- OpenSSHD 7.2p2 >= version')
    parser.add_argument('ip', help='[Required] The IP of the target server')
    parser.add_argument('-u', '--userlist', help='Specify a filepath with a list of usernames to try -- one username per line')
    parser.add_argument('-t', '--time', help='Set the time between requests (in seconds)')

    ip_addr = None
    filename = None
    req_time = 0.0
    args = parser.parse_args()

    if args.ip:
        ip_addr = args.ip
    if args.userlist:
        filename = args.userlist
    if args.time:
        req_time = float(args.time)
    main(ip_addr, filename, req_time)
