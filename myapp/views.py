from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from .models import Todo

from .models import Blog, Author
from .forms import BlogForm
from django.contrib import messages
from django.views.generic.edit import UpdateView

# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    return render(request,'myapp/index.html',{'blogs':blogs})

def blog(request):
    return render(request,'myapp/blog.html',{'name':'Arjun'})

def add_blog(request):
    # if request.method == 'POST':
    #     new_blog = Blog.objects.create(
    #         title=request.data.title,
    #         content = request.data.content
    #     )
    #     new_blog.save()
    #     return redirect('/blog')
    # return render(request,'myapp/add_blog.html',{'name':'Arjun'})
    authors = Author.objects.all()
    form = BlogForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'myapp/add_blog.html', {'form': form, 'authors': authors})

def signup(request):
    if request.method == 'POST':
        try:
            new_user = User.objects.create_user(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                username = request.POST['username'],
                password = request.POST['password'],
                email = request.POST['email'],
            )
            # new_user.is_active = False
            new_user.save()
        except:
            pass
        return redirect('/signin/')
    return render(request,'myapp/signup.html',{'name':'Arjun'})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user != None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/signin/')
    return render(request,'myapp/signin.html',{})

@login_required
def signout(request):
    logout(request)
    return redirect('/signin')

class TodoCreateView(CreateView):
    model = Todo
    fields = '__all__'
    template_name = 'myapp/todo_create.html'
    success_url = reverse_lazy('todo_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'ToDo created successfully!')
        return response

class TodoListView(ListView):
    model = Todo
    template_name = 'myapp/todo_list.html'

class TodoEditView(UpdateView):
    model = Todo
    template_name = 'myapp/todo_edit.html'
    fields = ['title','desc']
    context_object_name = 'todo'
    success_url = reverse_lazy('todo_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'ToDo updated successfully!')
        return response

class TodoDetailView(DetailView):
    model = Todo
    template_name = 'myapp/todo_detail.html'
    context_object_name = 'todo'

class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'myapp/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')