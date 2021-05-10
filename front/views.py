from django.shortcuts import render,redirect,reverse
from django.views.decorators.http import require_http_methods
from .models import User,Resources,Record
import os
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
        request.session['current_user'] = {
            'id':user.id,
            'username':user.username,
            'realname':user.realname,
            'password':user.password,
            'telephone':user.telephone,
            'signature':user.signature,
            'avatar':user.avatar,
            'is_admin':user.is_admin,
            'is_banned':user.is_banned
        }
        if remember:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        return JsonResponse({'code':200,'message':'登录成功'})
    else:
        return JsonResponse({'code':400,'message':'用户名或密码错误'})

@require_http_methods(['GET'])
def logout(request):
    request.session.flush()
    return redirect(reverse('index'))

def profile(request):
    user = User.objects.get(id=request.session['current_user']['id'])
    resources = user.resources_set.filter(is_remove=False)
    if request.method == 'GET':
        return render(request,'profile.html',context={'user':user,'resources':resources})
    else:
        username = request.POST.get('username')
        if User.objects.filter(username=username) and user.username != username:
            return JsonResponse({'code':400,'message':'该用户名已注册'})
        else:
            realname = request.POST.get('realname')
            telephone = request.POST.get('telephone')
            signature = request.POST.get('signature')
            user.username = username
            user.realname = realname
            user.telephone = telephone
            user.signature = signature
            user.save()

            return JsonResponse({'code':200,'message':'修改成功'})



@require_http_methods(['POST'])
def upload(request):
    avatar = request.FILES.get('file')
    user = User.objects.get(id=request.session['current_user']['id'])
    from studentshare.settings import BASE_DIR
    path = os.path.join(BASE_DIR,'static/images')
    user.avatar = avatar.name
    user.save()
    with open(os.path.join(path,avatar.name),'wb') as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)
    return JsonResponse({'code':0,'msg':avatar.name})


@require_http_methods(['POST'])
def repwd(request):
    password = request.POST.get('password')
    user = User.objects.get(id=request.session['current_user']['id'])
    user.password = password
    user.save()
    return JsonResponse({'code':200,'message':'修改成功'})


def addres(request):
    user = User.objects.get(id=request.session['current_user']['id'])
    if request.method == 'GET':
        return render(request,'addres.html')
    elif request.method == 'POST':
        res_name = request.POST.get('res_name')
        type = request.POST.get('type')
        is_free = request.POST.get('is_free')
        desc = request.POST.get('desc')
        img = request.POST.get('img')
        resource = Resources(name=res_name,desc=desc,type=int(type),is_free=True if is_free == '1' else False,img=img)
        resource.owner = user
        resource.save()
        return JsonResponse({'code':200,'message':'添加成功'})


def resource_index(request):
    user = User.objects.get(id=request.session['current_user']['id'])
    resources = user.resources_set.filter(is_remove=False)
    return render(request,'resource/resource_index.html',context={'resources':resources})

@require_http_methods(['POST'])
def upload_res(request):
    img = request.FILES.get('file')
    from studentshare.settings import BASE_DIR
    path = os.path.join(BASE_DIR,'static/images')

    with open(os.path.join(path,img.name),'wb') as fp:
        for chunk in img.chunks():
            fp.write(chunk)
    return JsonResponse({'code':0,'msg':img.name})

@require_http_methods(['POST'])
def del_res(request):
    data_id = request.POST.get('data_id')
    resource = Resources.objects.filter(id=data_id).first()
    resource.is_remove = True
    resource.save()
    return JsonResponse({'code':200,'message':''})