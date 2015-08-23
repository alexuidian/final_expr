#!/usr/bin/python
import os
import socket
import pickle
import re
import sys
import datetime

def connect_guest(server):
        s2=socket.socket()
        #if(not connected_host):
        #       return s
        #s=socket.socket()
        port=44445
        s2.connect((server,port))
        #connected_host=1
        return s2

def run_on_guest(cmd,host):

        s2=connect_guest(host)
        cmds=pickle.dumps(cmd)
        s2.send(cmds)
        #while True:
        while True:
                out= s2.recv(8196)
                print out,"\n"

                if(re.search('ENDD.*',out)):
                        break
        s2.close()


def main():

        ls=[]
        s='echo start'
        ls.append(s)
        if(len(sys.argv) > 1):
                for each in sys.argv[1:]:
                        ls.append(each)

        run_on_guest(ls,'10.129.26.249')


if __name__ == '__main__':
        main()

