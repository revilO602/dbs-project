"""DBSProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from DBSApp import views, v2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/health/', views.uptime),
    path('v1/ov/submissions/<int:id>', views.submissions_delete),
    path('v1/ov/submissions/<int:id>/', views.submissions_delete),
    path('v1/ov/submissions', views.submissions_parse_method),
    path('v1/ov/submissions/', views.submissions_parse_method),
    path('v1/ov/companies/', views.companies_request),

    path('v2/ov/submissions/', v2.parse_method),
    path('v2/ov/submissions', v2.parse_method),
    path('v2/ov/submissions/<int:id>/', v2.parse_method_id),
    path('v2/ov/submissions/<int:id>', v2.parse_method_id),
    path('v2/ov/companies/', v2.companies_request),

]
