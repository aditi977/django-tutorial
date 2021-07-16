from django.http import HttpResponse, HttpResponseRedirect 
# from django.template import loader

from django.shortcuts import get_object_or_404, render
from .models import Question, Choice
from django.urls import reverse
from django.db.models import F
from django.http import Http404

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html') # uses loader to get html template instead of coding it in here
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

# shortcut to ^above function using render() 
# b/c "it’s a very common idiom to load a template, fill a context and return an HttpResponse object with the result of the rendered template." 
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})


# shortcut to ^above function by using get_object_or_404()
# "The get_object_or_404() function takes a Django model as its first argument 
# and an arbitrary number of keyword arguments, which it passes to the get() 
# function of the model’s manager. It raises Http404 if the object doesn’t exist."
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)


# NOTE: this has a race condition because two users could vote at the exact same time, messing up the vote count
# SOLUTION: Using F(), we can allow a value to be directly updated in database bc it passes instructions directly to db, thus not having to deal with race conditions
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # avoiding race condition here
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))