from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Subscriber
from .bot_message import bot
from django.contrib import messages
import re


def index_view(request):
    return render(request, 'index.html')


def handler404(request, exception):
    return render(request, '404.html', status=404)


def subscribe_view(request):
    if request.method != 'POST':
        return render(request, 'index.html')

    email = request.POST.get('email')

    try:
        validate_email(email)
    except ValidationError:
        # Если email не проходит валидацию, вы можете обработать ошибку
        return render(request, 'index.html') 

    print(email)

    try:
        subscriber = Subscriber.objects.get(email=email)
        # Если email уже существует, не выполняем действий и просто перенаправляем пользователя
        return HttpResponseRedirect('/') 
    except Subscriber.DoesNotExist:
        # Если email не существует, добавляем его в базу данных
        subscriber = Subscriber(email=email)
        subscriber.save()

    return HttpResponseRedirect('/') 


def message_text(request):
    if request.method != 'POST':
        return render(request, 'index.html')
    
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    comments = request.POST.get('comments')


    digits_only = re.sub(r'\D', '', phone)

    try:
        phone = int(digits_only)
    except:
        return

    # Отправка сообщения в Telegram
    message = f"Новая заявка:\nИмя: {name}\nНомер: {digits_only}\nСообщение: {comments}"
    chat_id = '-1001944585110'  # Замените на ID вашего чата в Telegram

    bot.send_message(chat_id ,message)
    
    messages.success(request, 'Сообщение успешно отправлено!')
    # После успешной обработки данных, перенаправьте пользователя на главную страницу
    return HttpResponseRedirect('/')
    

    

    

