from django.shortcuts import render
from django.conf import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

def chatbot_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        bot_response = get_chatbot_response(user_input)

        return render(request, 'chatbot.html', {'bot_response': bot_response})

    return render(request, 'templates/chatbot.html')

def get_chatbot_response(user_input):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_input,
        temperature=0.5,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    bot_response = response.choices[0].text.strip()
    return bot_response