from logging import (
    getLogger,
    Formatter,
    LogRecord,
    StreamHandler,
)
from logging.handlers import SysLogHandler
from os import environ as env
from sys import stdout


RFC_SYSLOG_MAX_MSG_LENGTH = 1024


class TruncatingLogRecord(LogRecord):

    def getMessage(self):
        return super(TruncatingLogRecord, self).getMessage()[:RFC_SYSLOG_MAX_MSG_LENGTH]


def setup():
    root_logger = getLogger()
    level = env['LOG_LEVEL'] if 'LOG_LEVEL' in env else 'DEBUG'
    root_logger.setLevel(level)
    rsyslog = SysLogHandler(address=('rsyslog', 514))
    rsyslog.setFormatter(Formatter(fmt='%(levelname)s {%(processName)s[%(process)d]} %(message).900s'))
    root_logger.addHandler(rsyslog)
    from platform import python_version_tuple
    major, minor, _ = python_version_tuple()
    if int(major) > 2 and int(minor) > 1:
        # we need to make sure messages to rsyslog are kept under 1024 bytes
        # per RFC-3164 ('4.1 syslog Message Parts')
        # Not sure why this is not enforced by SysLogHandler
        # In python 3 we can change the logRecord factory.
        # In Python 2 we can only hope the Formatter format string is truncating the 'message' attribute
        # as in this example: "%(message).100s"  => limit is 100 chars
        from logging import setLogRecordFactory
        setLogRecordFactory(TruncatingLogRecord)
    root_logger.debug('Root logger is setup')


def log_to_stdout():
    root_logger = getLogger()
    root_logger.setLevel('DEBUG')
    streamingHandler = StreamHandler(stdout)
    streamingHandler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    root_logger.addHandler(streamingHandler)

