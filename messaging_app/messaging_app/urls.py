"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect

def root_redirect(request):
    """Redirect root URL to API endpoints"""
    return redirect('api/')

def api_root(request):
    """Simple API root view"""
    content = """
    <h1>Messaging App API</h1>
    <p>Welcome to the Messaging App API. Available endpoints:</p>
    <ul>
        <li><a href="/api/conversations/">Conversations</a></li>
        <li><a href="/api/messages/">Messages</a></li>
        <li><a href="/admin/">Admin Interface</a></li>
    </ul>
    <p>Use API clients like Postman or curl to interact with the endpoints.</p>
    """
    return HttpResponse(content)

urlpatterns = [
    path('', api_root, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
]