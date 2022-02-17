
from django.http.response import JsonResponse
from django.template.defaultfilters import safe, title
from .models import Blog,Topic,Post,Comment,Reply
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import (TemplateView, DetailView,
                                    ListView, CreateView,
                                    UpdateView,DeleteView,FormView,)
from .forms import PostForm,CommentForm,ReplyForm










class BlogListView(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'blogging/blog_list_view.html'

class TopicListView(DetailView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'blogging/topic_list_view.html'



class PostListView(DetailView):
    context_object_name = 'topics'
    model = Topic
    template_name = 'blogging/post_list_view.html'



#start detail

class PostDetailView(DetailView, FormView):
    context_object_name = 'posts'
    model = Post
    template_name = 'blogging/post_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
       
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)

        if form_name=='form' and form.is_valid():
            return self.form_valid(form)

        elif form_name=='form2' and form.is_valid():
            return self.form2_valid(form)
        
    def get_success_url(self):
        self.object = self.get_object()
        blog = self.object.blog
        topic = self.object.topic
        return reverse_lazy('blogApp:post_detail',kwargs={'blog':blog.slug,
                                                             'topic':topic.slug,
                                                             'slug':self.object.slug})
    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.post_name = self.object.comments.name
        fm.post_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())



#end detail







class PostCreateView(CreateView):
    form_class = PostForm
    context_object_name = 'topic'
    model= Topic
    template_name = 'blogging/post_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        blog = self.object.blog
        return reverse_lazy('blogApp:post_list',kwargs={'blog':blog.slug,
                                                             'slug':self.object.slug})


    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.blog = self.object.blog
        fm.topic = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class PostUpdateView(UpdateView):
    fields = ('title','article','post_image','video','ppt','Notes','link','youtube_link')
    model= Post
    context_object_name = 'posts'
    template_name = 'blogging/post_update.html'


class PostDeleteView(DeleteView):
    model= Post
    context_object_name = 'posts'
    template_name = 'blogging/post_delete.html'


    def get_success_url(self):
        print(self.object)
        blog = self.object.blog
        topic = self.object.topic
        return reverse_lazy('blogApp:post_list',kwargs={'blog':blog.slug,'slug':topic.slug})