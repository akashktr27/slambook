from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
from account.models import CustomUser
from post.models import Post
from django.db.models import Q
# Create your views here.

class HomePageView(TemplateView):
    template_name = 'post/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        obj = CustomUser.objects.get(email=user)
        context['obj'] = obj
        feeds = Post.objects.all()
        context['feeds'] = feeds
        return context

    def get(self, request, *args, **kwargs):
        # Handle GET requests here
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        # Handle POST requests here
        # You can access form data using request.POST
        custom_data_from_form = request.POST.get('custom_data_from_form')
        # Process the data as needed
        return HttpResponse(f'POST request received with custom data: {custom_data_from_form}')


def search_view(request):
    search_query = request.POST.get('search_query', '')

    # Perform your search logic here using the search_query variable
    # For example, you might want to filter a queryset based on the search query
    search_result = CustomUser.objects.filter(Q(last_name__icontains=search_query)|Q(first_name__icontains=search_query))

    # Render the template with the search results
    return render(request, 'post/search.html', {'search_result': search_result})