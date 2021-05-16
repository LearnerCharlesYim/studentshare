"""studentshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from front import views as front_views
from cms import views as cms_views

urlpatterns = [
    path('', front_views.index,name='index'),
    path('signup/',front_views.signup,name='signup'),
    path('login/',front_views.login,name='login'),
    path('logout/',front_views.logout,name='logout'),
    path('profile/',front_views.profile,name='profile'),
    path('upload/',front_views.upload,name='upload'),
    path('repwd/',front_views.repwd,name='repwd'),
    path('addres/',front_views.addres,name='addres'),
    path('resource/',front_views.resource_index,name='resource'),
    path('upload_res/',front_views.upload_res,name='upload_res'),
    path('del_res/',front_views.del_res,name='del_res'),
    path('edit_res/',front_views.editres,name='edit_res'),
    path('resource/detail/<id>/',front_views.res_detail,name='res_detail'),
    path('trading/',front_views.trading,name='trading'),
    path('access/',front_views.access_trade,name='access_trade'),
    path('cancel/',front_views.cancel_trade,name='cancel_trade'),
    path('free/',front_views.free_get,name='free_get'),
    path('cms/',cms_views.index,name='cms_index'),
    path('cms/user/',cms_views.user_manage,name='user_manage'),
    path('cms/banned/',cms_views.banned_user,name='banned_user'),
    path('cms/liftbanned/',cms_views.liftbanned_user,name='liftbanned_user'),
    path('cms/check/',cms_views.wait_to_access,name='wait_to_access'),
    path('cms/check/',cms_views.wait_to_access,name='wait_to_access'),
    path('cms/access/',cms_views.access_res,name='access_res'),
    path('cms/delete/',cms_views.delete_res,name='delete_res'),
    path('cms/resources/',cms_views.res_list,name='res_list'),
    path('cms/edit/',cms_views.edit_res,name='edit_res'),
    path('cms/remove/',cms_views.remove_res,name='remove_res'),
    path('cms/trade/',cms_views.trade_manage,name='trade'),
    path('cms/trade_access/',cms_views.trade_access,name='trade_access'),
    path('cms/trade_cancel/',cms_views.trade_cancel,name='trade_cancel'),
    path('cms/banner/',cms_views.banner,name='banner'),
    path('cms/upload_banner/',cms_views.upload_banner,name='upload_banner'),
    path('cms/edit_banner/',cms_views.edit_banner,name='edit_banner'),
    path('cms/delete_banner/',cms_views.delete_banner,name='delete_banner'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

