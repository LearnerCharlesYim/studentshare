from django.shortcuts import render
from front.models import User,Resources,Record,RecordFinish
from django.http import  JsonResponse
from .models import Banner
# Create your views here.

def index(request):
    user = User.objects.get(id=request.session['current_user']['id'])
    return render(request,'cms/index.html',context={'user':user})

def user_manage(request):
    user = User.objects.get(id=request.session['current_user']['id'])
    front_users = User.objects.all()
    return render(request,'cms/user_manage.html',context={'user':user,'front_users':front_users})

def banned_user(request):
     if request.method == 'POST':
         id = request.POST.get('id')
         user = User.objects.get(id=id)
         user.is_banned = True
         user.save()
         return JsonResponse({'code':200,'message':''})


def liftbanned_user(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = User.objects.get(id=id)
        user.is_banned = False
        user.save()
        return JsonResponse({'code': 200, 'message': ''})

def wait_to_access(request):
    user = User.objects.get(id=request.session['current_user']['id'])
    resources = Resources.objects.filter(is_access=False,is_remove=False).order_by('-pub_time')
    return render(request,'cms/wait_to_access.html',context={'user':user,'resources':resources})

def access_res(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        resource = Resources.objects.get(id=id)
        resource.is_access = True
        resource.save()
        return JsonResponse({'code':200,'message':''})

def delete_res(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        resource = Resources.objects.get(id=id)
        resource.delete()
        return JsonResponse({'code':200,'message':''})

def res_list(request):
    user = User.objects.get(id=request.session['current_user']['id'])
    resources = Resources.objects.filter(is_access=True,is_remove=False).order_by('-pub_time')
    return render(request, 'cms/res_list.html', context={'user': user, 'resources': resources})

def edit_res(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        type = request.POST.get('type')
        resource = Resources.objects.get(id=id)
        resource.type = int(type)
        resource.save()
        return JsonResponse({'code': 200, 'message': ''})

def remove_res(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        resource = Resources.objects.get(id=id)
        resource.is_remove = True
        resource.save()
        return JsonResponse({'code': 200, 'message': ''})

def trade_manage(request):
    user = User.objects.get(id=request.session['current_user']['id'])
    records = Record.objects.order_by('-trade_time').all()
    return render(request,'cms/trade_manage.html',context={'user':user,'records':records})

def trade_access(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        record = Record.objects.get(id=id)
        # 交换物品
        temp = record.sender_resources.owner
        record.sender_resources.owner = record.recipient_resources.owner
        record.recipient_resources.owner = temp
        record.sender_resources.save()
        record.recipient_resources.save()
        # 建立完成记录
        record_finish = RecordFinish(is_success=True)
        record_finish.save()
        record_finish.recipient_resources = record.recipient_resources
        record_finish.sender_resources = record.sender_resources
        record_finish.sender = record.sender_resources.owner
        record_finish.receiver = record.recipient_resources.owner
        record_finish.save()

        record.delete()
        return JsonResponse({'code':200,'message':''})

def trade_cancel(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        record = Record.objects.get(id=id)
        record.delete()
        return JsonResponse({'code':200,'message':''})

def banner(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.session['current_user']['id'])
        banners = Banner.objects.all()
        return render(request,'cms/banners.html',context={'user':user,'banners':banners})
    else:
        name = request.POST.get('name')
        priority = request.POST.get('priority')
        path = request.POST.get('path')
        banner = Banner(name=name,priority=priority,path=path)
        banner.save()
        return JsonResponse({'code':200,'message':''})


def upload_banner(request):
    if request.method == 'POST':
        banner = request.FILES.get('file')
        from studentshare.settings import BASE_DIR
        import os
        path = os.path.join(BASE_DIR, 'static/images/banners')
        with open(os.path.join(path, banner.name), 'wb') as fp:
            for chunk in banner.chunks():
                fp.write(chunk)
        return JsonResponse({'code': 0, 'msg': banner.name})

def edit_banner(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        priority = request.POST.get('priority')
        path = request.POST.get('path')
        banner = Banner.objects.get(id=id)
        banner.name = name
        banner.priority = priority
        banner.path = path
        banner.save()
        return JsonResponse({'code': 200, 'message': ''})

def delete_banner(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        banner = Banner.objects.get(id=id)
        banner.delete()
        return JsonResponse({'code': 200, 'message': ''})