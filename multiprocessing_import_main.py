import logging
def import_worker( i ):
    """Worker function"""
    logger = logging.getLogger("import_worker")
    logger.info("%s %d", "Imported Worker", i)
