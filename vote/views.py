from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import permission_required, user_passes_test
from vote.models import Poll, Vote, Student, Candidate
import time

# Create your views here.

def user_is_student(user):
    try:
        if len(user.student_set.all())>1:
            raise Exception("More than one Students for a single user")
        return len(user.student_set.all())==1
    except AttributeError:
        return False

@user_passes_test(user_is_student, login_url="/login/")
@permission_required("vote.add_vote", login_url="/login/")
def index(request):
    """This view renders the polls page which contains a list of polls that the student can vote for. The view first acquires all the polls the student is allowed to vote and determines whether or not the logged in student has voted in each of them. Then it forwards a context with a list of (voted, poll) tuples to the index.html template and renders it"""

    #Acquire data about the logged in user
    username = request.user.username
    student = Student.objects.get(user=request.user)

    #create the (voted,polls list)
    polls = [] #Container for (voted, poll) Tuples
    all_casted = True
    for i in Poll.objects.filter(active=True): #Select all active polls
        if i.category == "HR" or i.grade==student.grade: #if the student can vote
            voted = student in i.voted.all() #Bool representing if a student has voted
            if not voted:
                all_casted = False
            polls.append((voted, i))

    return render(request, "vote/index.html", locals())

    

@user_passes_test(user_is_student, login_url="/login/")
@permission_required("vote.add_vote", login_url="/login/")
def vote(request, poll_id):
    """ View for the Vote page for a certain poll whose id is given by poll_id. After assuring that the student is allowed to vote and has not already voted in the selected poll, the page renders a list of all the candidates for the selected poll""" 

    #Acquire data about the logged in user
    username = request.user.username
    student = Student.objects.get(user=request.user)

    #Assure that student is able to vote in the selected poll and has not already voted
    try:
        poll = Poll.objects.get(id=poll_id) #Extract poll data. Generate Exception if not found
        assert poll.active #Ensure that the poll is running
        assert poll.category=="HR" or poll.grade==student.grade  #Ensure that student is allowed to vote
        assert student not in poll.voted.all() #Ensure that the student has not already voted
    except: 
        return HttpResponseRedirect("/index/") #Go back to polls page
    
    candidates = poll.candidates.all() #List of all candidates in the selected poll
    
    return render(request, "vote/vote.html", locals())


@user_passes_test(user_is_student, login_url="/login/")
@permission_required("vote.add_vote", login_url="/login/")
def cast(request, poll_id, candidate_id):

    #Acquire data about the logged in user
    username = request.user.username
    student = Student.objects.get(user=request.user)

    #Assure that student is able to vote in the selected poll and has not already voted.
    #Also assure that the selected candidate is contesting for the selected poll
    try:
        poll = Poll.objects.get(id=poll_id) #Extract poll data. Generate Exception if not found
        assert poll.active #ensure that the poll is running
        assert poll.category=="HR" or poll.grade==student.grade  #Ensure that student is allowed to vote
        assert student not in poll.voted.all() #Ensure that the student has not already voted
        assert Candidate.objects.get(id=candidate_id) in poll.candidates.all() #Verify selected candidate_id
    except: 
        return HttpResponseRedirect("/index/") #Go back to polls page
    
    #Mark the logged in student as voted in the selected poll
    poll.voted.add(student)
    poll.save()

    #Get the selected candidate's data and current time
    candidate = Candidate.objects.get(id=candidate_id)
    poll_date = time.strftime("%Y-%m-%d")
    poll_time = time.strftime("%H:%M:%S")

    #Add a vote for the selected candidate in the Vote table
    vote_to_cast = Vote(poll=poll, candidate=candidate, poll_date=poll_date, poll_time=poll_time)
    vote_to_cast.save()

    return HttpResponseRedirect("/index/?vote_casted=True") #Redirect to polls page
    



def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/index/") 
        else:
            return render(request, "vote/login.html", {"error":True})
        
    return render(request, "vote/login.html", {})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")
