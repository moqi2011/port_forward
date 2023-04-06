import os
import sys
from subprocess import check_output


def is_windows():
    return os.name == 'nt'


charset = 'GBK' if is_windows() else 'utf-8'


def del_(la, lp):
    if is_windows():
        cmd = f'netsh interface portproxy delete v4tov4 listenaddress={la} listenport={lp}'
        print(cmd)
        print(check_output(cmd, shell=True).decode(charset))


def add_(la, lp, ca, cp):
    if is_windows():
        cmd = f'netsh interface portproxy add v4tov4 listenaddress={la} listenport={lp}  connectaddress={ca} connectport={cp}'
        print(cmd)
        print(check_output(cmd, shell=True).decode(charset))


def show_():
    if is_windows():
        print(check_output('netsh interface portproxy show all', shell=True).decode(charset).strip())


def clean_():
    if is_windows():
        lines = check_output('netsh interface portproxy show all', shell=True).decode(charset).splitlines()
        for line in lines:
            l = line.split()
            if len(l) == 4 and l[3].isnumeric():
                del_(l[0], l[1])


def main():
    # TODO check permissions

    if len(sys.argv) < 2:
        print('''\
port_forward Usage:
listenaddress defalut value: 0.0.0.0

add:
    port_forward [listenaddress:]listenport connectaddress[:connectport]

del:
    port_forward clean
    port_forward [listenaddress:]listenport\
        ''')
        show_()
        return
    if sys.argv[1] == 'clean':
        clean_()
        show_()
        return

    listen = sys.argv[1].split(":")
    la = '0.0.0.0' if len(listen) else listen[0]
    lp = listen[-1]

    if len(sys.argv) < 3:
        del_(la, lp)
    else:
        connectad = sys.argv[2].split(":")
        ca = connectad[0]
        cp = lp if len(connectad) == 1 else connectad[-1]
        add_(la, lp, ca, cp)

    show_()


if __name__ == '__main__':
    main()
