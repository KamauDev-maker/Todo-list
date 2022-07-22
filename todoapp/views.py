from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'todoapp/login.html'   
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('task')
    
class RegisterPage(FormView):
        template_name = 'todoapp/register.html'
        form_class = UserCreationForm
        redirect_authenticated_user = True
        success_url = reverse_lazy('task')
        
        def form_valid(self, form):
            user = form.save()
            if user is not None:
                login(self.request,user)
            return super(RegisterPage,self).form_valid(form)
    
        
        
    
    
    
    
class TaskList(LoginRequiredMixin ,ListView):
    model = Task
    context_object_name = 'task'
    
    # to make other users to not see task list items for other users
    def get_context_data(self,**kwargs):
        context  =super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(complete=False).count()
        return context
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task   
    context_object_name = 'task'
    template_name ='todoapp/task.html' #create a customtemplate
    
class TaskCreate(LoginRequiredMixin,CreateView):
     model = Task
     fields = ['title', 'description', 'complete']
     success_url = reverse_lazy('task')
     
     def form_valid(self, form):
         form.instance.user = self.request.user
         return super(TaskCreate,self).form_valid(form)
     
class TaskUpdate(LoginRequiredMixin,UpdateView):
     model = Task
     fields = ['title', 'description', 'complete']
     success_url = reverse_lazy('task')
      
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task')
        
     
       