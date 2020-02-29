#author: Divas Grover MSEE 2017
#to run this program open terminal in folder containing this program
#write python3.x <Name_of_this_program> <test_file.txt> <wsj-clean.txt>

import sys
from collections import defaultdict

assert (len(sys.argv) == 3),'Error please enter total of three arguments i.e. ...'\
                            'Name of this prog, test file, trainning file'

print("Transition based Dependency Parser by Divas Grover")

test_name = sys.argv[1]
train_name = sys.argv[2]

file_test = open(test_name, 'r')
file_train = open(train_name, 'r')

data_test = file_test.read()
data_train = file_train.read()

file_train.close()
file_test.close()

list_train = data_train.split("\n\n")
################################################################################
################################################################################
def count_tok_tag_L_R(train):

    c = 0
    POS = []
    l = 0
    r = 0
    for i in train:
        sep = i.split("\n")
        c += len(sep)
        for t in sep:
            f = t.split()
            if len(f) > 0:
                if int(f[0]) < int(f[3]):
                    l += 1
                else:
                    r += 1
                POS.append(f[2])

    POS = sorted(set(POS))
    return c-1, len(POS), l, r-len(train), POS

##############
y = count_tok_tag_L_R(list_train)
POS = y[4]
################################################################################
################################################################################
def switch_tree(train):
    keep = []
    ke = []
    for j in train:
        f = j .split()
        keep.append(f)

    for b in keep:
        u = []
        temp = []
        c = 0
        for x in range(len(b)):
            u.append(b[x])
            c += 1
            if c == 4:
                u[3], u[0] = int(u[0]), int(u[3])
                temp.append(u)
                u = []
                c = 0
        ke.append(sorted(temp))

    return ke
###############
f = switch_tree(list_train)

# print(f)
################################################################################
################################################################################
def only_tag (train):

    ke = []
    for g in train:
        t = defaultdict(list)
        for j in g:
            if j[2] in t:
                t[j[2]].extend([j[0],j[3]])
                ##j[0] = related_to_no, j[3] = serial_no
                # t[j[2]].extend(j[3])
            else:
                t[j[2]] = [j[0],j[3]]
                ##j[0] = related_to_no, j[3] = serial_no
        ke.append(dict(t))

    return ke
##############
tag = only_tag(f)
# print(tag)
################################################################################
################################################################################
def left_arc(all, un_tag):

    total_l = []
    for g in all:

        temp = defaultdict(list)
        for h in g:

            r = g[h][::2]
            s = g[h][1::2]
            ##collects only those which have relation index greater than there
            ##index number in the sentence
            ##appends them in a list
            for b in range(len(r)):

                if r[b] > s[b]:
                    temp[h].append(r[b])


        total_l.append(dict(temp)) # ITS A LIST

#-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    total_sr_l = {}

    for g in un_tag:

        tag_l = []
        for h in all:

            if g in h:
                tag_l.append(list(h[g][1::2]))
            else:
                tag_l.append(["null"])

        total_sr_l[g] = tag_l # ITS A DICTIONARY

#-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    left = {}
    for tup in un_tag:

        c = 0
        temp = {}
        for sentence in total_l:

            if tup in sentence:
                r = sentence[tup]
                for tags in total_sr_l:

                    h = total_sr_l[tags]
                    b = h[c]
                    for g in range(len(r)):

                        if r[g] in b or r[g] == b:
                            if tags in temp:
                                temp[tags] = temp[tags] + 1
                            else:
                                temp[tags] = 1
            c += 1

        left[tup] = temp

    return left

###############
arc_left = left_arc(tag, POS)
################################################################################
################################################################################
def right_arc(all, un_tag):

    total_r = []
    for g in all:

        temp = defaultdict(list)
        for h in g:

            r = g[h][::2]
            s = g[h][1::2]
            ##collects only those which have relation index greater than there
            ##index number in the sentence
            ##appends them in a list
            for b in range(len(r)):

                if r[b] < s[b] and r[b] != 0:
                    temp[h].append(r[b])

        total_r.append(dict(temp)) # ITS A LIST

    total_sr_r = {}

    for g in un_tag:

        tag_r = []
        for h in all:

            if g in h:
                tag_r.append(list(h[g][1::2]))
            else:
                tag_r.append(["null"])

        total_sr_r[g] = tag_r # ITS A DICTIONARY

    right = {}
    for tup in un_tag:

        c = 0
        temp = {}
        for sentence in total_r:

            if tup in sentence:
                r = sentence[tup]
                for tags in total_sr_r:

                    h = total_sr_r[tags]
                    b = h[c]
                    for g in range(len(r)):

                        if r[g] in b or r[g] == b:
                            if tags in temp:
                                temp[tags] = temp[tags] + 1
                            else:
                                temp[tags] = 1
            c += 1

        right[tup] = temp

    return right

    # print(right)
###############
arc_right = right_arc(tag,POS)
################################################################################
################################################################################
def confusion_arc(l,r):

    conf = {}
    for tag in l:
        lst = l[tag]
        emp = {}
        for tg in lst:
            h = r[tag]
            if tg in h:
                emp[tg] = [lst[tg],h[tg]]

        conf[tag] = emp

    c = 0
    for st in conf:
        kd = conf[st]
        ls = kd.keys()
        c = c + len(ls)

    return conf, c
###############
arc_confusion = confusion_arc(arc_left,arc_right) #[0] array itself, [1] number of confusing
################################################################################
################################################################################
def oracle_init(tst):

    dict_test = {}
    test = tst.split()
    for thing in test:
        g = thing.split("/")
        dict_test[g[0]] = g[1]
    strv = ""
    for t in test:
        strv = strv + t + " "

    print("\n\nInput Sentence:")
    print(strv)
    print("\n\nParsing Actions and Transitions:\n")

    global stack
    stack = []
    buffer = test
    print(stack,buffer,"SHIFT")
    stack.append(buffer[0])
    print(stack,buffer,"SHIFT")
    del buffer[0]
    stack.append(buffer[0])
    del buffer[0]
    dbv = 1

    return [buffer, stack, dbv]
###############
# c =  oracle_init(data_test)
################################################################################
################################################################################
def oracle(left,right,conf,b_v,s_v):

    buffer = b_v
    stack = s_v

    if len(stack) == 1 and len(buffer) != 0:
        print(stack,buffer,"SHIFT")
        stack.append(buffer[0])
        del buffer[0]

    if len(buffer) == 0 and len(stack) == 1:
        print(stack,buffer, "ROOT -->",stack[0])
        del stack[0]


    if len(stack) > 1:
        jth = stack[-1].split("/")[1]
        ith = stack[-2].split("/")[1]

        #Rule_1
        if ith[0] == 'V' and (jth[0] == '.' or jth[0] == 'R'):
            print(stack,buffer,"Right-Arc:",stack[-2],"-->",stack[-1])
            del stack[-1]

        #Rule_2
        elif ith[0] == 'I' and jth[0] == '.':
            print(stack,buffer,"SWAP")
            buffer.append(stack[-2])
            del stack[-2]

        # Rule_3
        elif (ith[0] == 'V' or ith[0] == 'I') and (jth[0] == 'D' or jth[0] == 'I' or jth[0] == 'J' or jth[0] == 'P' or jth[0] == 'R') and len(buffer) != 0:
            print(stack,buffer,"SHIFT")
            if len(buffer) > 0:
                stack.append(buffer[0])
                del buffer[0]

        #Confusion_Arc
        elif ith in conf and jth in conf[ith]:
            fg = conf[ith][jth]
            if fg.index(max(fg)) == 1:
                print(stack,buffer,"Right-Arc:",stack[-2],"-->",stack[-1])
                del stack[-1]
            elif fg.index(max(fg)) == 0:
                print(stack,buffer,"Left-Arc:",stack[-2],"<--",stack[-1])
                del stack[-2]

        # Left_Arc_Only
        elif ith in left and jth in left[ith]:
            print(stack,buffer,"Left-Arc:",stack[-2],"<--",stack[-1])
            del stack[-2]

        # Right_Arc_Only
        elif jth in right and ith in right[jth]:
            print(stack,buffer,"Right-Arc:",stack[-2],"-->",stack[-1])
            del stack[-1]

        else:
            print(stack,buffer,"SHIFT")
            if len(buffer) > 0:
                stack.append(buffer[0])
                del buffer[0]

    if len(stack) == 0:
        dbv = 0
    else:
        dbv = 1

    return [buffer, stack, dbv]

###############
# while c[2] == 1:
#     d = oracle(arc_left,arc_right,arc_confusion[0],c[0],c[1])
#     c[0] = d[0]
#     c[1] = d[1]
#     c[2] = d[2]
################################################################################
print("Corpus Statistics:\n")
n = 5 - len(str(len(list_train)))
print("\t# sentences  :", " "*n,len(list_train))
n = 5 - len(str(y[0]))
print("\t# tokens     :"," "*n,y[0])
n = 5 - len(str(y[1]))
print("\t# POS tags   :", " "*n,y[1])
n = 5 - len(str(y[2]))
print("\t# Left-Arcs  :"," "*n, y[2])
n = 5 - len(str(y[2]))
print("\t# Right-Arcs :"," "*n, y[3])
n = 5 - len(str(len(list_train)))
print("\t# Root-Arcs  :", " "*n,len(list_train))

##------------------------------------------
print("\n\nLeft Arc Array Nonzero Counts:\n")
for tag in POS:
    str_y = ""
    l_z = arc_left[tag]
    n = 4 - len(tag)
    for tag_2 in POS:
        if tag_2 in l_z:
            l_zz = l_z[tag_2]
            str_y = str_y + "[" + "  " + str(tag_2) + "," + " "*(4- len(str(l_zz)))+ str(l_zz) + "] "
    print(" "*n,tag,":",str_y)
##------------------------------------------
print("\n\nRight Arc Array Nonzero Counts:\n")
for tag in POS:
    str_y = ""
    l_z = arc_right[tag]
    n = 4 - len(tag)
    for tag_2 in POS:
        if tag_2 in l_z:
            l_zz = l_z[tag_2]
            str_y = str_y + "[" + "  " + str(tag_2) + "," + " "*(4- len(str(l_zz)))+ str(l_zz) + "] "
    print(" "*n,tag,":",str_y)
##------------------------------------------
print("\n\nArc Confusion Array:\n")
for tag in POS:
    str_y = ""
    l_z = arc_confusion[0][tag]
    n = 4 - len(tag)
    for tag_2 in POS:
        if tag_2 in l_z:
            l_zz = l_z[tag_2]
            str_y = str_y + "[" + "  " + str(tag_2) + ", " + str(l_zz[0]) + ","+ " "*(4- len(str(l_zz[1]))) + str(l_zz[1]) + "] "
    print(" "*n,tag,":",str_y)
##------------------------------------------
print("\n\tNumber of confusing arcs =", arc_confusion[1])
##------------------------------------------
c = oracle_init(data_test)
##------------------------------------------

while c[2] == 1:
    d = oracle(arc_left,arc_right,arc_confusion[0],c[0],c[1])
    c[0] = d[0]
    c[1] = d[1]
    c[2] = d[2]
