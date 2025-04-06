from django.shortcuts import render
from openai import OpenAI
from dotenv import load_dotenv
from django.http import JsonResponse
import os
from .models import Chat

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPEN_ROUTER_API_KEY")
)


# Create your views here.
def index(request):
    return render(request, "index.html")


def response(request):
    if request.method == "POST":
        message = request.POST.get("message", " ")

        completion = client.chat.completions.create(
            model="qwen/qwen-2.5-7b-instruct:free",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
        )
        answer = completion.choices[0].message.content
        new_chat = Chat(message=message, response=answer)
        new_chat.save()
        print("Berhasil menambahkan")

        return JsonResponse({"response": answer})
    return JsonResponse({"response": "Invalid Request"}, status=400)
