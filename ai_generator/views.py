from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json, os
""" from pytube import YouTube """
from django.conf import settings
import assemblyai as aai
import openai
from pytubefix import YouTube
from .models import NotePost
""" import yt_dlp """
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from decouple import config

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def generate_blog(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            yt_link = data['link']
            """ return JsonResponse({'content': yt_link}) """
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error':'Invalid data sent'}, status=400)
        
        #get title
        print(yt_link)
        title = yt_title(yt_link)

        #get transcript
        transcription = get_transcribtion(yt_link)
        if not transcription:
            return JsonResponse({'error':"Failed to get transcript"},status=500)
        
        #use openAI to generate blog
        blog_content = generate_from_transcript(transcription)
        if not blog_content:
            return JsonResponse({'error':"Failed to generate notes"},status=500)
        
        #save to database
        new_Note_articale = NotePost.objects.create(
            user = request.user,
            youtube_title = title,
            youtube_link = yt_link,
            generated_content = blog_content,
            
        )
        new_Note_articale.save()


        #return artical as responce
        return JsonResponse({'content':blog_content})
    
    else:
        return JsonResponse({'error':'Invalid request method'}, status=405)



# Youtube was blocking due to bot detection
def yt_title(link):
    yt = YouTube(link, client='WEB')
    title = yt.title
    return title
    



def get_Audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file,new_file)
    return new_file









def get_transcribtion(link):
    audio_file = get_Audio(link)
    aai.settings.api_key = config('assemblyAi_Key') # assemblyAi api key
    transcriber = aai.Transcriber()
    tramscript = transcriber.transcribe(audio_file)

    return tramscript.text
    
def generate_from_transcript(transcription):
    openai.api_key = config('openAi_Key') # openAI api key

    prompt = f"Based on the following transcript from a YouTube video, make notes that summarize all main topics of the video, fromat it in a way the notes can be used to learn from, at the end of your notes mention the main takaways from the notes, write it based on the transcript:\n\n{transcription}\n\nArticle:"

    responce = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )

    generated_content = responce.choices[0].message.content.strip()

    return generated_content

def note_list(request):
    Note_articals = NotePost.objects.filter(user=request.user)
    return render(request, "all-Notes.html", {'Note_articals':Note_articals})


@require_POST
def delete_note(request, pk):
    note = get_object_or_404(NotePost, pk=pk)
    note.delete()
    return redirect("/note-list")






def edit_note(request, pk):
    note = get_object_or_404(NotePost, pk=pk)
    if request.method == "POST":
        note.generated_content = request.POST.get("generated_content", note.generated_content)
        note.save()
        return redirect('note-details', pk=note.id)  # Use your detail view's URL name
    return render(request, "Note-details.html", {"note_artical_detail": note})



def note_details(request, pk):
    note_artical_detail = NotePost.objects.get(id=pk)
    if request.user == note_artical_detail.user:
        return render(request,"note-details.html", {"note_artical_detail":note_artical_detail})
    else:
        return redirect("/")

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username , password = password)
        if user is not None:
            login(request,user)
            return  redirect('/')
        else:
            error_message = "Invalid username ort password"
            return render(request, 'login.html', {'error_message':error_message})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username =  request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatpassword']

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username,email,password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request,'signup.html' ,{'error_message':error_message})
            
        else:
            error_message = 'Passwords do not match'
            return render(request,'signup.html' ,{'error_message':error_message})

    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')
