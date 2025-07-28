from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user
        events = Events.objects.filter(customer = user)
    else:
        events = Events.objects.all()
   
    date_range = request.GET.get('date_range')
    location_filters = request.GET.getlist('location')  
    organizer_filters = request.GET.getlist('organizer')

    today = timezone.now().date()

    if date_range == 'past_30':
        events = events.filter(startdate__date__gte=today - timedelta(days=30))
    elif date_range == 'past_7':
        events = events.filter(startdate__date__gte=today - timedelta(days=7))
    elif date_range == 'today':
        events = events.filter(startdate__date=today)
    elif date_range == 'next_7':
        events = events.filter(startdate__date__lte=today + timedelta(days=7))
    elif date_range == 'next_30':
        events = events.filter(startdate__date__lte=today + timedelta(days=30))

    if location_filters:
        events = events.filter(location__in=location_filters)

    if organizer_filters:
        events = events.filter(organizer__in=organizer_filters)

    
    unique_locations = Events.objects.values_list('location', flat=True).distinct()
    unique_organizers = Events.objects.values_list('organizer', flat=True).distinct()

    return render(request, 'index.html', {
        'data': events,
        'unique_locations': unique_locations,
        'unique_organizers': unique_organizers,
        'selected_locations': location_filters,
        'selected_organizers': organizer_filters
    })

def loginpw(request):
    if request.user.is_authenticated:
         return redirect('/')
    else:
         if request.method == 'POST':
          email=request.POST.get('email')
          password=request.POST.get('password')
          user=authenticate(request,email=email,password=password)
          if user is not None:
               login(request,user)
               messages.success(request,'Login Successfully!')
               return redirect('/')
          else:
            messages.warning(request,'Invalid Username and Password!')
            return redirect('login')
    return render(request,'login.html')

def logout_page(request):
   if request.user.is_authenticated:
      logout(request)
      messages.success(request,'Logout Successfully!')
   return redirect('/')

def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('pass')
        if CustomUser.objects.filter(email = email):
            messages.warning(request,'User Already Exist!')
         # Hash the password before saving
        hashed_password = make_password(password)  # Hash the password using Django's built-in function

        user = CustomUser(email = email,password = hashed_password, first_name = fname, last_name = lname, phone = phone)
        user.save()
        messages.warning(request,'User Registered Successfully!')
        return redirect('login')
    return render(request,'register.html')

def addevent(request):
    if request.method == 'POST':
        title  = request.POST.get('title')
        desc = request.POST.get('desc')
        sdate  = request.POST.get('sdate')
        edate = request.POST.get('edate')
        location = request.POST.get('loc')
        organizer = request.POST.get('org')

        user = request.user
        event = Events(customer = user,title = title,description = desc,startdate = sdate,enddate = edate,location = location,organizer = organizer)
        event.save()
        messages.warning(request,'Event Added Successfully!')
        return redirect('/')
    return render(request,'addevent.html')

def loadevent(request,id):
    event = Events.objects.get(id=id)
    return render(request,'updateevent.html',{'data':event})

def eventupdate(request,id):
    event = get_object_or_404(Events, id=id)
    if request.method == 'POST':
        if 'title' in request.POST:
            event.title = request.POST['title']
        if 'desc' in request.POST:
            event.description = request.POST['desc']
        if 'sdate' in request.POST:
            event.startdate = request.POST['sdate']
        if 'edate' in request.POST:
            event.enddate = request.POST['edate']
        if 'loc' in request.POST:
            event.location = request.POST['loc']
        if 'org' in request.POST:
            event.organizer = request.POST['org']
        if 'status' in request.POST:
            event.status = request.POST['status']
        event.save()
        messages.success(request, 'Event Updated successfully')
        return redirect('/')
    return render(request,'updateevent.html')

def deleteevent(request,id):
    event = Events.objects.get(id=id)
    event.delete()
    messages.success(request, 'Event Deleted successfully')
    return redirect('/')

def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '').strip()

        if keyword:
            events = Events.objects.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword)
            )
    
        return render(request,'search.html',{'keyword':keyword,'events':events})