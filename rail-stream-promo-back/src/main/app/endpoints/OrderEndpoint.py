from fastapi import APIRouter, Request

from data.models.OrderModel import OrderModel
from services.tools.EmailChecker import email_check


order_router = APIRouter(prefix="/api", tags=["orders"])

#==============================
# The main method that accepts the Order form
#==============================
@order_router.post("/save/form/order")
async def registerOrder(request: Request,order: OrderModel):

    validation_result = email_check(order.model_dump().get("email"))

    if validation_result:
        # A . TODO Сохранить данные в БД

        #==============================
        #Send a message to the Mail Collector
        #==============================
        request.app.state.celery.send_task(
            "send_gmail_notification_about_order",
            args=None, 
            date_order=order.model_dump().get("timestamp"), 
            client_email = order.model_dump().get("email"), 
            product = order.model_dump().get("product"), 
            organization = order.model_dump().get("organization"), 
            cient_number = order.model_dump().get("phone"))
        
        return {"success": 200}
    else:
        {"email invalid": 400}
