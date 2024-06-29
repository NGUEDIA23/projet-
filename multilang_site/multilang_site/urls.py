# Inclure les URLs de votre application principale
    # Ajoutez d'autres URLs internationalisées si nécessaire
from django.contrib import admin
from django.urls import path, include
from main.views import home 
from django.conf.urls.i18n import i18n_patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('main.urls')),
    path('', home, name='home'), 
]
urlpatterns += i18n_patterns(
    path('articles/', include('main.urls')), 
)