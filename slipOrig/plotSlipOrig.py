##
# @file       plotSlipOrig.py
# @brief      Plot 45 degree Timeline Slip chart
# @copyright  Copyright (C) Ian McEwan 2016. All rights reserved. This
#             file is distributed under the MPL license. See LICENSE file.

import numpy as np
import argparse
import matplotlib as mpl

mpl.use('pgf')
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": "\n".join([
         r"\usepackage[utf8x]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         ] )
}
mpl.rcParams.update({
    'font.size': 9,
    "font.family": "serif",
    'text.usetex':True,
    })
mpl.rcParams.update(pgf_with_pdflatex)

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, StrMethodFormatter,FuncFormatter 
from helpers import *

def doArgs() :
    parser = argparse.ArgumentParser(description= "Plot Schedule Slip Chart")
    parser.add_argument('-i', '--infile', dest='iname',required=True,
                        help='input file')
    parser.add_argument('-o', '--outfile', dest='oname',required=True,
                        help='output file basename')
    return parser.parse_args()


def plotSlip(ax,threads,params) :
    xmarks =[]
    ymarks =[]
    divs = 12

    font = params["font"]

    (xminY,xmaxY,xlabel) = params['axis']['x']
    (yminY,ymaxY,ylabel) = params['axis']['y']

    xmin = xminY * divs 
    xmax = xmaxY * divs 
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
                     ax.text(x+offset, y+0.33, cmt+" ",
                         ha=ha, va='top', fontsize=font["small"], zorder=4)
                     break
 
        xys = np.array(xys)

        ax.plot( xys[:,0], xys[:,1], alpha = 0.66, lw = 2, zorder=2)
        ax.plot( [ox], [oy], '^', ms=4, c='black', zorder=3) 

    xmarks = np.array(xmarks)
    ymarks = np.array(ymarks)

    ax.plot(xmarks[:,0] , xmarks[:,1], '|', c='grey', alpha = 0.33, zorder=1) 
    ax.plot(ymarks[:,0] , ymarks[:,1], '_', c='grey', alpha = 0.33, zorder=1) 

    s = ""
    fnts = params["footnote"]
    indent = fnts["indent"] if "indent" in fnts else ""
    (fx, fy) = fnts["location"] 

    for i in sorted( fnts.keys() ) :
        if type( floatOrString(i)) == float :
            s += sfmt(fnts[i],fnts["width"],indent)+"\n\n"
    
    ax.text(fx, fy, s,
            verticalalignment='top', horizontalalignment='left',
            transform=ax.transAxes, fontsize = font["small"], zorder=4)

    tmin = min( [xmin,ymin] )
    tmax = max( [xmax,ymax] )

    ax.plot( [tmin,tmax],[tmin,tmax], c='black', zorder=3 )
    ax.fill_between( [tmin,tmax], [tmin,tmax], [tmin,tmin], 
                                     facecolor='white',zorder=2)

    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin-1,ymax])
    ax.set_aspect('equal')
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    months = ['J','F','M','A','M','J','J','A','S','O','N','D']
    def fmt_mon(x, pos):
        return f'{months[int(x%12)]}'

    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks_position('top')

    ax.tick_params(which='major', width=0.8, length=8)
    ax.tick_params(which='minor', width=0.75, length=2.5, labelsize=10)

    ax.xaxis.set_ticks( np.arange(xmin,xmax,divs)-0.5 )
    ax.xaxis.set_ticklabels(["$~~~~~~%d$" % y for y in np.arange(xminY,xmaxY)],
                            ha='left')

    ax.xaxis.set_minor_locator(FixedLocator(np.arange(xmin, xmax)))
    ax.xaxis.set_minor_formatter(FuncFormatter(fmt_mon))
    ax.xaxis.set_ticks(np.arange(xmin,xmax), minor=True)

    ax.yaxis.set_ticks( np.arange(ymin,ymax,divs)-0.5 )
    ax.yaxis.set_ticklabels(["$~~~~~~%d$" % y for y in np.arange(yminY,ymaxY)],
                            va='bottom')

    ax.yaxis.set_minor_locator(FixedLocator(np.arange(ymin, ymax)))
    ax.yaxis.set_minor_formatter(FuncFormatter(fmt_mon))
    ax.yaxis.set_ticks(np.arange(ymin,ymax), minor=True)

    ax.grid(True, linestyle=':')

    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_rotation('vertical')

    ax.tick_params(axis='both', which='minor', labelsize=font["small"], pad=2)
    ax.tick_params(axis='both', which='major', labelsize=font["large"], pad=8 )

def main():
    args = doArgs()

    (ps, rs) = readProfile(args.iname)
    threads = readRows( rs ) 
    params = paramsToDict( ps )
 
    f,ax = plt.subplots(1,1)

    plotSlip(ax, threads, params)

    f.set_size_inches(params["axis"]["pagewidth"],
                      params["axis"]["pageheight"])

    f.savefig(args.oname+".pgf", bbox_inches = 'tight')
    f.savefig(args.oname+".pdf", bbox_inches = 'tight')
    f.savefig(args.oname+".svg", bbox_inches = 'tight')

main() 

