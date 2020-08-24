from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Task
from datetime import datetime
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            l = []
            p = request.POST.getlist("complete")
            c = 0
            i = 0
            while i < len(p):
                if not i == len(p)-1:
                    if p[i]=='false' and p[i+1] == 'true':
                        c += 1
                        print("True")
                        l.append(True)
                        i+=2
                    else:
                        print("False")
                        l.append(False)
                        i+=1
                else:
                   print("False") 
                   l.append(False)
                   i+=1
            lt = Task.objects.all()
            i = 0
            for task in lt:
                if request.user in task.completed.all() and not l[i]:
                    idd = request.user.id
                    task.completed.remove(idd)
                    task.save()
                    print(f"{task} deleted")
                    i += 1
                elif (request.user not in task.completed.all()) and l[i]:
                    task.completed.add(request.user)
                    task.save()
                    print(f"{task} added")
                    i += 1
                else:
                    i+=1
                    
            return render(request, "todoapp/mylist.html",{
            "tasks" : Task.objects.all()
            })
            # return HttpResponse(f"Responses : {l}")
        else:
            return render(request, "todoapp/mylist.html",{
            "tasks" : Task.objects.all()
            })
    else :
        return render(request, "todoapp/index.html", {
            "tasks" : Task.objects.all()
        })
def add(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login",))

    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["desc"]
        due  = request.POST["due"]
        urgency = request.POST["urgency"]
        obj = Task()
        obj.title = title
        obj.desc = desc
        obj.due = due
        obj.urgency = urgency
        obj.save()
        return HttpResponseRedirect(reverse("index",))
    return render(request, "todoapp/add.html")

def edit(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login",))

    if request.method =="POST":
        obj = Task.objects.get(pk=request.POST["id"])
        title = request.POST["title"]
        desc = request.POST["desc"]
        due  = request.POST["due"]
        urgency = request.POST["urgency"]
        # delt = request.POST["delt"]
        if "delt" in request.POST:
            obj.delete()
            return HttpResponseRedirect(reverse("index",))
        obj.title = title
        obj.desc = desc
        obj.due = due
        now = datetime.now()
        today = str(now)[:10]
        # year, month, day = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d") 
        # print(f"{due} {today}")
        if(due < today):
            print("Invalid")
            return HttpResponse("<h1>Invalid Due Date</h1>")
        obj.urgency = urgency
        obj.save()
        return HttpResponseRedirect(reverse("index",))

    return render(request, "todoapp/edit.html", {
        "id" : id,
        "task" : Task.objects.get(pk = id)
    })

def login_view(request):
    if request.method=="POST":
        uname = request.POST["username"]
        passw = request.POST["password"]
        user = authenticate(request, username=uname, password=passw)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index",))
        return render(request, "todoapp/login.html", {
            "mesg" : "Not authenticated!"
        })
    return render(request, "todoapp/login.html",)

def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index",))
    else:
        logout(request)
        return HttpResponseRedirect(reverse("index"),)
