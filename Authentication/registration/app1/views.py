from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import IdealData, Exercise, Food
from django.shortcuts import render
import requests
from .models import UserProfile, Video
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from isodate import parse_duration
from django.shortcuts import render, redirect
import json
from .models import UserData, IdealData
from .forms import UserInputForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django .contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')


def Landing(request):
    return render(request, 'exercise_landingPage.html')


def BucketPage(request):
    return render(request, 'bucket.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('bucket')
        else:
            return HttpResponse("Username or password is incorrect!")

    return render(request, 'login.html')


def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return HttpResponse("Your password and confirm password do not match!")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists. Please choose a different one.")

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password1)
            user.save()
            # Redirect to login page upon successful signup
            return redirect('login')
        except Exception as e:
            return HttpResponse(f"Error creating user: {str(e)}")

    return render(request, 'signup.html')


def LogoutPage(request):
    logout(request)
    return redirect('exercise_landingPage')


def user_input(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            user_data = form.save()

            # Fetch ideal data based on age and gender in a single query
            try:
                ideal_data = IdealData.objects.get(
                    age=user_data.age, gender=user_data.gender)
            except IdealData.DoesNotExist:
                ideal_data = None

            # Prepare data for graph
            data_for_graph = [
                {"label": "User Input", "data": [
                    user_data.weight, user_data.height, user_data.sleeping_hours]}
            ]
            if ideal_data:
                data_for_graph.append({
                    "label": "Ideal Data",
                    "data": [ideal_data.weight, user_data.height, ideal_data.sleeping_hours]
                })

            # Get exercise recommendations based on user data
            exercises = Exercise.objects.filter(
                age=user_data.age, gender=user_data.gender)

            # Get food recommendations based on user data
            foods = Food.objects.filter(
                age=user_data.age, gender=user_data.gender)

            return render(request, 'user_input_graph.html', {
                'form': form,
                'data_for_graph': json.dumps(data_for_graph),
                'exercises': exercises,
                'foods': foods
            })

    else:
        form = UserInputForm()

    return render(request, 'user_input_form.html', {'form': form})


# youtube ######


def index(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': request.POST.get('search', ''),
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video'
        }

        # Use the requests library to send HTTP requests
        r = requests.get(search_url, params=search_params)

        results = r.json().get('items', [])

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST.get('submit') == 'lucky' and video_ids:
            return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')

        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 9
        }

        r = requests.get(video_url, params=video_params)

        results = r.json().get('items', [])

        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    context = {
        'videos': videos
    }

    if request.method == 'POST':
        if 'add-to-favorites' in request.POST:
            video_id = request.POST.get('video_id')
            add_to_favorites(request, video_id)
            return JsonResponse({'message': 'Video added to favorites.'})

        if 'remove-from-favorites' in request.POST:
            video_id = request.POST.get('video_id')
            remove_from_favorites(request, video_id)
            return JsonResponse({'message': 'Video removed from favorites.'})

    return render(request, 'index.html', context)


def add_to_favorites(request, video_id):
    video_url = f'https://www.googleapis.com/youtube/v3/videos'

    video_params = {
        'key': settings.YOUTUBE_DATA_API_KEY,
        'part': 'snippet,contentDetails',
        'id': video_id,
        'maxResults': 1
    }

    response = requests.get(video_url, params=video_params)

    try:
        response_data = json.loads(response.content)
        video_data = response_data.get('items', [])
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Error adding video to favorites. Invalid API response.'})

    if video_data:
        video_info = video_data[0]['snippet']
        title = video_info['title']
        thumbnail = video_info['thumbnails']['high']['url']
        duration = int(parse_duration(
            video_data[0]['contentDetails']['duration']).total_seconds() // 60)

        video = Video.objects.create(
            title=title,
            video_id=video_id,
            url=f'https://www.youtube.com/watch?v={video_id}',
            duration=duration,
            thumbnail=thumbnail
        )

        user_profile, created = UserProfile.objects.get_or_create(
            user=request.user)
        user_profile.favorites.add(video)
        user_profile.save()

        return JsonResponse({'message': 'Video added to favorites.'})

    return JsonResponse({'message': 'Error adding video to favorites. Video not found.'})


def remove_from_favorites(request, video_id):
    video = get_object_or_404(Video, video_id=video_id)
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.favorites.remove(video)
    user_profile.save()


def favorite_videos(request):
    user_profile = UserProfile.objects.get(user=request.user)
    favorites = user_profile.favorites.all()

    context = {
        'favorite_videos': favorites
    }

    return render(request, 'favorite_videos.html', context)


def remove_favorite(request):
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        remove_from_favorites(request, video_id)
        return JsonResponse({'message': 'Video removed from favorites.'})
