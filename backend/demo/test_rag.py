from services.ai.chat_service import ai_chat_service

response = ai_chat_service.chat(

    message="what is the contents in my file",

    session_id="e56b6c98-cc30-4d31-9bed-0b423e4455b2",

)

print(response)