import asyncio
from agents import Agent, RunContextWrapper, Runner
from config.config import model

HOTELS = {
    "Hotel Sannata": "You are helping with Hotel Sannata's booking and info.",
    "Hotel Pearl": "You are helping with Hotel Pearl's booking and info.",
    "Hotel Serena": "You are helping with Hotel Serena's booking and info.",
}

def detect_hotel_from_query(query: str):
    for hotel in HOTELS:
        if hotel.lower() in query.lower():
            return hotel
    return None

def dynamic_instruction(ctx: RunContextWrapper, agent):
    user_name = ctx.context.get("name", "User")
    user_input = getattr(ctx, "input", "") or ""
    
    hotel_name = ctx.context.get("hotel_name") or detect_hotel_from_query(user_input)
    if hotel_name:
        ctx.context["hotel_name"] = hotel_name
    else:
        hotel_name = "our hotels"

    instruction = HOTELS.get(hotel_name, "You are helping with general hotel booking and info.")
    return f"Hello {user_name}, {instruction}"

# Define assistant agent
assistant = Agent(
    name="HotelAssistant",
    instructions=dynamic_instruction,
    model=model,
)

# Run the agent
async def main():
    query = "What are the check-in policies for Hotel Serena?"
    context = {"name": "Ben"}
    result = await Runner.run(assistant, query, context=context)
    print("Agent response:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
