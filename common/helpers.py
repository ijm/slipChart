##
# @file       helpers.py
# @brief      helper functions common to multiple scripts.
# @copyright  Copyright (C) Ian McEwan 2016. All rights reserved. This
#             file is distributed under the MPL license. See LICENSE file.


# Stuff for reading space separated, line oriented, profile dat files.

def floatOrString(s) :
    try:
        s = float(s)
    except:
        b = s.split(":") 
        if len(b) == 2 :
            s = float(b[0]) * 12.0 + (float(b[1]) -1 )

    return s

 
def readProfile(fname):
    f = open(fname, 'r')
    s = f.read()
    f.close()

    lines = ("".join(s.split("\\\n"))).split("\n")

    params = dict()
    rows = []
    for l in lines :
        if (l+" ")[0] == '#' or l.strip() == "" :
            continue
        bits = [ val for (i,s) in enumerate(l.strip().split('"') )
                 for val in ( s.split() if (i&1)==0 else [s]) ]
        if type(floatOrString(bits[0])) == float :
            rows.append( tuple( [ floatOrString(x) for x in bits] ))
        else:
            params[ bits[0] ] = None if len(bits)==1 else (
                floatOrString(bits[1]) if len(bits)==2 else (
                    tuple( [ floatOrString(x) for x in bits[1:] ] )
            ))

    return params, rows


def readRows( rs ) :
    threads = dict()
    
    for row in rs :
        now = row[0]
        name = row[1]
        cmd = row[2]
        val = row[3] if len(row)>3 else 0
        cmt = row[4] if len(row)>4 else ""
    
        if cmd != "Start" and name not in threads :
            print("Start of thread missing! ", row)
            raise NameError("missingThread")

        if cmd == "Start" and name in threads :
            print("Thread already exists! ", row)
            raise NameError("existingThread")
    
        if cmd == "Start":
            threads[ name ] = [ (now, val, cmt) ]
    
        elif cmd == "Delta" :
            (_, oend, _) = threads[name][-1]
            threads[ name ].append( (now, oend+val, cmt) )
    
        elif cmd == "End" :
            (_, oend, _) = threads[name][-1]
            if now != oend :
                print("Something went wrong at the end", row)
            threads[ name ].append( (now, oend, cmt) )

    return threads


def paramsToDict(p) : 
    d = dict()
    for k,v in p.items():
        (t,b) = k.split(".")
        if t not in d :
            d[t] = dict()
        d[t][b] = v

    return d


def sfmt(si, w, indent) :
    if w == 0 :
        return si

    so = ""
    sil = si.split()
    s = ""
    for sl in sil:
        if len(s)+len(sl) > w :
            so += s + "\n"
            s = indent + sl + " "
        else :
            s += sl + " "

    return (so+ ("" if s.strip() == indent.strip() else s)).strip()



