import sys
from pushover import Client

def write_stdout(s):
    # only eventlistener protocol messages may be sent to stdout
    sys.stdout.write(s)
    sys.stdout.flush()

def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()

def main():
    client = Client("<user-key>", api_token="<api-token>")
    while 1:
        # transition from ACKNOWLEDGED to READY
        write_stdout('READY\n')

        # read header line and print it to stderr
        line = sys.stdin.readline()
        # read event payload and print it to stderr
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len']))
        data_dic = dict([ x.split(':') for x in data.split()])
        group_name = data_dic.get('groupname')
        process_name = data_dic.get('processname')
        pid = data_dic.get('pid')
        from_state = data_dic.get('from_state')
        message = "{} with the pid {} just stopped.".format(process_name, pid)
        client.send_message(message, title=group_name)

        # transition from READY to ACKNOWLEDGED
        write_stdout('RESULT 2\nOK')

if __name__ == '__main__':
    main()
