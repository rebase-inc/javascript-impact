import re
import curio_http
from json import loads
from logging import getLogger
from functools import lru_cache
from curio import run, tcp_server, subprocess, open_connection

from log import setup

setup()

LOGGER = getLogger(__name__)
LOGGER.debug('made the logger')
KNOWN_PACKAGES = {}

async def get_downloads(package_name):
  if package_name in KNOWN_PACKAGES:
    return KNOWN_PACKAGES[package_name]
  async with curio_http.ClientSession() as session:
    response = await session.get('https://api.npmjs.org/downloads/point/last-week/{}'.format(package_name))
    if response.status_code != 200:
      LOGGER.debug('Cant find package "{}"'.format(package_name))
      return 0
    content = await response.json()
  downloads = content['downloads']
  KNOWN_PACKAGES[package_name] = downloads
  return downloads

async def echo_client(client, addr):
  while True:
    data = await client.recv(100000)
    if not data:
      break
    LOGGER.debug('got the data')
    download_count = await get_downloads(loads(data.decode())[1].strip())
    LOGGER.debug('download count is {}'.format(download_count))
    await client.sendall(bytes(str(download_count), 'utf-8'))
  LOGGER.debug('Connection closed')

if __name__ == '__main__':
  LOGGER.debug('making the server')
  run(tcp_server('', 25000, echo_client))
