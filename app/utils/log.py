import os
import datetime
import logging
from logging.handlers import RotatingFileHandler, BaseRotatingHandler
from config import log_dir


class DayRotatingHandler(BaseRotatingHandler):
    def __init__(self, filename, mode, encoding=None, delay=False):
        self.date = datetime.date.today()
        self.suffix = "%Y-%m-%d.log"
        super(BaseRotatingHandler, self).__init__(filename, mode, encoding,
                                                  delay)

    def shouldRollover(self, record):
        return self.date != datetime.date.today()

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        new_log_file = os.path.join(
            os.path.split(self.baseFilename)[0],
            datetime.date.today().strftime(self.suffix))
        self.baseFilename = "{}".format(new_log_file)
        self._open()


def register_logging(app):
    app.logger.name = 'flask_api'
    log_level = app.config.get("LOG_LEVEL", logging.INFO)
    cls_handler = logging.StreamHandler()
    log_file = os.path.join(log_dir,
                            datetime.date.today().strftime("%Y-%m-%d.log"))
    file_handler = DayRotatingHandler(log_file, mode="a", encoding="utf-8")

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(name)s "
        "%(filename)s[%(lineno)d] %(funcName)s() %(levelname)s: %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        handlers=[cls_handler, file_handler])

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(os.path.join(
                log_dir, 'flask_api.log'),
                                               maxBytes=1024 * 1024 * 50,
                                               backupCount=5,
                                               encoding='utf-8')
            file_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s %(name)s %(levelname)s: %(message)s '
                    '[in %(pathname)s:%(lineno)d]'))

            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
