#!/usr/bin/env python3.8

import sys,subprocess,os,json


def parser(option):
    result = subprocess.run(['openstack',option,'list','-f','json'],capture_output=True)
    list = json.loads(result.stdout.decode())
    return list


def show_options(list):
    num = 1
    show_string = ""
    for l in list:
        show_string = show_string + 'option ' + str(num) + ')\n'
        for k,v in l.items():
            show_string = show_string + k + ': ' + str(v) + '\n'
        show_string = show_string + '\n'
        num = num + 1
    print(show_string)

mandatory = ['flavor','image','network']
options = ['flavor','image','keypair','security group','network']
command = ['openstack','server','create']

for o in options:
    list = parser(o)
    show_options(list)
    choose = False
    while not choose:
        if o not in mandatory:
            i = input("Enter your option for " + o + ":[Default] ")
        else:
            i = input("Enter your option for " + o + ": ")
        if i.isdigit() and int(i) <= len(list):
            if o == 'security group':
                command.append("--" + 'security-group')
            elif o == 'keypair':
                command.append("--" + 'key-name')
            else:
                command.append("--" + o)
            if o == 'keypair':
                command.append(list[int(i)-1]["Name"])
            else:
                command.append(list[int(i)-1]["ID"])
            choose = True
            print('******************************************************')
        elif i == '' and o not in mandatory:
            choose = True
            print('******************************************************')
            continue
        else:
            print('Invalid input!')

name = input("Enter name of the server: ")
while name == '':
    name = input("Enter name of the server: ")
command.append(name)

print(" ".join(command))
result = subprocess.run(command)








