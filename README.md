[![PyPI version](https://badge.fury.io/py/gelfguru.svg)](https://badge.fury.io/py/gelfguru)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ecc1f25454164ff78e432f5a126563cb)](https://www.codacy.com/manual/augustoliks/loguru-gelf-extension?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=augustoliks/loguru-gelf-extension&amp;utm_campaign=Badge_Grade)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# gelfguru

A Loguru extension for handling log messages and adapt to GELF payload pattern, without modifying  built-in Loguru methods call.
This library was created especially for applications running in Docker environment with GELF Logging Driver.

Features:
- Dont modify call methods Loguru, like `logger.trace`, `logger.info`, `logger.info` etc;
- Create new methods for `logger` instance, with all [RFC-5424](https://en.wikipedia.org/wiki/Syslog) Severity level;
- Associates [RFC-5424](https://en.wikipedia.org/wiki/Syslog) Severity Levels Numerical Codes in GELF field.
- Filter logs by environment variable `GELFGURU_LEVEL`.

# Installation

```shell
pip3.7 install gelfguru
```

# How to Use 

If you configure Loguru instance with `gelfguru`, you only need to execute:

```python
from loguru import logger
from gelfguru import configure_gelf_output

configure_gelf_output()

logger.trace('loguru trace calls equals gelfguru debug calls')
logger.info('Numeric level RFC-5424')
logger.emergency('Implemented RFC-5424 Syslog Severity Logs')
```

## Log Levels

GELF log level is equal to the standard syslog levels.

| gelfluru             | Syslog Severity  | Numerical Code   | Description
|:---:                 |:---:             | :---:            | :---:
|  `emergency`         | Emergency        | 0                | System is unusable. A panic condition
|  `alert`             | Alert            | 1                | Action must be taken immediately. A condition that should be corrected immediately, such as a corrupted system database.[
|  `critical`          | Critical         | 2                | Critical conditions. Hard device errors
|  `error`             | Error            | 3                | Error conditions. 
|  `warning`           | Warning          | 4                | Warning conditions
|  `success`, `notice` | Notice           | 5                | Normal but significant condition. Conditions that are not error conditions, but that may require special handling
|  `info`              | Informational    | 6                | Informational messages
|  `debug`, `trace`    | Debug            | 7                | Debug-level messages. Messages that contain information normally of use only when debugging a program.

Example:

```python
from loguru import logger                                                                             
from gelfguru import configure_gelf_output                                                            

configure_gelf_output()                                                                               

logger.trace('loguru trace calls equals gelfguru debug calls')                                        
# {
#   "version": "1.1",
#   "short_message": "trace\n",
#   "full_message": "trace\n",
#   "timestamp": 1593137655.309429,
#   "level": 7,
#   "line": 1,
#   "_file": "<ipython-input-4-698cb139534b>",
#   "_context": {
#     "module": "__main__:<module>:1",
#     "process": "MainProcess",
#     "thread": "MainThread"
#   }
# }

logger.info('Change numeric level value, in the case, is used RFC-5424 numeric level value')          
# {
#   "version": "1.1",
#   "short_message": "Change numeric level value, in the case, is used RFC-5424",
#   "full_message": "Change numeric level value, in the case, is used RFC-5424 numeric level value",
#   "timestamp": 1593137655.42884,
#   "level": 6,
#   "line": 1,
#   "_file": "<ipython-input-5-d527b5b194dc>",
#   "_context": {
#     "module": "__main__:<module>:1",
#     "process": "MainProcess",
#     "thread": "MainThread"
#   }
# }

logger.emergency('Implemented RFC-5424 Syslog Severity Logs')                                         
# {
#   "version": "1.1",
#   "short_message": "Implemented RFC-5424 Syslog Severity Logs",
#   "full_message": "Implemented RFC-5424 Syslog Severity Logs",
#   "timestamp": 1593137657.236526,
#   "level": 0,
#   "line": 1,
#   "_file": "<ipython-input-6-5c45ca4c1de6>",
#   "_context": {
#     "module": "__main__:<module>:1",
#     "process": "MainProcess",
#     "thread": "MainThread"
#   }
# }

logger.bind(new_field="i am additional filed gelf").error('iste natus error sit')
# {
#   "version": "1.1",
#   "short_message": "iste natus error sit",
#   "full_message": "iste natus error sit",
#   "timestamp": 1593138435.430722,
#   "level": 3,
#   "line": 18,
#   "_file": "/home/augustoliks/github/loguru-gelf-extension/tests/test_loguru_gelf_extension.py",
#   "_context": {
#     "module": "test_loguru_gelf_extension:test_loguru_calls:18",
#     "process": "MainProcess",
#     "thread": "MainThread"
#   },
#   "_new_field": "i am additional filed gelf"
# }
```