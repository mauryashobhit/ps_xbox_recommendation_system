from django.http import HttpResponse
from django.shortcuts import  render, redirect
import requests
import bs4
from bs4 import BeautifulSoup
from lxml import etree
import requests
import urllib
import pandas as pd
import urllib.request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import  Login
from django.contrib import messages
import wikipedia
from django.conf import settings
from isodate import parse_duration
# Create your views here.
def index(request):
    return render(request,'index.html')

def ps(request):
    return render(request,'PS.html')

def xbox(request):
    return render(request,'XBOX.html')

def ps_trailers(request):
    return render(request,'ps_trailers.html' )

def get_suggestions_ps():
    data = pd.read_csv('final_ps.csv')
    return list(data['Title'].str.capitalize())

def user_index(request):
    return render(request,'user_index.html')

def ps_recommend(request):
    return render(request,'ps_recommend.html')

def ps_suggestions(request):
    data=pd.read_csv("final_ps.csv")
    Director=""
    Publisher=""
    Genre=""
    list=""
    videos=[]
    if request.method == 'POST':
        Title= request.POST.get('Title')
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part' : 'snippet',
            'q' : request.POST['Title'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 6,
            'type' : 'video'
        }
        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])
        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')
        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 9
        }
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)
    Director=data.loc[data['Title'] == Title, 'Developer(s)'].iloc[0]
    Publisher=data.loc[data['Title'] == Title, 'Publisher(s)'].iloc[0]
    Genre=data.loc[data['Title'] == Title, 'Genre(s)'].iloc[0]
    list=wikipedia.summary(Title, sentences=20)
    df=data.loc[data['Genre(s)']==Genre]
    df1=data.loc[data['Publisher(s)']==Publisher]
    df=df["Title"].tolist()
    df1=df1["Title"].tolist()
    df.remove(Title)
    df1.remove(Title)
    return render(request,"ps_recommend.html",context={'df':df,'videos' : videos,"Director":Director,"Publisher":Publisher,"Title":Title,"Genre":Genre,"list":list})


def xbox_recommend(request):
    return render(request,'xbox_recommend.html')

def xbox_suggestions(request):
    data=pd.read_csv("final_xbox.csv")
    Director=""
    Publisher=""
    Genre=""
    list=""
    videos=[]
    if request.method == 'POST':
        Title= request.POST.get('Title')
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part' : 'snippet',
            'q' : request.POST['Title'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 9,
            'type' : 'video'
        }
        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])
        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')
        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 9
        }
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)
    Director=data.loc[data['Title'] == Title, 'Developer(s)'].iloc[0]
    Publisher=data.loc[data['Title'] == Title, 'Publisher(s)'].iloc[0]
    Genre=data.loc[data['Title'] == Title, 'Genre(s)'].iloc[0]
    list=wikipedia.summary(Title, sentences=20)
    df=data.loc[data['Genre(s)']==Genre]
    df=df["Title"].tolist()
    df.remove(Title)
    return render(request,"xbox_recommend.html",context={'df':df,'videos' : videos,"Director":Director,"Publisher":Publisher,"Title":Title,"Genre":Genre,"list":list})

#---------------------------------------------------------------------------------------------------------------------------------------------------

def ps_news(request):
    list=[]
    list1=[]
    results=requests.get("https://www.pocket-lint.com/games/news/playstation")
    soup=bs4.BeautifulSoup(results.text,"lxml")
    details = soup.findAll('div',attrs={"class":"article"})
    title=soup.findAll('span',attrs={"class":"article-info-title"})
    for x in title:
        list.append(x.find('span').text)
    for i in details:
        list1.append(i.find('p').text)
    return render(request,"ps_news.html",context={"list":list,"list1":list1})

def xbox_news(request):
    list=[]
    list1=[]
    results=requests.get("https://www.pocket-lint.com/games/news/xbox")
    soup=bs4.BeautifulSoup(results.text,"lxml")
    details = soup.findAll('div',attrs={"class":"article"})
    title=soup.findAll('span',attrs={"class":"article-info-title"})
    for x in title:
        list.append(x.find('span').text)
    for i in details:
        list1.append(i.find('p').text)
    return render(request,"xbox_news.html",context={"list":list,"list1":list1})

def xbox_trailers(request):
    return render(request,"xbox_trailers.html")


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('login')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')


		context = {'form':form}
		return render(request, 'register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('user_index')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('user_index')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('index')
