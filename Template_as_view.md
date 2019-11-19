1. url.py文件加上app_name

   ```
   app_name = 'polls'
   ```

2. html文件

   ```
   {% url 'polls:detail' question.id %}
   ```

   

<hr>

1. 引用generic

   >```
   >from django.views import generic
   >```
   >
   >list view
   >
   >```
   >class IndexView(generic.ListView):
   >    template_name = 'polls/index.html'
   >    context_object_name = 'latest_question_list'
   >```
   >
   >detail view
   >
   >```
   >class DetailView(generic.DetailView):
   >    model = Question
   >    template_name = 'polls/detail.html'
   >```

2. url 引用view

   >views.类名.as_view()
   >
   >```
   >views.IndexView.as_view()
   >```

   