from scapy.all import *

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys


x = {"init":0}
time = datetime.now()
exception_word = ["0.0.0.0"]

def main():
    global exception_word
    args = sys.argv
    for i in range(len(args)-1):
        exception_word.append(args[i+1])

    print(exception_word)
    sniff(prn=Sniff_Arp)


def Sniff_Arp(packet):
    frag = 0
    global x
    global exception_word

    for i in range(len(x.keys())):
        try:
            st = str(packet[IP].src)
        except IndexError:
            frag = 1
            print("err")
            break

        if "init"== x.keys()[i]:
            frag = 3

        for j in range(len(exception_word)):
            if exception_word[j] == st:
                frag = 2

        if st == x.keys()[i] and frag != 2:
            frag = 1
            x[st] += 1

    if frag == 0 or frag == 3:
        x[st] = 1
        if frag == 3:
            x.pop("init")



    timenow = datetime.now()
    global time
    if abs(timenow - time) >= timedelta(seconds=2):
        l = np.array([])
        h = np.array([])
        la = np.array([])
        for i in range(len(x.keys())):
            l = np.append(l,i+1)
            h = np.append(h,x[x.keys()[i]])
            la = np.append(la,x.keys()[i])
        Map(l,h,la)
        time = timenow


def Map(left_arry,height_harry,label):
    plt.cla()
    left = np.array(left_arry)
    height = np.array(height_harry)
    plt.barh(left, height, tick_label=label, align="center")
    plt.pause(0.0000000001)


if __name__ == '__main__':
    main()
