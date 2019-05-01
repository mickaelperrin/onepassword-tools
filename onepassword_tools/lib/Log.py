import json
import logging
logger = logging.getLogger("app")


class Log:

    @staticmethod
    def _pretty_print(msg):
        if type(msg).__name__ == 'dict':
            msg = json.dumps(msg, indent=4)
        return msg

    @staticmethod
    def debug(msg, name='', pretty_print=True):
        if pretty_print:
            msg = Log._pretty_print(msg)
        if name:
            logger.debug('** %s **' % name)
        logger.debug(msg)
        logger.debug('')

    @staticmethod
    def debug2(msg, name='', pretty_print=True):
        if pretty_print:
            msg = Log._pretty_print(msg)
        if name:
            logger.log(5, '>> %s' % name)
        logger.log(5, msg)
        logger.log(5, '')

    @staticmethod
    def error(msg):
        logger.error(msg)

    @staticmethod
    def info(msg, name='', pretty_print=False):
        if pretty_print:
            msg = Log._pretty_print(msg)
        if name:
            logger.info('** %s **' % name)
        logger.info(msg)

