from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomEmailConfirmView
from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import PasswordResetView
from accounts.serializers import CustomPasswordResetSerializer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/auth/password/reset/', PasswordResetView.as_view(serializer_class=CustomPasswordResetSerializer), name='password_reset'),
    path('api/auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='custom_password_reset_confirm'),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/account-confirm-email/<str:key>/', CustomEmailConfirmView.as_view(), name='account_confirm_email'), # Always add it before "dj_rest_auth.registration.urls"
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/account/', include('accounts.urls')),
    path('api/doctor/', include('doctors.urls')),
    path('api/filter/', include('filterings.urls')),
    path('api/contact/', include('contacts.urls')),
]


urlpatterns+=static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
