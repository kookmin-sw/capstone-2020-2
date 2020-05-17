from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = {
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('user/<int:id>/analyze/<str:emotionTag>/', views.getAnalyzingVideo.as_view(), name='analyze'),
    path('user/<int:id>/analyze/real-time-result/', views.realTimeAnalyze, name='realTimeResult'),
}

#urlpatterns = format_suffix_patterns(urlpatterns)