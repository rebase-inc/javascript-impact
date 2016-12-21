import os
import base64
import logging

import rsyslog

from curio_http import ClientSession
from asynctcp import AsyncTCPCallbackServer
    
rsyslog.setup(log_level = os.environ['LOG_LEVEL'])
LOGGER = logging.getLogger(__name__)

async def get_downloads(package_name):
    async with ClientSession() as session:
        url = 'https://api.npmjs.org/downloads/point/last-week/{}'.format(package_name)
        response = await session.get(url)
        if response.status_code == 404:
            LOGGER.debug('No such package {}'.format(package_name))
            return 0
        elif (response.status_code < 200) or (response.status_code >= 300):
            LOGGER.error('GET of {} returned {}'.format(url, response.status_code))
            return 0
        content = await response.json()
        downloads = content['downloads'] if 'downloads' in content else 0
        LOGGER.debug('number of downloads for package {} is {}'.format(package_name, downloads))
        return downloads

if __name__ == '__main__':
    AsyncTCPCallbackServer(
            callback = get_downloads, 
            host = '0.0.0.0',
            port = 9999,
            encode = lambda d: bytes(str(d) + '\n', 'utf-8'),
            decode = lambda d: base64.b64decode(d).decode().strip()
            ).run()
