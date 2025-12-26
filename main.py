import time
from app.bootstrap import create_app
from core.logger import setup_logger


def main():
    logger = setup_logger()
    use_cases, storage, config = create_app()
    try:
        with storage:
            while True:
                    use_cases.execute()
                    time.sleep(config.interval)

    except KeyboardInterrupt:
        logger.info("Stopping Application")


if __name__ == "__main__":
    main()
