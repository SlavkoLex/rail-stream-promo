from typing import Optional, Union
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from celery import Celery
from bson.objectid import ObjectId
from celery.result import AsyncResult
from celery.exceptions import OperationalError
from kombu.exceptions import OperationalError as KombuError

from data.models.order_model import OrderModel
from data.models.error_response_model import ErrorResponse
from data.models.success_response_model import SuccessResponseData, SuccessResponse
from utils.email_checker import email_check


order_router = APIRouter(prefix="/api", tags=["orders"])

#==============================
# The main method that accepts the Order form
#==============================
@order_router.post("/save/form/order")
async def register_order(request: Request,order: OrderModel) -> dict[str, Union[str, int]]:

    #===============================
    #email address validation
    #===============================
    validation_result = email_check(order.model_dump().get("email"))

    #TODO: Добавить валидацию оргинизации и номера телефона при условии что данные поля не None !!!!!


    if validation_result:

        #==============================
        # Saving order information in the database
        #============================== 
        mongo_result: Optional[ObjectId] = await request.app.state.order_rep.post_order_info(order)

        if mongo_result is None:
            #TODO: ЛОГИРОВАТЬ ОШИБКУ!!
            print("=======================")
            print("Mongo Error: The data is not saved!!")
            print("=======================")

            error_response = ErrorResponse(
                title="Database Error",
                status=500,
                detail="The order data could not be saved. Try again later",
                instance="/api/save/form/order"
            )

            return JSONResponse(
                status_code=error_response.status,
                content=error_response.model_dump()
            )

        #==============================
        # Send a message to the Mail Collector
        #==============================
        celery_client: Celery = request.app.state.celery.get_celery_object()


        try:
            celery_result: AsyncResult = celery_client.send_task(
                    "send_gmail_notification_about_order", 
                    args = [order.model_dump().get("timestamp"), 
                            order.model_dump().get("email"), 
                            order.model_dump().get("product"), 
                            order.model_dump().get("organization"), 
                            order.model_dump().get("phone")]
                    )
        except OperationalError as e:
            #TODO: ЛОГИРОВАТЬ ОШИБКУ!!
            print("=======================")
            print(f"Celery Error: Connection error with the Celery broker -> {e}")
            print("=======================")

        except KombuError as ek:
            #TODO: ЛОГИРОВАТЬ ОШИБКУ!!
            print("=======================")
            print(f"Celery Error: Routing error when sending a Celery worker task -> {ek}")
            print("=======================")

        except Exception as ex:
            #TODO: ЛОГИРОВАТЬ ОШИБКУ!!
            print("=======================")
            print(f"Celery Error: Possible incorrect specification of arguments for the task -> {ex}")
            print("=======================")

            
        try:
            await request.app.state.celery.wait_task_result(celery_result.id)    
        except Exception as e:
            #TODO: ЛОГИРОВАТЬ ОШИБКУ!!
            print("=======================")
            print(f"Celery Error: Getting the Celery result failed -> {e}")
            print("=======================")

        success_response = SuccessResponse(
            data=SuccessResponseData(
                email=order.model_dump().get("email"),
                organization=order.model_dump().get("organization"),
                phone=order.model_dump().get("phone"),
                product=order.model_dump().get("product"),
                createdAt=order.model_dump().get("timestamp").strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        return JSONResponse(
                content=success_response.model_dump()
            )
    
    else:

        error_response = ErrorResponse(
                title="Email Error",
                status=400,
                detail="The email value is not valid",
                instance="/api/save/form/order"
        )

        return JSONResponse(
                status_code=error_response.status,
                content=error_response.model_dump()
            )
