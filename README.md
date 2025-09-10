# Instructions

Create a mock drive thru ordering system that allows users to place and cancel their orders using AI.

![Example UI](./image.png)

For this project, assume the order item options are either 1) burgers, 2) fries, or 3) drinks. 

These are examples of user inputs and the corresponding actions to take:
* "I would like to order a burger" -> order of 1 burger
* "My friend and I would each like a fries and a drink" -> order for 2 fries, 2 drinks
* "Please cancel my order, order #2" -> cancel order #2

You will need an LLM to figure out the actions, you cant just search the text for keywords in general. You can assume every user input is either for an order and includes the items to order, or a cancellation with the order number to cancel, but the exact text and structure of the sentences could vary.

# Setup

See backend/README.md and frontend/README.md for setup instructions

# Criteria

1. Create a UI in Svelte that shows the total number of items that have been ordered, a list of placed orders and has a single text box for new user requests
2. Implement a backend using FastAPI that uses OpenAI's function calling to allow users to place or cancel their orders
3. Orders can contain one or multiple items and 1 or multiple quantities of each item
4. Placing or cancelling orders should be reflected in the UI

# Other Considerations

Please think through and be able to talk about the following considerations:

* validating user inputs
* multi-tenant access
* extensibility for example, new functions being added
* testing and reliability
