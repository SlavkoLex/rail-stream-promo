import type { OrderData } from "@/types/OrderDataTypes.ts";

export const OrderRecordAPI = {
  async createOrderRecord(backend: string, orderData: OrderData) {
    const response = await fetch(backend, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(orderData),
    });

    return response.json();
  },
};
