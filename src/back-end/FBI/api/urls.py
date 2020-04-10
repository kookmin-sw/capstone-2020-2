from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = {
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('capture/', views.captureImage, name="capture"),
    path('user/<int:id>/analyze/start/', views.getAnalyzingVideo.as_view(), name='analyze'),
}

urlpatterns = format_suffix_patterns(urlpatterns)