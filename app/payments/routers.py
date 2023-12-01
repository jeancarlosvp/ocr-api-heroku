from fastapi import APIRouter,Request, status, UploadFile
from typing import Union
from app.security import valid_header
from app.config import API_KEY
from app.payments.services import process_image_file, send_data_to_gs
from app.payments.utils import select_bank, get_bank_data

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def send_file_payment(file:Union[UploadFile, None], request: Request):
    try:
        valid_header(request, API_KEY)
        if not file:
            return {"detail":"File not found"}
        result_list = process_image_file(file)
        print(result_list)
        selection = select_bank(result_list)
        print(f"selection: {selection}")
        matches_dict = get_bank_data(selection, result_list)
        print (f"matches_dict: {matches_dict}")
        if matches_dict:
            return send_data_to_gs(matches_dict)
        else:
            return {"detail":"Error procesando la imagen", "data":matches_dict}
    except Exception as e:
        return {"detail":str(e)}