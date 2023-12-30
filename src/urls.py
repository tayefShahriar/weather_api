from django.contrib import admin
from django.urls import path, include
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('code-explain/', app_views.CodeExplainView.as_view(), name='code-explain' ),
    path('users/', app_views.UserView.as_view(), name='users'),
    path('tokens/', app_views.TokenView.as_view(), name='tokens'),

]
