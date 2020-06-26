import gelfguru
from loguru import logger
import unittest


class TestCallMethods(unittest.TestCase):
    def setUp(self) -> None:
        gelfguru.configure_gelf_output()

    def test_loguru_calls(self):
        logger.critical('test critical')
        logger.error('test error')
        logger.success('success == info')
        logger.warning('test warning Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit')
        logger.debug('test debug')
        logger.trace('test test tests')
        logger.emergency('emergency')
