from json import loads
from logging import getLogger
from multiprocessing import current_process
from signal import signal, SIGTERM, SIGINT
from sys import exit

from curio import run, tcp_server
from curio_http import ClientSession

from .log import setup


current_process().name = 'impact-javascript'


setup()


LOG = getLogger(__name__)


KNOWN_PACKAGES = {}


def quit(signal_number, stack_frame):
    exit(0)


async def get_downloads(package_name):
    if package_name in KNOWN_PACKAGES:
        return KNOWN_PACKAGES[package_name]
    async with ClientSession() as session:
        response = await session.get('https://api.npmjs.org/downloads/point/last-week/{}'.format(package_name))
        if response.status_code != 200:
            LOG.debug('Cant find package "{}"'.format(package_name))
            return 0
        content = await response.json()
        downloads = content['downloads']
        KNOWN_PACKAGES[package_name] = downloads
    return downloads


async def connection_handler(client, addr):
    LOG.debug('New connection with client at {}'.format(addr))
    stream = client.as_stream()
    while True:
        args_as_JSON = await stream.readline()
        if not args_as_JSON:
            break
        download_count = await get_downloads(loads(args_as_JSON.decode())[1].strip())
        LOG.debug('download count is {}'.format(download_count))
        await stream.write(bytes(str(download_count)+'\n', 'utf-8'))
    LOG.debug('Connection closed')


if __name__ == '__main__':
    signal(SIGTERM, quit)
    signal(SIGINT, quit)
    run(tcp_server('', 25000, connection_handler))


