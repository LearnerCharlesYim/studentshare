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
from front import views


urlpatterns = [
    path('', views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('upload/',views.upload,name='upload'),
    path('repwd/',views.repwd,name='repwd'),
    path('addres/',views.addres,name='addres'),
    path('resource/',views.resource_index,name='resource'),
    path('upload_res/',views.upload_res,name='upload_res'),
    path('del_res/',views.del_res,name='del_res'),
    path('edit_res/',views.editres,name='edit_res'),
    path('resource/detail/<id>/',views.res_detail,name='res_detail'),
    path('trading/',views.trading,name='trading'),
    path('access/',views.access_trade,name='access_trade')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

