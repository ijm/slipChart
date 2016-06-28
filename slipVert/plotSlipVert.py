##
# @file       plotSlipVert.py
# @brief      Plot Vertical Timeline Slip chart
# @copyright  Copyright (C) Ian McEwan 2016. All rights reserved. This
#             file is distributed under the MPL license. See LICENSE file.

import numpy as np
import argparse
import matplotlib as mpl

mpl.use('pgf')
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        ]
    }
mpl.rcParams.update({'font.size': 9, "font.family": "serif",})
mpl.rcParams.update(pgf_with_pdflatex)

import matplotlib.pyplot as plt
from helpers import *

def doArgs() :
    parser = argparse.ArgumentParser(description= "Plot Schedule Slip Chart")
    parser.add_argument('-i', '--infile', dest='iname',required=True,
                        help='input file')
    parser.add_argument('-o', '--outfile', dest='oname',required=True,
                        help='output file basename')
    return parser.parse_args()


def plotSlip(ax,threads,params) :
    xmarks = []
    ymarks = []
    divs = 12

    font = params["font"]

    (yminY,ymaxY,ylabel) = params['axis']['y']

    xmin = -24
    xmax = 24
    ymin = yminY * divs 
    ymax = ymaxY * divs 

    ans = params["annotate"] if "annotate" in params else dict()

    aindent = ans["indent"] if "indent" in ans else ""
    awidth  = ans["width"]  if "width"  in ans else 0

    for k,v in threads.items() :
        (ox,oy,_) = (sx,sy,_) = v[0]
        xys = []
        for (x,y,cmt) in v :
             xys.append( (x, oy) )
             xys.append( (x, y)    )
             for tx in np.arange( ox, x+1) :
                 xmarks.append( (tx, oy) )
             
             for ty in np.arange(oy, y+1) if y>oy else np.arange(y,oy+1) :
                 ymarks.append( (x, ty) )
             ox = x
             oy = y
             ha = 'left'
             offset = 0.5
             while len(cmt) > 0 :
                 if cmt[0] == '-' :
                     ha = 'right'
                     offset -= 1
                     cmt = cmt[1:]
                 elif cmt[0] == '+' :
                     ha = 'left'
                     offset += 1
                     cmt = cmt[1:]
                 else:
                     aax = (x-y)*0.5
                     aay = (x+y)*0.5 
                     ax.annotate( sfmt(cmt,awidth,aindent),
                                  xy = (aax,aay), xytext=(aax+offset,aay), 
                                  arrowprops=(dict() if abs(offset) < 1.0 else 
                                              dict(facecolor='grey',
                                                   alpha=0.2,
                                                   arrowstyle='-')),
                                  ha=ha, va='center', fontsize=font["small"] )
                     break

        # This is the scaled 45 degree rotation for each line, and it is
        # kludgy. It would be better if I set up a custom projection
        # type - but that's a real pain, so  this is it for now.
 
        xys0 = np.array(xys)
        xys = np.copy(xys0)

        xys[:,0] -= xys[:,1]
        xys[:,1] += xys0[:,0]
        xys[:,0] *= 0.5
        xys[:,1] *= 0.5

        xys[:,0] = (xys0[:,0] - xys0[:,1] ) *0.5
        xys[:,1] = (xys0[:,0] + xys0[:,1] ) *0.5

        oxt = ox
        ox -= oy
        oy += oxt
        ox *= 0.5
        oy *= 0.5

        sxt = sx
        sx -= sy
        sy += sxt
        sx *= 0.5
        sy *= 0.5

        ax.plot( xys[:,0], xys[:,1], alpha = 0.66, lw = 2, zorder=2)
        ax.plot( [ox], [oy], '^', ms=4, c='black', zorder=3) 

    # This is the scaled 45 degree rotation for ticks along lines see
    # comment above about kludgyness.
    xmarks = np.array(xmarks)
    tmp = np.copy(xmarks)
    xmarks[:,0] -= xmarks[:,1]
    xmarks[:,1] += tmp[:,0]
    xmarks *= 0.5

    ymarks = np.array(ymarks)
    tmp = np.copy(ymarks)
    ymarks[:,0] -= ymarks[:,1]
    ymarks[:,1] += tmp[:,0]
    ymarks *= 0.5

    ax.plot( xmarks[:,0], xmarks[:,1], 'x', c='grey', alpha = 0.33,zorder =1) 
    ax.plot( ymarks[:,0], ymarks[:,1], 'x', c='grey', alpha = 0.33,zorder =1) 

    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin-1,ymax])
    ax.set_aspect('equal')
    #ax.set_ylabel(ylabel)
    #ax.set_xlabel(xlabel)

    months = ['J','F','M','A','M','J','J','A','S','O','N','D']*int(ymax-ymin)
    
    ax.xaxis.set_label_position('top')
    ax.yaxis.set_label_position('right')

    ax.yaxis.set_ticks( np.arange(ymin,ymax,divs)-0.5+6 )
    ax.yaxis.set_ticklabels(["$%d$" % y for y in np.arange(yminY,ymaxY)],
                            va='center')

    ax.yaxis.set_ticks(np.arange(ymin,ymax) , minor=True)
    ax.yaxis.set_ticklabels(months, minor=True )

    ys = range( int(ymin)-divs, int(ymax)+divs+1, divs )
    for y in ys :
        ax.plot( [xmin, 0, xmin], [y+xmin-0.5, y-0.5, y-xmin-0.5], ':',
                 c='black', alpha=0.33)
        ax.plot( [0, xmax] , [y-0.5,y-0.5] , ':', c='black', alpha=0.33)

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_position(('data',0))
    ax.spines['left'].set_position(('data',xmax))

    # This needs cleanup.
    ax.tick_params(axis='both', which='both',
          labeltop='off', labelbottom='off', labelright='on', labelleft='on',
          top     ='off', bottom     ='off', right='on',      left='on'
          )
    ax.tick_params(axis='y', which='both', direction='out')
    ax.tick_params(axis='both', which='minor', labelsize=font["small"], pad=1, 
                   labelleft='off', left='off' )
    ax.tick_params(axis='both', which='major', labelsize=font["large"], pad=7,
                   labelright='off', left='off', right='off' )

    plt.setp(ax.get_yticklabels() , rotation=90)

    
def main():
    args = doArgs()

    (ps, rs) = readProfile(args.iname)
    threads = readRows( rs ) 
    params = paramsToDict( ps )

    f,ax = plt.subplots(1,1)
    
    plotSlip(ax, threads, params)

    f.set_size_inches( params["axis"]["pagewidth"],
                       params["axis"]["pageheight"] )

    f.savefig(args.oname+".pgf", bbox_inches = 'tight')
    f.savefig(args.oname+".pdf", bbox_inches = 'tight')

main() 

