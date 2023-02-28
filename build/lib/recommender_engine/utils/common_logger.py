import uvicorn
import logging
import os

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    datefmt="%Y-%m-%dT%H:%M",
    format="[%(asctime)s.%(msecs)03dZ]: %(levelname)s: [%(module)s - L%(lineno)d] %(message)s",
)

LOGGER = logging.getLogger("transcript-service")

# Add uvicorn error handler
log_config = uvicorn.config.LOGGING_CONFIG
format_string = "[%(asctime)s.%(msecs)03dZ]:  - %(levelname)s - %(message)s"
log_config["formatters"]["access"]["fmt"] = format_string
log_config["formatters"]["default"]["fmt"] = format_string

# Handle logging for the docker container
logger = logging.getLogger("uvicorn.access")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(handler)
