from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.db.models.query_utils import Q
from .forms import SignUpForm, CustomUserChangeForm, MessageForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm  # Create a login form in forms.py
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, FriendRequest, Notification, Message
from post.models import Post
from django.contrib.auth import get_user_model
# Create your views here.

class SignUpView(TemplateView):
    template_name = 'account/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_data'] = 'This is custom data!'

        return context

    def get(self, request, *args, **kwargs):
        # Handle GET requests here
        user = request

        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        # Handle POST requests here
        # You can access form data using request.POST

        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')

        else:
            return self.get(request)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email)
            print(password)
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                # Redirect to a success page or home page after successful login
                print('Login success')
                return redirect('post:home')
            else:
                messages.error(request, 'Invalid email or password.')

    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    # Logout the user
    logout(request)
    # Redirect to a specific page after logout
    return redirect(reverse('account:login'))


def send_friend_request(request, to_username):
    from_user = request.user
    to_user = get_object_or_404(CustomUser, email=to_username)

    # Check if a friend request already exists
    existing_request = FriendRequest.objects.filter(from_user=from_user, to_user=to_user).first()
    if existing_request:
        print('Request already sent')
        # Handle case where a request already exists (e.g., redirect to a profile page)
        return JsonResponse({'request': 'already sent'})

    # Create a new friend request
    friend_request = FriendRequest(from_user=from_user, to_user=to_user)
    friend_request.save()
    print('Request added')
    # Redirect to a page indicating that the friend request has been sent
    return redirect('post:home')


def friend_request_list(request):
    current_user = request.user
    received_requests = FriendRequest.objects.filter(to_user=current_user, is_accepted=False)
    sent_requests = FriendRequest.objects.filter(from_user=current_user, is_accepted=False)

    return render(request, 'friend_request_list.html',
                  {'received_requests': received_requests, 'sent_requests': sent_requests})


def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user, is_accepted=False)

    # Accept the friend request
    friend_request.is_accepted = True
    friend_request.save()

    # Add each user to the other's friends list
    # friend_request.from_user.friends.add(request.user)
    request.user.friends.add(friend_request.from_user)

    # mark notification as seen
    Notification.objects.filter(user=request.user).update(is_viewed=True)

    return JsonResponse({"status": "request accepted"})


def profile(request, user_id):
    # User = get_user_model()
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'account/profile.html', {'user': user, 'form': form})

def notifications(request):
    post_likes = Notification.objects.filter(user=request.user, notification_type='post_like', is_viewed=False)
    frnd_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False)
    context = {
        'post_likes': post_likes,
        'frnd_requests' : frnd_requests
    }
    # unread_notifications.update(is_viewed=True)
    return render(request, 'account/notification.html', context)

def mark_asread(request):
    Notification.objects.filter(user=request.user).update(is_viewed=True)

    return JsonResponse({"status": "success"})


def show_profile(request, user_id):
    print('ise', user_id)
    user = get_object_or_404(CustomUser, id=user_id)
    image_data = Post.objects.filter(user=user).exclude(image='')


    context = {
        "pictures": image_data
    }
    return render(request, 'account/show_profile.html', context)


@login_required
def get_friends(request):
    user_profile = get_object_or_404(CustomUser, id=request.user.id)
    friends = user_profile.friends.all()

    context = {
        "friends" : friends
    }
    return render(request, "account/friends.html", context)


def send_message(request, friend_id):
    friend = get_user_model().objects.get(pk=friend_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = friend
            message.save()
            return redirect('account:chat', friend_id=friend.id)
    else:
        form = MessageForm()

    return redirect('account:chat', friend_id=friend.id)

def conversation_history(request, friend_id):
    friend = get_user_model().objects.get(pk=friend_id)
    from django.contrib.auth import models
    messages = Message.objects.filter(
        (models.Q(sender=request.user, receiver=friend) | models.Q(sender=friend, receiver=request.user))
    ).order_by('timestamp')

    context = {
        'friend': friend,
        'messages': messages,
    }
    return render(request, 'conversation_history.html', context)

def chat(request, friend_id=None):
    user_profile = get_object_or_404(CustomUser, id=request.user.id)

    # acive chat
    if not friend_id:
        try:
            friends = user_profile.friends.all().order_by('id')
        except:
            friends = []
        active_friend, messages, friend_profile = [], [], []

    else:
        active_friend = friend_id
        friend_profile = get_object_or_404(CustomUser, id=friend_id)
        try:
            messages = Message.objects.filter(
                (Q(sender=request.user, receiver=active_friend) | Q(sender=active_friend, receiver=request.user))
            ).order_by('-timestamp')[:6]
        except:
            messages = {}
        friends = user_profile.friends.all().order_by('id')

    # send msg
    form = MessageForm()
    context = {
        'active_friend': friend_profile,
        'friends': friends,
        'form': form,
        'messages':messages
    }

    return render(request, "account/chat.html", context)
