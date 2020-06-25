# loguru-gelf-extension

A Loguru extension for handling log messages and adapt to GELF payload pattern, without modifying  built-in Loguru methods call.

This library was created especially for applications running in Docker environment with GELF Logging Driver.

Features:
    - Dont modify call methods Loguru, like `logger.trace`, `logger.info`, `logger.info` etc...;
    - Create new methods for `logger` instace, with all [RFC-5424](https://en.wikipedia.org/wiki/Syslog) Severity level;
    - Associates [RFC-5424](https://en.wikipedia.org/wiki/Syslog) Severity Levels Numerical Codes in GELF field.


# Installation

```shell
pip3.7 install gelfguru
```


# How to Use 

If you configure loguru instance with `gelfguru`, you only need to execute:

```python
from loguru import logger
from gelfguru import configure_gelf_output

configure_gelf_output()

logger.trace('loguru trace calls equals gelfguru debug calls')
logger.info('Change numeric level value, in the case, is used RFC-5424 numeric level value')
logger.emergency('Implemented RFC-5424 Syslog Severity Logs')
logger.emerg('Implemented RFC-5424 Keyword calls')
```


## Log Levels

GELF log level is equal to the standard syslog levels.


Value |	Severity	   | Keyword  | Description
:---: |:---:           |:---:     | :---:
0     | Emergency      |  emerg   | System is unusable. A panic condition
1     | Alert          |  alert   | Action must be taken immediately. A condition that should be corrected immediately, such as a corrupted system database.[
2     | Critical       |  crit    | Critical conditions. Hard device errors
3     | Error          |  err     | Error conditions. 
4     | Warning        |  warning | Warning conditions
5     | Notice         |  notice  | Normal but significant condition. Conditions that are not error conditions, but that may require special handling
6     | Informational  |  info    | Informational messages
7     | Debug          |  debug   | Debug-level messages. Messages that contain information normally of use only when debugging a program.


gelfguru implements methods with Severity or Keyword, for example:

```python
>>> import logger
>>> from gelfguru import configure_gelf_output 

>>> configure_gelf_output() 

>>> logger.bind(field_extra='any_field').trace('Extra fields add with .bind() function')

{
  "version": "1.1",
  "short_message": "Extra fields add with .bind() function",
  "full_message": "TRACE\n",
  "timestamp": 1593051186.92822,
  "level": 5,
  "line": 6,
  "_file": "/home/augustoliks/github/loguru-gelf-extension/test.py",
  "_context": {
    "module": "__main__:<module>:6",
    "process": "MainProcess",
    "thread": "MainThread"
  },
  "_field_extra": "any_field"
}

>>> logger.bind(id='6sdaf4das6f34453').info('id bind is trasform to _id_record')

{
  "version": "1.1",
  "short_message": "id bind is trasform to _id_record",
  "full_message": "info\n",
  "timestamp": 1593051186.929191,
  "level": 6,
  "line": 7,
  "_file": "/home/augustoliks/github/loguru-gelf-extension/test.py",
  "_context": {
    "module": "__main__:<module>:7",
    "process": "MainProcess",
    "thread": "MainThread"
  },
  "_id_record": "6sdaf4das6f34453"
}
```
