portAuthority
=============
Simple zmap automation in python.
Call the python module and pass in a single argument containing a newline delimited set of networks in CIDR format.
e.g. python portAuthority.py networks.txt
where networks.txt looks like:
192.168.0.1/24
172.16.0.0/16
10.10.10.10/30

Whilst running the program, interactive input is taken from the user to collect the requisite port or port range. Each network in the list gets it's own output file and when the program completes a Bash one-liner is generated for neatly displaying the positive results of your scan.
