from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from account.models import CustomUser, FriendRequest
from post.models import Post
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from .form import PostForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
# Create your views here.

class LoginRequiredMixin:
    """
    Mixin to check if the user is logged in.
    Redirects to the login page if the user is not logged in.
    """
    login_url = 'account:login'  # Change to the actual URL name of your login view

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse(self.login_url))
        return super().dispatch(request, *args, **kwargs)

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'post/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # to get user logged in
        user = self.request.user
        obj = CustomUser.objects.get(email=user)
        context['obj'] = obj

        # to get feed
        friends = user.friends.all()
        feed_posts = Post.objects.filter(Q(user=user) | Q(user__in=friends)).order_by('-created_at')
        # to check received frnd req
        frnd_requests = FriendRequest.objects.filter(to_user=user, is_accepted=False)[:5]

        # add pagination
        paginator = Paginator(feed_posts, 4)
        page = self.request.GET.get('page')
        print('page', page)
        page_obj = paginator.get_page(page)

        context['frnd_requests'] = frnd_requests
        context['request_count'] = len(frnd_requests)
        context['page_obj'] = page_obj
        return context

    def get(self, request, *args, **kwargs):
        # Handle GET requests here


        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        # Handle POST requests here
        # You can access form data using request.POST
        custom_data_from_form = request.POST.get('custom_data_from_form')
        # Process the data as needed

        form = PostForm(request.POST, request.FILES)  # Assuming your form has an 'image' field
        if form.is_valid():
            # Save the post to the database
            post = form.save(commit=False)
            post.user = request.user  # Set the user field to the current user
            post.save()
            return redirect('post:home')
        else:
            return JsonResponse({'post': "Error in post submission"})


def search_view(request):
    search_query = request.POST.get('search_query', '')
    print(search_query)
    # Perform your search logic here using the search_query variable
    # For example, you might want to filter a queryset based on the search query
    if search_query:
        search_result = CustomUser.objects.filter(Q(last_name__icontains=search_query)|Q(first_name__icontains=search_query))
    else:
        search_result = {}
    context = {
        'search_result': search_result,
        'search_query': search_query,
    }
    # Render the template with the search results
    return render(request, 'post/search.html', context)


def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)

        # Perform logic to handle the like, e.g., update the likes field in the Post model
        post.likes.add(request.user)  # Assuming you have authentication and request.user is available
        post.save()

        # return JsonResponse({'message': 'Post liked successfully', 'likes': post.likes.count()})
        return redirect("post:home")
    return JsonResponse({'message': 'Invalid request'})