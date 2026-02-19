from lib2to3.fixes.fix_input import context
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy,reverse
from django.views.generic import TemplateView,ListView, DetailView, CreateView, UpdateView,DeleteView
from blog.models import Post,  Comments
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages#
# Create your views here.



#authenticate(): Checks the provided username and password against the database. If they match an existing user, it returns a User object; if not, it returns None.
#login(): Logs the authenticated user into the session. It associates the user with the current session, meaning the user is considered "logged in" on the website.

def login_as_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog:about')  # Change 'home' to the actual URL name where you want to redirect users
        else:
            messages.error(request, 'Something is wrong with your Username or Password')

    return render(request, 'Blog/accounts/login.html')

def logout_as_view(request):
    logout(request)
    return redirect('blog:about')

class BlogHomeView(TemplateView):
    template_name = 'Blog/blog_homepage.html'

class PostListView(ListView):
    #This view shows the list of posts
    model = Post
    #use context_object_name to change the name of the class in templates


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for post in context['post_list']:
            post.comment_count = post.comments.count()

        return context

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')# Object relational mapping
        #This means:
        #This is like a SQL query but in Python.
        #It takes the Post model and then all the objects there anbd filter out based on the conditions provided
        #published_date__lte means filter on when the published date is less than or equal to(lte) the time/date now and to order by published date
        #The order by takes arguements in the form modelfield__lookuptype  (The double underscore is important)


class PostDetailView(DetailView):

    #This view would show one post from the list of posts in detail.
    model=Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #context['images'] = PostFile.objects.filter(post=self.object)

        return context


def PostCreateFuncView(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'post_form':form})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    #Necessary Attributes
    login_url = 'login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm

    login_url = 'login/'    
    
    template_name = 'blog/post_edit.html'
    redirect_field_name = 'blog/post_detail.html'

    
        #fields = ('title', 'text')

class DraftListView(LoginRequiredMixin, ListView):


    model = Post


    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-create_date')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    # Reverse lazy so that only when the delete is successful, will the website take you back to the lis of posts
    success_url = reverse_lazy('blog:post_list')






@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail',pk=pk)

#@login_required# Makes this view required the user lgoin
def add_comment(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':# Means someone has filled in the form and pressed enter
        form = CommentForm(request.POST)# The current form is now the comment form
        if form.is_valid():# The form being valid requires that thy filled in all the required parameters
            comment = form.save(commit=False)
            comment.post = post# assigning the post foreign key, this cooment will now be assigned to the post

            comment.save()
            return  redirect('blog:post_detail',pk=post.pk)
        else:
            print(form.errors)
    else:
        form = CommentForm()#get a blank form
    return render(request, 'blog/comment_form.html', {'form':form })



@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.approve()
    return redirect('blog:post_list')#,pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comments,pk=pk)
    post_pk = comment.post.pk# This needs to be saved so that it will be retained when the comment is deleted
    comment.delete()
    return redirect('blog:post_list')#,pk=post_pk)