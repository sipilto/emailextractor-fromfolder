#!/usr/bin/env python


from optparse import OptionParser
import os.path
import time
import re
from os import listdir
from os.path import isfile, join



regex = re.compile(("([a-z0-9!#$%&*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

# create file to export emails
extensionTime = time.strftime("%H%M%S")
myFile = "emailList_"+extensionTime+".txt"

def file_to_str(filename):
    """Returns the contents of filename as a string."""
    with open(filename) as f:
        return f.read().lower() # Case is lowered to prevent regex mismatches.

def get_emails(s):
    """Returns an iterator of matched emails found in string s."""
    # Removing lines that start with '//' because the regular expression
    # mistakenly matches patternslike 'http://foo@bar.com' as '//foo@bar.com'.
    return (email[0] for email in  re.findall(regex, s) if not email[0].startswith('//'))

def add_to_file(myFile, email):
    """Save in a text file the emails extracted """
    with open(myFile,"a") as emailsfile:
        emailsfile.write(email+"\n")

def process(file):
    if isfile(file):
        # regex emails
        for email in get_emails(file_to_str(file)):
            if "@gmail.com" in email:
                #print (email)
                add_to_file(myFile, email)
    else:
        for f in listdir(file):
            p = join(file, f)
            process(p)
        
if __name__ == '__main__':
    parser = OptionParser(usage="Usage: python %prog [FILE]...")
    # No options added yet. Add them here if you ever need them.
    options, args = parser.parse_args()

    if not args:
        parser.print_usage()
        exit(1)

    for arg in args:
        process(arg)
