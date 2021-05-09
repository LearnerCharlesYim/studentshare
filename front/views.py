from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import User
from django.http import HttpResponse,JsonResponse
# Create your views here.

def index(request):
    return render(request,'news/index.html')

@require_http_methods(["POST"])
def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not User.objects.filter(username=username):
        user = User.objects.create(username=username,password=password)
        user.save()
        return JsonResponse({'code':200,'message':'注册成功'})
    else:
        return JsonResponse({'code':400,'message':'用户名已存在'})

@require_http_methods(['POST'])
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    user = User.objects.filter(username=username,password=password).first()
    if user:
        request.session['user_id'] = user.id
        if remember:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        return JsonResponse({'code':200,'message':'登录成功'})
    else:
        return JsonResponse({'code':400,'message':'用户名或密码错误'})


