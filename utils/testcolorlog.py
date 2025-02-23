import logging
import colorlog

class MyClass:
    # Logger erstellen und konfigurieren
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Handler und Formatter für farbige Ausgaben erstellen
        handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            '%(asctime)s - %(log_color)s%(levelname)-8s%(reset)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def do_something(self):
        self.logger.debug("Dies ist eine Debug-Nachricht")
        self.logger.info("Dies ist eine Info-Nachricht")
        self.logger.warning("Dies ist eine Warnung")
        self.logger.error("Dies ist ein Fehler")
        self.logger.critical("Dies ist eine kritische Nachricht")


# Instanziiere die Klasse und rufe eine Methode auf
obj = MyClass()
obj.do_something()
