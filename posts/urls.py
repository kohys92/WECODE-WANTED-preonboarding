from django.urls import path
from .views import PostView, PostlistView

urlpatterns = [
    path('/<int:post_id>', PostView.as_view()),
    path('/list', PostlistView.as_view())
]