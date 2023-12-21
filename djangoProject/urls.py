"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from Footballer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', views.show_info, name='info'),
    path('showfootballer/<int:id_user>/', views.show_footballer),
    path('showfootballer/<str:name_division>/<int:id_club>/<int:id_user>/addGame/', views.create_game, name='create_game'),
    path('showfootballer/<str:name_division>/<int:id_club>/<int:id_user>/<int:number_game>/deleteGame/', views.delete_game, name='delete_game'),
    path('', views.show_index, name='home'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('refereeView/<str:name_division>/', views.show_club_ofDivision, name='footballer_ofDivision'),
    path('refereeView/<str:name_division>/<int:id_club>/', views.show_footballerFromGroup, name='footballerFromGroup'),
    path('refereeView/<str:name_division>/<int:id_club>/<int:id_user>/', views.show_footballer, name='show_footballer'),
    path('index/sign', views.signup, name='sign'),
#ajax url
    path('ajax/validate_username', views.validate_username, name='validate_username'),
    path('ajax/check_numberGame/<str:name_division>/<int:id_footballer>', views.check_numberGame, name='check_numberGame'),

]
