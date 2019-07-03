"""IPS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from vote import views as voteviews
from administration import views as adminviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', voteviews.index),
    path('vote/<int:poll_id>/', voteviews.vote),
    path('login/', voteviews.login),
    path('logout/', voteviews.logout),
    path('cast/<int:poll_id>/<int:candidate_id>/', voteviews.cast),

    path('manage/', adminviews.index),
    path('manage/polls', adminviews.polls),
    path('manage/voters', adminviews.voters),

    path('manage/voters/add', adminviews.addvoter),
    path('manage/voters/delete/<str:voter_id>', adminviews.deletevoter),

    path('manage/polls/add', adminviews.addpoll),
    path('manage/ajaxhandlers/getcandidatename', adminviews.getcandidatename),
    path('manage/polls/delete/<int:poll_id>', adminviews.deletepoll),
    path('manage/ajaxhandlers/changepollstatus/<int:poll_id>', adminviews.changepollstatus),
    path('manage/polls/analysis/<int:poll_id>', adminviews.pollanalysis),

    path('manage/generateids', adminviews.generateids),
    path('manage/voters/import', adminviews.importvoters), 

]
