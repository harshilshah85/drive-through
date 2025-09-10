from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from openai import OpenAI
import os

app = FastAPI()

# Add CORS middleware after app is defined
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# In-memory order store
orders = []
order_counter = 1

# Set your OpenAI API key here or via environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key")
client = OpenAI(api_key=OPENAI_API_KEY)

ORDER_ITEMS = ["burger", "fries", "drink"]

class Order(BaseModel):
    order_id: int
    items: Dict[str, int]  # e.g., {"burger": 2, "fries": 1}

class UserRequest(BaseModel):
    text: str

@app.get("/orders", response_model=List[Order])
def get_orders():
    return orders

@app.get("/orders/total")
def get_total_items():
    total = {item: 0 for item in ORDER_ITEMS}
    for order in orders:
        for item, qty in order['items'].items():
            total[item] += qty
    return {"total": total}

@app.post("/orders")
def place_or_cancel_order(req: UserRequest):
    """
    Uses OpenAI function calling to parse the user request and place/cancel orders.
    """
    global order_counter
    # Call OpenAI function calling API
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": req.text}],
        functions=[
            {
                "name": "place_order",
                "description": "Place a new order with items and quantities.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "object",
                            "properties": {item: {"type": "integer", "minimum": 1} for item in ORDER_ITEMS},
                            "additionalProperties": False,
                        }
                    },
                    "required": ["items"]
                }
            },
            {
                "name": "cancel_order",
                "description": "Cancel an existing order by order_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "integer"}
                    },
                    "required": ["order_id"]
                }
            }
        ],
        function_call="auto"
    )
    choice = response.choices[0]
    if choice.finish_reason == "function_call":
        fn = choice.message.function_call
        import json
        args = json.loads(fn.arguments)
        if fn.name == "place_order":
            items = {k: v for k, v in args['items'].items() if v > 0}
            if not items:
                raise HTTPException(status_code=400, detail="No valid items in order.")
            order = {"order_id": order_counter, "items": items}
            orders.append(order)
            order_counter += 1
            return {"message": f"Order placed! Order #{order['order_id']}", "order": order}
        elif fn.name == "cancel_order":
            oid = args['order_id']
            for i, order in enumerate(orders):
                if order['order_id'] == oid:
                    orders.pop(i)
                    return {"message": f"Order #{oid} cancelled."}
            raise HTTPException(status_code=404, detail=f"Order #{oid} not found.")
    raise HTTPException(status_code=400, detail="Could not understand request.")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
