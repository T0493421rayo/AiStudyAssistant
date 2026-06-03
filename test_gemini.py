from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6LL1wre2YFfh22h-Ma9VpQ2pi_5Lo9lb5-EldDs1jedyQ"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello in one sentence."
)

print(response.text)