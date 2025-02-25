import logging
import logging.handlers

from .schema import WorkerCfg
from .. import ctx


KiB = 1024
MiB = 1024 * KiB


def configure_logging(cfg: WorkerCfg) -> None:
    FORMAT = "%(levelname)s - trace_id=%(trace_id)s - %(asctime)s - module=%(name)s - func=%(funcName)s - %(message)s"
    syslog_formatter = logging.Formatter(FORMAT)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    filelog_cfg = cfg.loggers.rotating_file
    filelog = logging.handlers.RotatingFileHandler(
        filename=filelog_cfg.filename,
        maxBytes=100 * MiB if filelog_cfg.max_bytes is None else filelog_cfg.max_bytes,
    )
    filelog.addFilter(CtxFilter())
    filelog.setFormatter(syslog_formatter)

    syslog = logging.StreamHandler()
    syslog.addFilter(CtxFilter())
    syslog.setFormatter(syslog_formatter)

    logger.addHandler(syslog)
    logger.addHandler(filelog)


class CtxFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = ctx.trace_id.get()
        return True
