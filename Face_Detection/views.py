import time

from django.contrib import messages
from django.shortcuts import render, redirect

from Face_Detection.detection import FaceRecognition
from .forms import *

faceRecognition = FaceRecognition()


def home(request):
    return render(request, 'faceDetection/home.html')


def register(request):
    if request.method == "POST":
        form = ResgistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            print("IN HERE")
            messages.success(request, "SuccessFully registered!")
            addFace(request.POST['face_id'])
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
    print(face_id)
    user = UserProfile.objects.filter(face_id=face_id).exists()
    if not user:
        danger_message = 'Authentication failed!'
        messages.add_message(request, level=20, message=danger_message)
        return redirect('home')
    messages.add_message(request, level=20, message='You are welcome')
    return redirect('greeting', str(face_id))


def greeting(request, face_id):
    face_id = int(face_id)
    try:
        face_id = UserProfile.objects.get(face_id=face_id).pk
        context = {
            'user': UserProfile.objects.get(face_id=face_id)
        }
        return render(request, 'faceDetection/greeting.html', context=context)
    except:
        return render(request, 'faceDetection/home.html')
