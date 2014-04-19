# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 09:42:34 2014

@author: amyskerry
"""
import sys
sys.path.append('/Users/amyskerry/Dropbox/antools/utilities/')
import os
import aesbasicfunctions as abf
import matplotlib.pyplot as plt
import numpy as np

##hard coding
version='ver2asd'
remotedir='/home/askerry/'
if version=='ver2_control':
    remoteshscript='dlNDE_dim2_control.sh'
    remotefiles=[remotedir+'NDE_dimdl2_control.csv']
    localfiles=['NDE_dimdl2_control.csv']
    localdestination='/Users/amyskerry/documents/projects/turk/NDE_dim2/data/DIM_data/sqldata/'
elif version =='ver2':    
    remoteshscript='dlNDE_dim2.sh'
    remotefiles=[remotedir+'NDE_dimdl2.csv']
    localfiles=['NDE_dimdl2.csv']
    localdestination='/Users/amyskerry/documents/projects/turk/NDE_dim2/data/DIM_data/sqldata/'
elif version =='ver2asd':    
    remoteshscript='dlNDE_dim2asd.sh'
    remotefiles=[remotedir+'NDE_dimdl2_asdresponses.csv', remotedir + 'NDE_dimdl2_asdsubjlog.csv']
    localfiles=['NDE_dimdl2_asdresponses.csv', 'NDE_dimdl2_asdsubjlog.csv']
    localdestination='/Users/amyskerry/documents/projects/turk/NDE_dim2asd/data/DIM_data/sqldata/'
hostname='mindhive.mit.edu'
username='askerry'
password='password'
##

def main(hostname,username,password, remoteshscript,remotedir,remotefile,localdestination):
    homedir=os.getcwd()
    os.chdir(localdestination)
    ## first ssh in
    abf.runsshremotescript(hostname, username, password, remoteshscript)
    ##now sftp in
    for remotefile in remotefiles:
        abf.fetchviasftp(hostname,username,remotedir,remotefile,localdestination)
    os.chdir(homedir)
    
def checkdata(names, data, version):
    checkthresh=6
    hitthresh=7
    if version=='ver2':
        qindex=names.index('expectedness_qlabel')
        numitems=200
    elif version=='ver2asd':
        qindex=names.index('expectedness_qlabel')
        numitems=20
    elif version=='ver2_control':
        qindex=names.index('valence_qlabel')
        numitems=200
    checkindex=names.index('main_character')
    nameindex=names.index('subjid')
    hist_all=[[] for a in range(0,numitems)]
    hist_keep=[[] for a in range(0,numitems)]
    hist_keep_names=[[] for a in range(0,numitems)]
    hist_all_names=[[] for a in range(0,numitems)]
    for a in range(0,numitems):
        hist_all[a]=[d[qindex][1:] for d in data if abf.floatiffloattable(d[qindex][1:])==a+1]
        hist_keep[a]=[d[qindex][1:] for d in data if abf.floatiffloattable(d[qindex][1:])==a+1 and abf.float_or_zero(d[checkindex])>checkthresh]
        hist_all_names[a]=[d[nameindex] for d in data if abf.floatiffloattable(d[qindex][1:])==a+1]
        hist_keep_names[a]=[d[nameindex] for d in data if abf.floatiffloattable(d[qindex][1:])==a+1 and abf.float_or_zero(d[checkindex])>checkthresh]
    #labels=[h[0] for h in hist_all]
    labels=[str(hn+1) for hn,h in enumerate(hist_all)]
    histocounts_all=[len(h) for h in hist_all]
    histocounts_keep=[len(h) for h in hist_keep]
    f,axes=plt.subplots(2, figsize=[26,5])
    axes[0].bar(range(0,numitems), histocounts_all)
    axes[0].set_xticks(np.arange(0.6,numitems+.6,2))
    axes[0].set_xticklabels(labels[0:numitems:2], rotation=90, fontsize=10)
    axes[0].set_xlabel('all completes')
    axes[1].bar(range(0,numitems), histocounts_keep)
    axes[1].set_xticks(np.arange(0.6,numitems+.6,2))
    axes[1].set_xticklabels(labels[0:numitems:2], rotation=90, fontsize=10)
    axes[1].set_xlabel('keepers only (check>8)')
    plt.tight_layout()
    blacklist=[(el,histocounts_keep[eln]) for eln,el in enumerate(labels) if histocounts_keep[eln]>hitthresh]
    listdict=dict(blacklist)  
    if len(blacklist)>0:
        blacklist,counts=zip(*blacklist)   
        blacklist=[int(b)-1 for b in blacklist]
        print 'blacklist=' 
        print blacklist
    print listdict
    hist_all_names=[name for sublist in hist_all_names for name in sublist]
    hist_keep_names=[name for sublist in hist_keep_names for name in sublist]
    return hist_all, hist_keep, hist_all_names, hist_keep_names
    
    
if __name__=='__main__':
    main(hostname,username,password, remoteshscript,remotedir,remotefiles,localdestination)
    names,data=abf.extractdata(localdestination+localfiles[0])
    hist_all, hist_keep, hist_all_names, hist_keep_names=checkdata(names,data,version)
        