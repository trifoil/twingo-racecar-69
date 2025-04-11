import logging
import logging.handlers
import sys
import os

class Logging_Utils():
    logging_folder = "logs"
    logging_file_size_bytes = 500000
    backup_count = 2
    logging_format = "| %(levelname)s | %(asctime)s | %(filename)s:%(lineno)s | %(message)s"

    @staticmethod
    def setup_logging_in_main(verbose: bool = True, write_file: bool = True, log_info: bool = False):
        """
        Méthode qui permet de réinitialiser / mettre en place le système de logging. Elle doit être appelée au moins une fois dans l’arborescence du code, peu importe le niveau.
        :param verbose: si les logs doivent être affichés dans la console
        :param write_file: si les logs doivent être enregistrés dans les fichiers de logging
        :param log_info: si les informations (capteurs/actionneurs) doivent être ajoutées aux logs
        """
        logger = __class__.get_logger()
        __class__._reset_logging(logger)
        if verbose: __class__._setup_terminal_logging(logger)
        if write_file: __class__._setup_file_logging(logger)
        __class__._setup_logging_level(logger, log_info)
        
        if not (write_file or verbose):
            logger.addHandler(logging.NullHandler())


    @staticmethod
    def _setup_terminal_logging(logger):
        """
        Ajoute le logging dans la console du logger passé en paramètre.
        :param logger: le logger en question
        """
        stdout = logging.StreamHandler(stream=sys.stdout)
        formater = logging.Formatter(__class__.logging_format)
        stdout.setFormatter(formater)
        logger.addHandler(stdout)


    @staticmethod
    def _setup_file_logging(logger):
        """
        Ajoute le logging dans un fichier du logger passé en paramètre.
        :param logger: le logger en question
        """
        __class__._setup_file_logging_directory()
        fileWriting = logging.handlers.RotatingFileHandler(
            __class__.logging_folder+"/current_logs.txt",
            maxBytes=__class__.logging_file_size_bytes,
            backupCount=__class__.backup_count
        )
        formater = logging.Formatter(__class__.logging_format)
        fileWriting.setFormatter(formater)
        logger.addHandler(fileWriting)


    @staticmethod
    def _setup_file_logging_directory():
        """Crée le dossier des logs s'il n'existe pas."""
        if not os.path.isdir(__class__.logging_folder):
            os.makedirs(__class__.logging_folder)


    @staticmethod
    def _reset_logging(logger):
        """
        Retire tous les handlers du logger passé en paramètre.
        :param logger: le logger en question
        """
        for hdl in logger.handlers:
            logger.removeHandler(hdl)


    @staticmethod
    def _setup_logging_level(logger, log_info: bool):
        """
        Change le niveau de log en fonction de si log_info est activé ou non.
        :param log_info: s'il faut activer ou non le logging des informations capteurs/actionneurs/...
        """
        if log_info: logger.setLevel(logging.INFO)


    @staticmethod
    def get_logger():
        """Retourne le logger de l'application"""
        return logging.getLogger("__main__")