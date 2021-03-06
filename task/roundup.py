#!/usr/bin/python

import cgitb, cgi, MySQLdb
from qs import questions
import ndim_funcs as ndf
import config as cf
from config import emolist
#
printpage=cf.htmldict['roundup']
tablename=cf.table
subjtablename=cf.subjtable
##
myform=cgi.FieldStorage()
cgitb.enable()
print 'Content-type:text/html\n\n'
cursor = MySQLdb.connect(host=cf.host,user=cf.user,passwd=cf.passwd,db=cf.db).cursor()


theids=myform.keys() 
subjid = myform['subjid'].value
#questionID=ndf.defineQ(subjid)
#qnum=int(questionID)
qnum=int(myform['qnum'].value)
qindex=myform['qindex'].value
possqs = myform['possqs'].value

try:
    possqs = ndf.string2intlist(possqs)
except:
    pass #will fail when number of rounds is max
dnums=list(eval(myform['dnums'].value))
thisround=int(myform['thisround'].value) 
formindex=ndf.savelastentry(cursor, tablename, myform, emolist)
ndf.updatelog(cursor, subjtablename, subjid, qnum)
possrounds=len(questions)
if thisround==1:
    thisroundunit='round'
else:
    thisroundunit='rounds'
if thisround==possrounds:
    printpage=cf.htmldict['summary']
totalpayment=cf.baserate+cf.rate*(int(thisround)-1)

#print the page
newhtml=ndf.gethtml(printpage)
newhtml=newhtml.replace('qindex_var',str(qindex)).replace('qnum_var',str(qnum)).replace('nextthing_var','demographics.py').replace('subjid_var',subjid).replace('dnumlist_var',str(dnums)).replace('formindex_var',str(formindex)).replace('possqs_var',str(possqs)).replace('thisround_var',str(thisround)).replace('thisroundunit_var',thisroundunit).replace('possrounds_var',str(possrounds)).replace('rate_var', str(cf.rate)).replace('totalpayment_var', str(totalpayment))
head=ndf.gethtml(cf.htmldict['head'])
newhtml=newhtml.replace('head_var', head)

print newhtml
