from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
from datetime import date
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    this_user = User.objects.create(user_name= request.POST['user_name'], email=request.POST['email'], password=pw_hash)
    request.session['user_id'] = this_user.id
    return redirect('/dashboard')


def dashboard(request):
    if "user_id" not in request.session:
        return redirect('/')
    logged_user = User.objects.get(id=request.session['user_id'])
    followersList = [logged_user.id]
    for followed in logged_user.followers.all():
        followersList.append(followed.user_id_id)
    context = {
        "logged_user" : logged_user,
        "followingPosts": Post.objects.filter(creator__in=followersList).order_by("-created_at")
    }
    return render(request, 'success.html', context)

def logout(request):
    del request.session['user_id']
    return redirect('/')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/dashboard')
        else:
            messages.error(request, "Username or password incorrect")
    
    return redirect('/')

def displayMyProfile(request):
    user = User.objects.get(id=request.session["user_id"])
    context = {
        "logged_user": user,
        
    }
    return render(request, 'profile.html', context)

def updateProfile(request):
    if request.method == "POST":
        errors = User.objects.update_validator(request.POST)
        user = User.objects.get(id=request.POST['user_id'])
        if len(request.FILES) != 0:
            user.pfp = request.FILES["file"]
        
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/profile')
        else:
            user.user_name = request.POST["user_name"] 
            if len(request.POST["password"]) != 0:
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                user.password = pw_hash
                user.save()
        
        return redirect('/profile')
    else:
        return redirect('/profile')

def makePost(request):
    if request.method == "POST":
        errors = Post.objects.post_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/dashboard")
        author = User.objects.get(id=request.POST["uid"])
        if(len(request.FILES) != 0):
            post = Post.objects.create(
                header=request.POST["header"],
                img=request.FILES["img"], content=request.POST["content"], 
                creator=author)
        else:
            post = Post.objects.create(header=request.POST["header"],
                content=request.POST["content"], 
                creator=author)
        return redirect('/dashboard')


def createThread(request):
    if request.method == "POST":
        errors = Thread.objects.thread_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/discussions")
        else:
            new_thread = Thread.objects.create(title=request.POST["title"], content=request.POST["content"], 
                    creator=User.objects.get(id=request.session["user_id"]))
            if request.POST["year"] and request.POST["make"] and request.POST["model"]:
                new_thread.year = request.POST["year"]
                new_thread.make = request.POST["make"]
                new_thread.model = request.POST["model"]
                new_thread.save()
        return redirect("/discussions")

def displayThreadForm(request):
    return render(request, "new_thread_form.html")    

def postToThread(request):
    if request.method == "POST":
        errors = Post.objects.post_validator(request.POST)
        if errors:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect(request.POST["next"])
        else:
            thread = Thread.objects.get(id=request.POST["thread_id"])
            post = Post.objects.create(header=request.POST["header"], content=request.POST['content'],
             thread=thread, creator=User.objects.get(id=request.session["user_id"]))
            if(len(request.FILES) != 0):
                post.img = request.FILES["img"]
                post.save()
            return redirect(request.POST["next"])
    else:
        return redirect(request.POST["next"])

def deletePost(request, id):
    deletePost = Post.objects.get(id=id)
    if deletePost.creator.id == request.session["user_id"]:
        deletePost.delete()
        return redirect(request.POST["path"])
    return redirect(request.POST["path"])
    
def displayEditPostForm(request, id):
    post = Post.objects.get(id=id)
    context = {
        "post": post,
        "logged_user": User.objects.get(id=request.session["user_id"])
    }
    return render(request, "edit_post_form.html", context)
def editPost(request):
    if request.method == "POST":
        errors = Post.objects.post_validator(request.POST)
        post = Post.objects.get(id=request.POST["post_id"])
        if errors: 
            for key,value in errors.items():
                messages.error(request, value)
            return redirect("/dashboard")
        else:
            post.header = request.POST["header"]
            post.content = request.POST["content"]
            if(len(request.FILES) != 0):
                post.img = request.FILES["img"]
            post.save()
        return redirect("/dashboard")
    return redirect("/dashboard")

def likePost(request):
    user = User.objects.get(id=request.session['user_id'])
    liked_post = Post.objects.get(id=request.POST["post_id"])
    liked_post.likes.add(user)
    next = request.POST["next"]
    return redirect(next)

def followUser(request, id):
    user = User.objects.get(id=request.session["user_id"])
    userFollowed = User.objects.filter(id=id)
    if userFollowed:
            UserFollowing.objects.create(user_id=userFollowed[0], following_user_id=user)
            return redirect("/users/"+ str(id))
    else:
        return redirect("/users/"+ str(id))

def displayUser(request, id):
    user_viewed = User.objects.filter(id=id)
    if user_viewed:
        context = {
            "logged_user": User.objects.get(id=request.session["user_id"]),
            "user": user_viewed[0]
        }
        return render(request, "userPage.html", context)
    else:
        return redirect("/dashboard")


def discussionsHome(request):
    context = {
        "threads": Thread.objects.all(),
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'discussion_home.html', context)

def discussionPage(request, id):
    if Thread.objects.filter(id=id):
        context = {
            "logged_user": User.objects.get(id=request.session["user_id"]),
            "thread": Thread.objects.filter(id=id)[0]
        }
        return render(request, "discussion_page.html", context)
    else:
        return redirect("/discussions")
def deleteThread(request, id):
    if Thread.objects.filter(id=id):
        thread = Thread.objects.filter(id=id)[0]
        if thread.creator.id == request.session["user_id"]:
            thread.delete()
            return redirect("/discussions")
        else:
            return redirect("/discussions")
    else:
        return redirect("/discussions")

def displayUpdateThreadForm(request, id):
    context = {
        "thread": Thread.objects.get(id=id),
        "user": User.objects.get(id=request.session["user_id"])
    }
    return render(request, "update_thread_form.html", context)

def updateThread(request, id):
    if request.method == "POST":
        edit_thread = Thread.objects.get(id=id)
        if edit_thread.creator.id == request.session["user_id"]:
            errors = Thread.objects.thread_validator(request.POST)
            if errors:
                for key,value in errors.items():
                    messages.error(request, value)
                return redirect("/discussions/" + str(id) + "/editForm")
            else:
                edit_thread.title = request.POST["title"]
                if request.POST['year']:
                    edit_thread.year = request.POST["year"]
                if request.POST['make']:
                    edit_thread.make = request.POST["make"]
                if request.POST['model']:
                    edit_thread.model = request.POST["model"]
                edit_thread.save()
                return redirect("/discussions/" + str(id))
        else: 
            return redirect("/discussions/" + str(id))
    else:
        return redirect("/discussions/" + str(id))
                
def meets(request):
    context = {
        "key": "API_KEY",
        "meets": Meet.objects.all(),
        "logged_user": User.objects.get(id=request.session["user_id"])
    }
    return render(request, "meets.html", context)

def newMeetForm(request):
    user = User.objects.get(id= request.session["user_id"])
    context = {
        "logged_user":  user
    }
    return render(request, "new_meet_form.html", context)

def createMeet(request):
    if request.method == "POST":
        errors = Meet.objects.meet_validator(request.POST)
        if errors:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect("/meets/new")
        else:
            address = request.POST["address"]
            address = address.replace(" ", "+")
            user = User.objects.get(id=request.session["user_id"])
            Meet.objects.create(title=request.POST["title"], address=address, 
                        description=request.POST["description"], state=request.POST["state"], creator=user,
                        date=request.POST["date"], time=request.POST["time"])
            return redirect("/meets")
    return redirect("/meets")

def deleteMeet(request, id):
    if Meet.objects.filter(id=id):
        deleted_meet = Meet.objects.get(id=id)
        if deleted_meet.creator.id == request.session["user_id"]:
            deleted_meet.delete()
        return redirect("/meets")
    else:
        return redirect("/meets")

def displayMeet(request, id):
    if Meet.objects.filter(id=id):
        meet = Meet.objects.filter(id=id)[0]
        context = {
            "meet": meet,
            "key": "AIzaSyCoz8Z6Uw7t32gmCymP4lbtR2KpRKWqS68",
            "logged_user": User.objects.get(id=request.session["user_id"])
        }
        return render(request, "meet_page.html", context)
    else: 
        return redirect("/meets")

def meetsByState(request):
    meets = Meet.objects.filter(state=request.POST["state"])

    context = {
        "meets": meets,
        "logged_user": User.objects.get(id=request.session["user_id"])
    }
    return render(request, "meets.html", context)

def attendMeet(request, id):
    if Meet.objects.filter(id=id):
        meet = Meet.objects.get(id=id)
        user = User.objects.get(id=request.session["user_id"])
        meet.attendees.add(user)
        return redirect(request.POST["path"])
    return redirect(request.POST["path"])
