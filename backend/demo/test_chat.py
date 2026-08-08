from services.ai.chat_service import ai_chat_service

response = ai_chat_service.chat(

    message="Explain Artificial Intelligence.",

    session_id="demo",

)

print(response)