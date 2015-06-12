#!/usr/bin/python

import os.path
import plistlib
import sys

import reports

# Print the usage text if needed
if len(sys.argv) != 2:
	print "Usage: python wikifiy-summary.py Summary.plist"
	sys.exit()

# Read in the file they named
infile = open(sys.argv[1], "r")
data = infile.read()
infile.close()

# We want an array of reports, but we also want direct access to the plist
plist = plistlib.readPlistFromString(data)
reportlist = reports.summaryPlistToReports(data)

# Print out the header
print """== Static Analysis of Adium ==

This page lists the reports generated by [http://clang.llvm.org/StaticAnalysis.html Clang Static Analyzer] as run on r%(revision)s. This page can be used by developers to investigate each report and make a ruling on its validity.

=== Key ===

|| ||No ruling||
||[ticket:6 Y]||Confirmed report, ticket open||
||[ticket:1337 Y]||Confirmed report, ticket closed||
||~~[changeset:4 F]~~||Confirmed report, fixed without a ticket||
||N||False positive||

=== Reports ===

|| ||Data||Comment||""" % { "revision" : plist["Revision"] }

# Now print out each report
for r in reportlist:
	print "|| ||%(bugtype)s in [http://rgov.org/adium/r%(revision)s/%(reportfile)s %(sourcefile)s:%(linenum)i]|| ||" % {
		"bugtype" : r.type,
		"revision" : plist["Revision"],
		"reportfile" : r.reportfile,
		"sourcefile" : os.path.basename(r.sourcefile),
		"linenum" : r.endpathline,
	}