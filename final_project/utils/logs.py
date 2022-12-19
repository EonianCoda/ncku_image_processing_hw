def setup_logging(level='info', log_file=None):
    """Initialize logging settings."""
    import logging
    from logging import basicConfig

    from rich.console import Console
    from rich.logging import RichHandler

    if isinstance(level, str):
        level = level.upper()

    handlers = []
    if log_file:
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s %(filename)s:%(lineno)d'
        )
        fh.setFormatter(formatter)
        handlers.append(fh)

    console = Console(width=160)
    handlers.append(RichHandler(console=console))
    basicConfig(level=level, format='%(message)s',
                datefmt='[%X]', handlers=handlers)