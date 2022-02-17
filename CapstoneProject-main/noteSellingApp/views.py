from django.http.response import JsonResponse
from django.shortcuts import render
from django.template.defaultfilters import safe, title
from django.views.generic import (TemplateView, DetailView,
                                    ListView, CreateView,
                                    UpdateView,DeleteView,FormView,)
from .models import Codetable, Review, Standard,Course, Lesson
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import LessonForm,ReviewForm

# Create your views here.


#search

def searchbar(request):
    if request.method=='GET':
        search = request.GET.get('search')
        post = Lesson.objects.all().filter(name__icontains=search)
        return render(request,'search.html',{'post':post})
    else:
        return render(request,'search.html')



def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = Lesson.objects.filter(name__icontains=query_original)
    mylist=[]
    mylist += [x.name for x in queryset]
    return JsonResponse(mylist,safe=False)
#search end

#code

def codetrick(request):
    if request.method=='GET':
        cd = request.GET.get('codedownload')
        cod = request.GET.get('code')

        if cod == '2901':
            ps = Lesson.objects.all().filter(name=cd)
            return render(request,'download.html',{'ps':ps})
        
    else:
        return render(request,'download.html')

#code





class StandardListView(ListView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'notesell/standard_list_view.html'

class CourseListView(DetailView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'notesell/course_list_view.html'

class LessonListView(DetailView):
    context_object_name = 'courses'
    model = Course
    template_name = 'notesell/lesson_list_view.html'




class LessonDetailView(DetailView,FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'notesell/lesson_detail_view.html'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'

        form = self.get_form(form_class)
       
        if form_name=='form' and form.is_valid():
            return self.form_valid(form)
       
    
    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.Standard
        course = self.object.course
        return reverse_lazy('noteSellingApp:lesson_detail',kwargs={'standard':standard.slug,
                                                             'course':course.slug,
                                                             'slug':self.object.slug})
    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.reviews.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
    
 
   


    
    




class LessonCreateView(CreateView):
    form_class = LessonForm
    context_object_name = 'course'
    model= Course
    template_name = 'notesell/lesson_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        return reverse_lazy('noteSellingApp:lesson_list',kwargs={'standard':standard.slug,
                                                             'slug':self.object.slug})

    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Standard = self.object.standard
        fm.course = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class LessonUpdateView(UpdateView):
    fields = ('name','description','image1','image2','image3','lesson_video','Notes')
    model= Lesson
    template_name = 'notesell/lesson_update.html'
    context_object_name = 'lessons'



class LessonDeleteView(DeleteView):
    model= Lesson
    context_object_name = 'lessons'
    template_name = 'notesell/lesson_delete.html'

    def get_success_url(self):
        print(self.object)
        standard = self.object.Standard
        course = self.object.course
        return reverse_lazy('noteSellingApp:lesson_list',kwargs={'standard':standard.slug,'slug':course.slug})




