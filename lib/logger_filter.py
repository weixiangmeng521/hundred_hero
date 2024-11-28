import logging


class LoggerFilter(logging.Filter):
    """自定义过滤器，只允许 DEBUG 和 ERROR 级别的日志通过"""
    def filter(self, record):
        return record.levelno in (logging.DEBUG, logging.ERROR)