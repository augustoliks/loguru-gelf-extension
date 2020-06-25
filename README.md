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

>>> logger.trace('loguru trace calls equals gelfguru debug calls') 

{"version": "1.1", "short_message": "loguru trace calls equals gelfguru debug calls", "full_message": "TRACE\n", "timestamp": "1593048146.440082", "level": 5, "line": 6, "_file": "<ipython-input-1-29f7b6d3520d>", "_context": {"module": "__main__:<module>:6", "process": "MainProcess", "thread": "MainThread"}}

>>> logger.info('Change numeric level value, in the case, is used RFC-5424 numeric level value') 

{"version": "1.1", "short_message": "Change numeric level value, in the case, is used RFC-5424", "full_message": "info\n", "timestamp": "1593048146.440787", "level": 6, "line": 7, "_file": "<ipython-input-1-29f7b6d3520d>", "_context": {"module": "__main__:<module>:7", "process": "MainProcess", "thread": "MainThread"}}

>>> logger.emergency('Implemented RFC-5424 Syslog Severity Logs') 

{"version": "1.1", "short_message": "Implemented RFC-5424 Syslog Severity Logs", "full_message": "emergency\n", "timestamp": "1593048146.441399", "level": 0, "line": 8, "_file": "<ipython-input-1-29f7b6d3520d>", "_context": {"module": "__main__:<module>:8", "process": "MainProcess", "thread": "MainThread"}}

>>> logger.emerg('Implemented RFC-5424 Keyword calls')                                   

{"version": "1.1", "short_message": "Implemented RFC-5424 Keyword calls", "full_message": "emerg\n", "timestamp": "1593048146.441991", "level": 0, "line": 9, "_file": "<ipython-input-1-29f7b6d3520d>", "_context": {"module": "__main__:<module>:9", "process": "MainProcess", "thread": "MainThread"}}
```
