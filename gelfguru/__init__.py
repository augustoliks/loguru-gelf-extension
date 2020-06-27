"""
A Loguru extension for handling log messages and adapt to GELF
payload pattern, without modifying  built-in Loguru methods call.
This library was created especially for applications running in
Docker environment with GELF Logging Driver.
"""
__version__ = '0.1.3'


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
        'success': 5,
        'informational': 6,
        'info': 6,
        'debug': 7,
        'trace': 7,
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
        except Exception as e:
            print('Error log level configuration, will be set INFO level for default | {}'.format(e))

    def __call__(self, record):
        return record["level"].no <= self.level


def _gelf_sink(payload):
    event = json.loads(payload)
    record = event.get('record')
    text = event.get('text')

    if record.get('level').get('no') <= 3 and record.get('exception'):
        msg_short = " ".join(text.split(' ')[:10])
        msg_full = text
    else:
        msg_short = " ".join(record.get('message').split(' ')[:10])
        msg_full = record.get('message')

    gelf_payload = {
        'version': '1.1',
        "short_message": msg_short,
        "full_message": msg_full,
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
        gelf_payload.update({
            '_{}'.format(extra_field): extra_value
        })

    print(json.dumps(gelf_payload))


def configure_gelf_output() -> logger:
    logger.__class__.emergency = partialmethod(logger.__class__.log, "emergency")
    logger.__class__.alert = partialmethod(logger.__class__.log, "alert")
    logger.__class__.critical = partialmethod(logger.__class__.log, "critical")
    logger.__class__.error = partialmethod(logger.__class__.log, "error")
    logger.__class__.warning = partialmethod(logger.__class__.log, "warning")
    logger.__class__.notice = partialmethod(logger.__class__.log, "notice")
    logger.__class__.success = partialmethod(logger.__class__.log, "success")
    logger.__class__.informational = partialmethod(logger.__class__.log, "informational")
    logger.__class__.info = partialmethod(logger.__class__.log, "info")
    logger.__class__.debug = partialmethod(logger.__class__.log, "debug")
    logger.__class__.trace = partialmethod(logger.__class__.log, "trace")

    logger.level("emergency", no=0)
    logger.level("alert", no=1)
    logger.level("critical", no=2)
    logger.level("error", no=3)
    logger.level("warning", no=4)
    logger.level("notice", no=5)
    logger.level("success", no=5)
    logger.level("informational", no=6)
    logger.level("info", no=6)
    logger.level("debug", no=7)
    logger.level("trace", no=7)

    filter_syslog_levels = _FilterSyslogLevels(os.getenv('GELFGURU_LEVEL', 'debug'))
    logger.configure(
        handlers=[
            dict(sink=_gelf_sink, filter=filter_syslog_levels, format='{level}', serialize=True, level=0)
        ]
    )

    return logger
