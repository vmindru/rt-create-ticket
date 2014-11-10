#!/bin/env python
from rtkit.resource import RTResource
from rtkit.authenticators import KerberosAuthenticator
from rtkit.errors import RTResourceError
from optparse import OptionParser
from rtkit import set_logging
import sys,logging,os,fileinput

logger = logging.getLogger('rtkit')
produrl = 'https://engineering.redhat.com/rt/REST/1.0/'
testurl = 'https://rt-stage.englab.bne.redhat.com/rt/REST/1.0/'
url=testurl
resource = RTResource(url, None, None, KerberosAuthenticator)


RT_Queue="eng-ops-prod"
RT_Status="new"
RT_Requestor="vmindru@redhat.com"
RT_Owner=RT_Requestor



def submit_ticket_static(content):
	try:
	    response = resource.post(path='ticket/new', payload=content,)
	    logger.info(response.parsed)
	    print response.status
	    print response.body
	except RTResourceError as e:
	    logger.error(e.response.status_int)
	    logger.error(e.response.status)
	    logger.error(e.response.parsed)

def main():
        parser = OptionParser()
        parser.add_option("-q", "--queue", dest = "queue" , default= "eng-ops-prod" , help="specify queue")
        parser.add_option("-S", "--status", dest = "status" , default= "new" , help="specify status new,resolved,open")
        parser.add_option("-r", "--requestor", dest = "requestor" , default= "none" , help="specify status new,resolved,open")
        parser.add_option("-o", "--owner", dest = "owner" , default= "none" , help="specify status new,resolved,open")
        parser.add_option("-s", "--subject", dest = "subject" , default= "Ticket created other API", help="specify status new,resolved,open")
	parser.add_option("-i", "--input", dest = "input" ,default = "none", help="specify input of message body. stdin,file")
	parser.add_option("-f", "--file", dest = "file" , help="path to file for message body")
	(options, args) = parser.parse_args()
	my_options = {
			"options": {
					"Queue": options.queue,
					"Status": options.status,	
					"Requestor": options.requestor,
					"Owner": options.owner,
					"Subject": options.subject,
					"Input": options.input,
					"File": options.file,
				}	
		}
	return my_options


def define_content():
	content = {
	    'content': {
		'id': 'ticket/new',
	        'Subject' : RT_Subject,
		'Text' : RT_Text,
	        'Queue': RT_Queue,
		'Status': RT_Status,
		'Requestor': RT_Requestor,
		'Owner': RT_Owner,
	    }
	}
	return content

# build_request_options - checks for invoked options. 
def build_request_options(opts):
	# Make sure we have a proper Subject.
	if len(opts["options"]["Subject"]) > 20:	
		True	
	else:	
		print "to short Subject"
		sys.exit(22)
	# Make sure the status is new,resolved or open
	if opts["options"]["Status"] in ["new","resolved","open"]:
		True
	else:
		print "Status can be [new,resolved,open] only"
		sys.exit(22)
	# Make sure we have a Requestor 
	if opts["options"]["Requestor"] == "none":
		print "Define requestor email address"
		sys.exit(22)
	else:
		True
	# Make sure we have a Owner
	if opts["options"]["Owner"] == "none":
		print "Define owner email address"
		sys.exit(22)
	else:
		True
	
	# check if -i has been invoked, if no read from stdin if yes check if file exists and store it in 'text'
	if opts["options"]["Input"] == "none":
		print "Grabing data from STDIN"
		text=''
		for line in sys.stdin:
   			text=text+line


	else:
		if os.path.isfile(opts["options"]["Input"]): 
			text=''
			for line in fileinput.input(files = opts["options"]["Input"]):
				    text=text+line
		else:
			print "we doubt {} is a file".format(opts["options"]["Input"])
	return opts,text

if __name__ == "__main__":
	opts = main()
	data = 	build_request_options(opts)

options = data[0]
print options["options"]["Queue"]






