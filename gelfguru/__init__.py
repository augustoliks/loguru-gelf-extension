__version__ = '0.1.0'


from loguru import logger
import json
from functools import partialmethod
import os


class _FilterSyslogLevels:
    LEVELS = {
        'emergency': 0,
        'alert': 1,
        'critical': 2,
        'error': 3,
        'warning': 4,
        'notice': 5,
        'informational': 6,
        'info': 6,
        'debug': 7,
    }

    def __init__(self, level):
        self.level = 7

        try:
            if str(level).isdigit():
                for _, level_no in self.LEVELS.items():
                    if level_no == level:
                        self.level = level_no
            else:
                self.level = self.LEVELS.get(level.lower(), 7)
        except:
            print('Error log level configuration, will be set INFO level for default')

    def __call__(self, record):
        return record["level"].no <= self.level


def _gelf_sink(payload):
    event = json.loads(payload)
    record = event.get('record')
    text = event.get('text')

    _short = record.get("extra").get(
        "short_msg",
        " ".join(record.get("message").split()[:10])
    )

    gelf_payload = {
        'version': '1.1',
        "short_message": _short,
        "full_message": text,
        "timestamp": record.get("time").get('timestamp'),
        "level": record.get("level").get("no"),
        "line": record.get("line"),
        "_file": record.get("file").get("path"),
        "_context": {
            "module": "{}:{}:{}".format(record.get("name"), record.get("function"), record.get("line")),
            "process": record.get("process").get('name'),
            "thread": record.get("thread").get('name'),
        }
    }

    if record.get("extra").get("id"):
        gelf_payload.update({"_id_record": record.get("extra").get("id")})
        record["extra"].pop("id")

    if record.get("exception"):
        gelf_payload.update({"_exception": record.get("exception")})

    for extra_field, extra_value in record.get("extra").items():
        gelf_payload.update({'_{}'.format(extra_field): extra_value})        

    print(json.dumps(gelf_payload))


def configure_gelf_output():
    logger.__class__.emergency = partialmethod(logger.__class__.log, "emergency")
    logger.__class__.emerg = partialmethod(logger.__class__.log, "emerg")
    logger.__class__.alert = partialmethod(logger.__class__.log, "alert")
    logger.__class__.critical = partialmethod(logger.__class__.log, "critical")
    logger.__class__.crit = partialmethod(logger.__class__.log, "crit")
    logger.__class__.error = partialmethod(logger.__class__.log, "error")
    logger.__class__.err = partialmethod(logger.__class__.log, "err")
    logger.__class__.warning = partialmethod(logger.__class__.log, "warning")
    logger.__class__.notice = partialmethod(logger.__class__.log, "notice")
    logger.__class__.informational = partialmethod(logger.__class__.log, "informational")
    logger.__class__.info = partialmethod(logger.__class__.log, "info")
    logger.__class__.debug = partialmethod(logger.__class__.log, "debug")
    # logger.level("emergency", no=0)
    logger.level("emerg", no=0)
    logger.level("alert", no=1)
    logger.level("critical", no=2)
    logger.level("crit", no=2)
    logger.level("error", no=3)
    logger.level("err", no=3)
    logger.level("warning", no=4)
    logger.level("notice", no=5)
    logger.level("informational", no=6)
    logger.level("info", no=6)
    logger.level("debug", no=7)
    filter_syslog_levels = _FilterSyslogLevels(os.getenv('LOG_LEVEL', 'debug'))
    logger.configure(
        handlers=[
            dict(sink=_gelf_sink, filter=filter_syslog_levels, format='{level}', serialize=True, level=0)
        ]
    )
