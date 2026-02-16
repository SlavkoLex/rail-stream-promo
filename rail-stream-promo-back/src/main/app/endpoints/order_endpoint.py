from typing import Optional
from fastapi import APIRouter, Request
from celery import Celery
from bson.objectid import ObjectId
from celery.result import AsyncResult
from celery.exceptions import OperationalError
from kombu.exceptions import OperationalError as KombuError

from data.models.order_model import OrderModel
from services.tools.email_checker import email_check


order_router = APIRouter(prefix="/api", tags=["orders"])

#==============================
# The main method that accepts the Order form
#==============================
@order_router.post("/save/form/order")
async def register_order(request: Request,order: OrderModel) -> dict[str, int]:

    validation_result = email_check(order.model_dump().get("email"))

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

        return {"success": 200}
    
    else:
        {"email invalid": 400}
