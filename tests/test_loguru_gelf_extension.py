from loguru import logger
import unittest
import gelfguru


gelfguru.configure_gelf_output()
MESSAGE = 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit'


@logger.catch(level='emergency', reraise=False)
def test_capture_context_emergency(a, b):
    raise RuntimeError('any error')


@logger.catch(level='critical', reraise=False)
def test_capture_context_critical(a, b):
    raise RuntimeError('any critical')


@logger.catch(level='error', reraise=False)
def test_capture_context_error(a, b):
    raise RuntimeError('any error')


class TestCallMethods(unittest.TestCase):
    def test_loguru_default_calls(self):
        logger.critical('any critical - ' + MESSAGE)
        logger.error('any error - ' + MESSAGE)
        logger.success('any success - ' + MESSAGE)
        logger.warning('any warning - ' + MESSAGE)
        logger.debug('any debug - ' + MESSAGE)
        logger.trace('any trace - ' + MESSAGE)

    def test_loguru_new_calls(self):
        logger.emergency('any emergency - ' + MESSAGE)
        logger.informational('any informational - ' + MESSAGE)
        logger.notice('any notice - ' + MESSAGE)

    def test_add_new_fields(self):
        logger.bind(new_field="i am additional filed gelf").error('iste natus error sit')

    def test_capture_context_from_logger_catch_critical(self):
        test_capture_context_critical(5, 5)

    def test_capture_context_from_logger_catch_emergency(self):
        test_capture_context_emergency(5, 5)

    def test_capture_context_from_logger_catch_error(self):
        test_capture_context_error(5, 5)

    def test_capture_context_from_call_error(self):
        logger.error('any error - ' + MESSAGE)

    def test_capture_context_from_call_critical(self):
        logger.critical('any critical - ' + MESSAGE)

    def test_capture_context_from_call_alert(self):
        logger.alert('any alert - ' + MESSAGE)

    def test_capture_context_from_call_emergency(self):
        logger.emergency('any emergency - ' + MESSAGE)
