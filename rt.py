#!/bin/env python
from rtkit.resource import RTResource
from rtkit.authenticators import KerberosAuthenticator
from rtkit.errors import RTResourceError

from rtkit import set_logging
import logging
#set_logging('debug')
logger = logging.getLogger('rtkit')
produrl = 'https://engineering.redhat.com/rt/REST/1.0/'
testurl = 'https://rt-stage.englab.bne.redhat.com/rt/REST/1.0/'
url=testurl

resource = RTResource(url, None, None, KerberosAuthenticator)


SUBJ='test ticket'
TEXT='this is  my test'

content = {
    'content': {
	'id': 'ticket/new',
        'Subject' : 'Slava-testing New Ticket',
	'Text' : 'Body: Slava testing',
        'Queue': 'eng-ops-prod',
	'Status': 'Resolved',
	'Requestor': 'vmindru@redhat.com',
	'Owner': 'vmindur@redhat.com',
	
    }
}
try:
    response = resource.post(path='ticket/new', payload=content,)
    logger.info(response.parsed)
    print response.status
    print response.body
except RTResourceError as e:
    logger.error(e.response.status_int)
    logger.error(e.response.status)
    logger.error(e.response.parsed)


