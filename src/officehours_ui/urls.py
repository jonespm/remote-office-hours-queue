from django.urls import path

from .views import SpaView, AuthPromptView, auth_callback_view


urlpatterns = [
    path('', SpaView.as_view(), name='home'),
    path('queue/', SpaView.as_view()),
    path('queue/<str:queue_id>/', SpaView.as_view()),
    path('manage/', SpaView.as_view(), name='manage'),
    path('manage/<str:queue_id>/', SpaView.as_view()),
    path('search/<str:term>/', SpaView.as_view()),
    path('preferences/', SpaView.as_view(), name='preferences'),
    path('auth/<backend_name>/', AuthPromptView.as_view(), name='auth_prompt'),
    path('callback/<backend_name>/', auth_callback_view, name='auth_callback'),
]
