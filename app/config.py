from starlette.config import Config

config = Config("./.env")

CORS_ORIGINS = config("CORS_ORIGINS")
API_KEY = config("API_KEY")
SEND_GS = config("SEND_GS")
URL_SENDER_GS = config("URL_SENDER_GS")

OCR_SPACE_URL = config("OCR_SPACE_URL")
OCR_SPACE_API_KEY = config("OCR_SPACE_API_KEY")