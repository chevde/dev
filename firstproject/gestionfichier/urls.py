from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import profile
from .views import CustomLoginView
from .views import CustomLogoutView
from .views import search
from .views import signup
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('profile/', profile, name='profile'),
    path('upload_photo', views.upload_photo, name='upload_photo'),
    path('photo_list/', views.photo_list, name='photo_list'),
    path('delete_all_photos/', views.delete_all_photos, name='delete_all_photos'),
    path('delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('delete_annonce/<int:annonce_id>/', views.delete_annonce, name='delete_annonce'),
    path('accounts/profile/', profile, name='profile'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView, name='logout'),
    path('signup/', signup, name='signup'),
    path('search/', search, name='search'),
    path('api/annonces/', views.list_announces, name='list_announces'),
    path('api/annonces/create/', views.create_annonce, name='create_annonce'),
    path('api/annonces/delete/<int:annonce_id>/', views.delete_annonce, name='delete_annonce'),
    path('api/annonces/search_annonce/', views.search_annonce, name='search_annonce'),
    path('api/annonces/update/<int:pk>/', views.update_annonce, name='update_annonce'),
]
# Configuration pour servir les fichiers médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    