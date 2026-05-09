import time

from django.contrib import messages
from django.shortcuts import render, redirect

from apps.detection import FaceRecognition
from .forms import *

faceRecognition = FaceRecognition()


def home(request):
    return render(request, 'faceDetection/home.html')


def register(request):
    if request.method == "POST":
        form = ResgistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            print("IN HERE")
            messages.success(request, "SuccessFully registered!")
            addFace(user.face_id)
            time.sleep(2)
            return redirect('home')
        else:
            messages.error(request, "Account registered failed")
    else:
        form = ResgistrationForm()

    return render(request, 'faceDetection/register.html', {'form': form})


def addFace(face_id):
    face_id = face_id
    faceRecognition.faceDetect(face_id)
    faceRecognition.trainFace()
    return redirect('/')


def login(request):
    face_id = faceRecognition.recognizeFace()

    if face_id is None:
        messages.error(request, "Authentication failed!")
        return redirect('home')

    user = UserProfile.objects.filter(face_id=face_id).first()

    if not user:
        messages.error(request, "Authentication failed!")
        return redirect('home')

    messages.success(request, "You are welcome")
    return redirect('greeting', str(user.face_id))


def greeting(request, face_id):
    try:
        user = UserProfile.objects.get(face_id=face_id)
        return render(request, 'faceDetection/greeting.html', {'user': user})
    except UserProfile.DoesNotExist:
        return redirect('home')
