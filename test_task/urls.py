from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
                  path("reports/", include("orders.urls"))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
