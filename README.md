NDIM2_asd
========

code for collecting behavioral data from ASD group (and controls on MTURK). very barebones app to host on mindhive.mit.edu. writes data to mysql db.

web app lives in /task. backend in python (cgi). ghetto frontend lives in in /html... html files loaded as strings with string replacement instead of templating :/
csvs to load into turk live in /turkcsvs
turkcsvs and relevant webtask data (slist.csv) are generated using prepNDIM24turk.py (lives in dropbox/antools/turk)
all changes can be made via config.py (set wage rate, databasename, etc.) and the data living in /appdata (NDE_stims = questions, appraisals= event dimensions, config_data= other relevant data)
collected data live in a mysql database on mindhive. this should be converted to CSV and stored in /data.
