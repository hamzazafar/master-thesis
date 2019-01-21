# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from celery.utils.log import get_task_logger

from subprocess import Popen, PIPE

import random

logger = get_task_logger(__name__)

@shared_task(bind=True)
def scan(self, scan_name, address_range, target_port, version, request_hexdump,
         cron_str=''):
    logger.info('Request: {0!r}'.format(self.request))
    logger.info("""
                Scan Name: {0}
                Address Range: {1}
                UDP Port: {2}
                IP Version:{3}
                Hex Dump: {4}
                """.format(scan_name, address_range, target_port, version, request_hexdump))

    if version not in [4, 6]:
        raise ValueError("Invalid IP Address Version %s specified " % version)

    zmap_udp_probe = "udp" if version == "4" else "ipv6_udp"

    """
    # TODO: don't scan until you get Planet Lab IP Address
    process = Popen(['zmap',
                     '-M', zmap_udp_probe,
                     '-p', target_port,
                     '--probe-args=hex:%s' % request_hexdump,
                     '-f', 'saddr,udp_pkt_size',
                     '--output-filter="success = 1 && repeat = 0"',
                     address_range.join(' '), stdout=PIPE, stderr=PIPE])

    stdout, stderr = process.communicate()

    if "ERROR" in stderr:
        raise Exception(stderr)

    """

    stdout = "saddr,udp_pkt_size\n"
    num_amps = random.randint(1,10)
    request_size = random.randint(20,60)

    for i in range(num_amps):
        saddr = "%s.%s.%s.%s" % (random.randint(0,255),random.randint(0,255),
                                 random.randint(0,255),random.randint(0,255))
        response_size = random.randint(70,10000)
        stdout += "%s,%s\n" % (saddr, response_size)

    logger.info(stdout)
    amps = dict()
    data = stdout.split('\n')
    for row in data[1:]:
        if not row:
            continue
        amplifier, response_size = row.split(',')
        amps[amplifier] = dict()
        amps[amplifier]["response_size"] = response_size
        amps[amplifier]["amplification_factor"] = round(int(response_size)/request_size,2)

    result= dict()
    result["scan_name"] = scan_name
    result["request_size"] = request_size
    result["active_amplifiers_count"] = num_amps
    result["amplifiers"] = amps
    return result
