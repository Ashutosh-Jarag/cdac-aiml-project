from services.providers.gemini_provider import gemini_provider

response = gemini_provider.generate(
    "Say Hello from ResearchAI"
)

print(response)