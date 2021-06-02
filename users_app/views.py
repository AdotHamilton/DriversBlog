from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
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
    context = {
        "logged_user" : logged_user,
        "posts": Post.objects.filter(creator=logged_user)
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
        "user": user,
        
    }
    return render(request, 'profile.html', context)

def updateProfile(request):
    if request.method == "POST":
        errors = User.objects.update_validator(request.POST)
        user = User.objects.get(id=request.POST['user_id'])
        if len(request.FILES) != 0:
            user.pfp = request.FILES["file"]
            
        user.user_name = request.POST["user_name"]
        if len(request.POST["password"]) != 0: 
            if errors:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/profile')
            else:
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                user.password = pw_hash
                user.save()
        else:
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

def postToThread(request, id):
    if request.method == "POST":
        errors = Post.objects.post_validator(request.POST)


def deletePost(request, id):
    deletePost = Post.objects.get(id=id)
    if deletePost.creator.id == request.session["user_id"]:
        deletePost.delete()
        return redirect("/dashboard")
    return redirect("/dashboard")
    

def editPost(request):
    if request.method == "post":
        return redirect("/dashboard")
    return redirect("/dashboard")

def likePost(request):
    user = User.objects.get(id=request.session['user_id'])
    liked_post = Post.objects.get(id=request.POST["post_id"])
    liked_post.likes.add(user)
    next = request.POST["next"]
    return redirect(next)

def followUser(request, id):
    user = User.objects.get(request.session["user_id"])
    userFollowed = User.objects.filter(id=id)
    if userFollowed:
        if user not in userFollowed.following.all():
            UserFollowing.objects.create(user_id=user, UserFollowing=userFollowed)
            return redirect(request, "users/"+ str(id))
        else: 
            messages.error(request, "Already following this user!")
            return redirect(request, "users/"+ str(id))
    else:
        return redirect(request, "users/"+ str(id))

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

def meets(request):

    return render(request, "meets.html")

def discussionsHome(request):
    context = {
        "vehicles": Vehicle.objects.all,
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'discussion_home.html', context)
def discussionPage(request, id):
    context = {
        "user": User.objects.get(id=request.session["user_id"])
    }
    return render(request, "discussion_page.html", context)