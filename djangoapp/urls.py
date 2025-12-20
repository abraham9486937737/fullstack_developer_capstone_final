from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # path for registration
    # path('register', views.register, name='register'),

    # path for login
    # path('login', views.login_user, name='login'),

    # path for dealer reviews view
    # path('dealer/<int:dealer_id>/reviews', views.dealer_reviews, name='dealer_reviews'),

    # path for add a review view
    # path('dealer/<int:dealer_id>/add_review', views.add_review, name='add_review'),

    # path for get_cars view
    path('get_cars', views.get_cars, name='getcars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
