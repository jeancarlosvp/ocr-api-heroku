from PIL import Image
from io import BytesIO
import requests
from app.config import (
    OCR_SPACE_API_KEY,
    OCR_SPACE_URL,
    SEND_GS,
    URL_SENDER_GS
)


def resize_image(image_bytes, target_size=(800, 1200)):
    '''
    Resize image to target size
    '''
    try:
        img = Image.open(BytesIO(image_bytes)).convert('RGB')
        img = img.resize(target_size)
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        resized_image_bytes = buffered.getvalue()
        
        return resized_image_bytes
    except Exception as e:
        return {"detail":str(e)}

def process_image_file(file):
    '''
    Process image file to extract text
    '''
    try:
        resize_image = None
        # resize_image = resize_image(file.file.read())
        resize_image = file.file.read()
        if resize_image is None:
            return {"detail":"Error processing image"}
        ocr_space_payload = {
            'apikey': OCR_SPACE_API_KEY,
            'language': 'eng',
            'OCRengine': 2
        }
        response = requests.post(
            OCR_SPACE_URL,
            files={'file': ('image.jpg', resize_image)},
            data=ocr_space_payload,
        )
        ocr_result = response.json()
        parsed_text = [item["ParsedText"].upper() for item in ocr_result["ParsedResults"]]
        result_list = [texto for texto in parsed_text[0].split('\n') if texto.strip()]

        return result_list

    except Exception as e:
        return {"detail":str(e)}
    

def send_data_to_gs(matches_dict):
    '''
    Send data to Google Sheets
    '''
    try:
        if SEND_GS == "True":
            dict_translate = {
                "date_payment": "",
                "dni": matches_dict.get("DNI", ""),
                "total": matches_dict.get("Total", ""),
                "bank": matches_dict.get("Banco", ""),
                "mode_payment": "DS",
                "operation_code": matches_dict.get("Codigo de operacion", ""),
                "card_number": matches_dict.get("Numero tarjeta", "")
            }
            response = requests.post(
                URL_SENDER_GS,
                json=dict_translate
            )
            if response.status_code == 201:
                return {"message":response.json(), "data":matches_dict}
            else:
                return {"message":response.json(), "data":matches_dict}
        else:
            return {"detail":"No fue enviado a GS, revisar SEND_GS", "data":matches_dict}
    except Exception as e:
        return {"detail":str(e)}