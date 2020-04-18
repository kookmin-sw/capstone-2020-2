from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = {
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('user/<int:id>/analyze/start/', views.getAnalyzingVideo.as_view(), name='analyze'),
    path('user/<int:id>/trial/<str:emotionTag>/', views.getTrialVideo.as_view(), name='trial'),
}

urlpatterns = format_suffix_patterns(urlpatterns)