import logging

from ..schemas.config import ApiCfg

from .. import ctx


def configure_logging(cfg: ApiCfg) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    syslog = logging.StreamHandler()
    syslog.addFilter(CtxFilter())
    formatter = logging.Formatter("%(levelname)s:trace_id=%(trace_id)s:%(message)s")
    syslog.setFormatter(formatter)

    logger.addHandler(syslog)


class CtxFilter(logging.Filter):
    def filter(self, record):
        trace_id = ctx.trace_id.get()
        record.trace_id = trace_id
        return True
