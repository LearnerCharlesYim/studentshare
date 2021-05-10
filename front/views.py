from django.shortcuts import render,redirect,reverse
from django.views.decorators.http import require_http_methods
from .models import User,Resources,Record,RecordFinish
import os
from django.http import HttpResponse,JsonResponse
from functools import wraps

# Create your views here.
def login_required(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        if 'current_user' in request.session:
            return func(request,*args,**kwargs)
        else:
            return redirect(reverse('index'))
    return inner


def index(request):
    user = None
    if request.session.get('current_user'):
        user = User.objects.get(id=request.session['current_user']['id'])
    return render(request,'news/index.html',context={'user':user})

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

@login_required
def profile(request):
    user = User.objects.get(id=request.session['current_user']['id'])
    resources = user.resources_set.filter(is_remove=False).order_by('-pub_time')
    user.resources_set.filter()
    if request.method == 'GET':
        records = Record.objects.all()
        user_records = []
        for record in records:
            if record.recipient_resources or record.sender_resources in user.resources_set.all():
                user_records.append(record)

        user_finish_records = []
        finish_records = RecordFinish.objects.all()
        for record in finish_records:
            for i in record.sender_resources.all():
                if i in user.resources_set.all():
                    user_finish_records.append(record)
            for j in record.recipient_resources.all():
                if j in user.resources_set.all():
                    user_finish_records.append(record)

        return render(request,'profile.html',context={'user':user,'resources':resources,'user_records':user_records,'user_finish_records':user_finish_records})
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
@login_required
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

@login_required
@require_http_methods(['POST'])
def repwd(request):
    password = request.POST.get('password')
    user = User.objects.get(id=request.session['current_user']['id'])
    user.password = password
    user.save()
    return JsonResponse({'code':200,'message':'修改成功'})

@login_required
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

@login_required
def editres(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        resource = Resources.objects.get(id=id)
        return render(request,'editres.html',context={'resource':resource})
    elif request.method == 'POST':
        id = request.POST.get('id')
        res_name = request.POST.get('res_name')
        type = request.POST.get('type')
        is_free = request.POST.get('is_free')
        desc = request.POST.get('desc')
        img = request.POST.get('img')
        resource = Resources.objects.get(id=id)
        resource.name = res_name
        resource.type = type
        resource.is_free = True if is_free == '1' else False
        resource.desc = desc
        resource.img = img
        resource.save()
        return JsonResponse({'code':200,'message':'编辑成功'})


def resource_index(request):
    # user = User.objects.get(id=request.session['current_user']['id'])
    # resources = user.resources_set.filter(is_remove=False).order_by('-pub_time')
    resources = Resources.objects.filter(is_remove=False).order_by('-pub_time')
    sum = resources.count() % 4

    return render(request,'resource/resource_index.html',context={'resources':resources,'sum':4-sum if sum != 0 else 0})

@require_http_methods(['POST'])
@login_required
def upload_res(request):
    img = request.FILES.get('file')
    from studentshare.settings import BASE_DIR
    path = os.path.join(BASE_DIR,'static/images')

    with open(os.path.join(path,img.name),'wb') as fp:
        for chunk in img.chunks():
            fp.write(chunk)
    return JsonResponse({'code':0,'msg':img.name})

@require_http_methods(['POST'])
@login_required
def del_res(request):
    data_id = request.POST.get('data_id')
    resource = Resources.objects.filter(id=data_id).first()
    resource.is_remove = True
    resource.save()
    return JsonResponse({'code':200,'message':''})

@login_required
def res_detail(request,id):
    user = User.objects.get(id=request.session.get('current_user')['id'])
    resource = Resources.objects.filter(id=id).first()

    return render(request,'resource/resource_detail.html',context={'user':user,'resource':resource})


@login_required
def trading(request):
    user = User.objects.get(id=request.session.get('current_user')['id'])
    if request.method == 'GET':
        id = request.GET.get('id')
        resource = Resources.objects.filter(id=id).first()

        user_resources = user.resources_set.all()
        user_resources_name = [user_resource.name for user_resource in user_resources]
        records = Record.objects.all()
        for record in records:
            if record.recipient_resources.name in user_resources_name:
                user_resources_name.remove(record.recipient_resources.name)
            elif record.sender_resources.name in user_resources_name:
                user_resources_name.remove(record.sender_resources.name)
        return render(request,'trade.html',context={'resource':resource,'user':user,'user_resources_name':user_resources_name})
    if request.method == 'POST':
        id = request.POST.get('id')
        res = request.POST.get('res')
        sender_resources = Resources.objects.filter(name=res).first()
        recipient_resources = Resources.objects.filter(id=id).first()
        record = Record(status=1)
        record.sender_resources = sender_resources
        record.recipient_resources = recipient_resources
        record.save()
        return JsonResponse({'code':200,'message':''})

@require_http_methods(['POST'])
def access_trade(request):
    data_id = request.POST.get('data_id')
    record = Record.objects.get(id=data_id)
    record_finish = RecordFinish(is_success=True)
    record_finish.save()
    record_finish.sender_resources.add(record.sender_resources)
    record_finish.recipient_resources.add(record.recipient_resources)

    record.delete()
    return JsonResponse({'code':200,'message':''})

