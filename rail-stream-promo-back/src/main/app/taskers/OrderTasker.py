from App import app
from data.models.OrderModel import OrderModel

@app.post("api/save/form/order")
async def registerOrder(order: OrderModel):

    # 1. Выполнить валидацию email
    # ПОЛЕ ЯВЛЯЕТСЯ ОБЯЗАТЕЛЬНЫМ 
    # Если не указано вернуть ошибку *Вы не указали email -> Код ошибки: ;
    # Если не пройден validator вернуть ошибку *Указан не верный email -> Код ошибки: 

    # 2. Если email валидный отправить сообщение на админ-почту -> api/save/form/order
    # 3. Сохранить объетк Order в БД.
    pass