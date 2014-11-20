import subprocess
import datetime
import logging
import sys
from netaddr import IPNetwork
from time import sleep

netcount = 0
ipcount = 0
date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

if len(sys.argv) < 2:
        print 'Missing argument. Please provide a network list file, and optionally a port\n'
        print 'e.g. python portAuthority.py networks.txt 8088\n'
        print 'nohup python portAuthority.py networks.txt 8088 > foo.out 2> foo.err < /dev/null &'
        exit()

try:
        zmapBin = subprocess.check_output(['which', 'zmap']).strip()
        print 'zmap was found at:\n' + zmapBin
except:
        print 'zmap was not found in your PATH, quitting'
        exit()

if len(sys.argv) == 3:
        port = sys.argv[2]
else:
        port = raw_input('Enter port number to scan\ne.g. 8088\n:')

with open(sys.argv[1], 'r') as networksFile:
                for network in networksFile:
                        netcount = netcount +1
                        ip = IPNetwork(network)
                        ipcount = ipcount + ip.size 

print 'Total number of networks to be scanned: ' + str(netcount)
print 'Total number of IPs to be scanned: ' + ("{:,}".format(ipcount));

if len(sys.argv) < 3:
        choice = raw_input('Would you like to continue? Y/n ').lower()
        if 'n' in choice:
                exit()

with open(sys.argv[1], 'r') as networksFile:
        for network in networksFile:
                netname = network[0:8].strip('.')
                outFile = '{0}.{1}.{2}.zmap'.format(date, port, netname)
                zmapOptions = ' -p {0} -o {1} -B 1M -s 53 -v 2 '.format(port, outFile)
                fullCommand = 'nohup ' + zmapBin + zmapOptions + network.strip()
                print fullCommand + ' RUNNING \n'
                try:
                        subprocess.check_output(fullCommand, shell=True)
                        time.sleep(8)
                except subprocess.CalledProcessError as e:
                        logging.warning(e.output)
                        continue
                except Exception, e:
                        logging.warning(e.output)

networksFile.close()

print 'Scanning complete\n'
print 'find *.zmap | grep ' + port + ' | xargs cat | sort -t . -k 1,1n -k 2,2n -k 3,3n -k 4,4n | uniq'

exit()