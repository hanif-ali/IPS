from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from vote.models import House, Grade, Student, Poll, Candidate, Vote
from django.contrib.auth.models import User
from administration.forms import VoterForm, dynamicpollform
from django.db.utils import IntegrityError
from django.db.models import QuerySet
import time, random, string

# Create your views here.

def index(request):
    grades = Grade.objects.all()
    houses = House.objects.all()
    
    # Data for Summary Cards
    active_polls = Poll.objects.filter(active=True) # All Active Polls
    inactive_polls = Poll.objects.filter(active=False) # All Inactive Polls
    no_of_students = Student.objects.count() # Number of Registered Students
    no_of_candidates = Candidate.objects.count() # Number of Registered Candidates
    votes_casted = Vote.objects.count() # Total Votes Casted
    
    last_vote = Vote.objects.order_by("-poll_date", "-poll_time")[0]
    last_vote_date = last_vote.poll_date
    last_vote_time = last_vote.poll_time

    date_now = time.strftime("%D")
    time_now = time.strftime("%H:%M")


    #Data for charts
    results = []   # List of (Poll, {candidate_votes}) Tuples
    for a_poll in active_polls:
        candidates_votes = {} # Dictionary of {Candidate:vote} values
        for a_candidate in a_poll.candidates.all():
            # Select all votes of the candidates in the given poll
            votes = Vote.objects.filter(poll=a_poll).filter(candidate=a_candidate)
            number_of_votes = votes.count()
            candidates_votes[a_candidate] = number_of_votes
        # Add corresponding result to the results list
        # Each entry in results list is used to construct one chart
        results.append((a_poll, candidates_votes))

    return render(request, "administration/index.html", locals())


def polls(request):
    grades = Grade.objects.all()
    houses = House.objects.all()

    all_polls = [] # A list of (Poll, progress) tuples
    for poll in Poll.objects.all():
        no_of_votes = Vote.objects.filter(poll = poll).count()
        if poll.category == "HR":
            no_of_voting_students = Student.objects.count()
        else:
            no_of_voting_students = Student.objects.filter(grade = poll.grade).count()
        progress = no_of_votes*100/no_of_voting_students
        all_polls.append((poll, progress))

    return render(request, "administration/polls.html", locals())


def voters(request):
    grades = Grade.objects.all()
    houses = House.objects.all()

    try:
        filter_type = request.POST["filter_type"]
        filter_key = request.POST["filter_key"]
    except:
        voters_list = Student.objects.all()
    else:
        if filter_type == 'id':
            try:
                user = User.objects.get(username = str(filter_key))
                voters_list = Student.objects.filter(user=user)
            except:
                voters_list = []
        elif filter_type=="name":
            voters_list = Student.objects.filter(name__contains=filter_key)
        elif filter_type=="grade":
            try:
                grade = Grade.objects.get(name=str(filter_key))
                voters_list = Student.objects.filter(grade=grade)
            except:
                voters_list = []
        else:
            voters_list = []

    return render(request, "administration/voters.html", locals())



def addvoter(request):
    try:
        voter_data = request.POST
        voter_form = VoterForm(voter_data)
    except:
        return HttpResponseRedirect("/manage/voters?invalid_details=True")

    if voter_form.is_valid():
        voter_id = str(voter_form.cleaned_data['voter_id'])
        name = voter_form.cleaned_data['name']
        grade = Grade.objects.get(id=voter_form.cleaned_data['grade'])
        new_voter_user = User.objects.create_user(username=voter_id, password="dummy")
        try:
            new_voter_user.save()
        except IntegrityError:
            return HttpResponseRedirect("/manage/voters?id_exists="+voter_id)
        new_voter_student = Student(user=new_voter_user, name=name, grade=grade)
        new_voter_student.save()
    else:
        return HttpResponseRedirect("/manage/voters?invalid_details=True")

    return HttpResponseRedirect("/manage/voters?voter_added=True")



def deletevoter(request, voter_id):
    try:
        voter_user = User.objects.get(username=voter_id)
        voter_student = Student.objects.get(user=voter_user)
    except:
        return HttpResponseRedirect("/manage/voters")

    voter_student.delete()
    voter_user.delete()
    return HttpResponseRedirect("/manage/voters?voter_deleted=True")

    
def addpoll(request):
    number_of_candidates = request.POST["number_of_candidates"]
    PollForm = dynamicpollform(int(number_of_candidates))
    form = PollForm(request.POST)
    if form.is_valid():

        new_poll = Poll()

        try:
            house = House.objects.get(id=form.cleaned_data["house"])
            grade = Grade.objects.get(id=form.cleaned_data["grade"])
        except:
            return HttpResponseRedirect("/manage/polls?invalidinput=True")

        category = form.cleaned_data["category"]
        active = True
        new_poll.house = house
        new_poll.category = category
        new_poll.grade = grade
        new_poll.active = active
        new_poll.save()
        all_candidates = QuerySet

        for it_no in range(int(number_of_candidates)):
            candidate_id = form.cleaned_data["candidateid"+str(it_no)]
            try:
                candidate_user = User.objects.get(username = candidate_id)
                candidate_student = candidate_user.student_set.get()
                candidate = Candidate.objects.filter(student = candidate_student)
                if not candidate.count():
                    Candidate(student = candidate_student).save()
                    candidate = Candidate.objects.filter(student = candidate_student)
                all_candidates = all_candidates.union(candidate)
                

            except:
                new_poll.delete()
                return HttpResponseRedirect("/manage/polls?invalidinput=True")

        new_poll.candidates.set(all_candidates)
        new_poll.save()
        return HttpResponseRedirect("/manage/polls?added=True")

    else:
        return HttpResponseRedirect("/manage/polls?invalidinput=True")


def deletepoll(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
    except:
        return HttpResponseRedirect("/manage/polls?deletefail=True")

    votes = Vote.objects.filter(poll=poll)
    for vote in votes:
        vote.delete()

    poll.delete()
    return HttpResponseRedirect("/manage/polls?deleted=True")


def pollanalysis(request, poll_id):
    try:
        poll = Poll.objects.get(id = poll_id)
    except:
        return HttpResponseRedirect("/manage/polls?invalidinput=True")

    candidates_votes = {} # Dictionary of {Candidate:vote} values
    for a_candidate in poll.candidates.all():
        # Select all votes of the candidates in the given poll
        votes = Vote.objects.filter(poll=poll).filter(candidate=a_candidate)
        number_of_votes = votes.count()
        candidates_votes[a_candidate] = number_of_votes

    if poll.category == "HR":
        students_who_can_vote = Student.objects.all()
    else:
        students_who_can_vote = Student.objects.filter(grade = poll.grade)

    yet_to_vote = students_who_can_vote.difference(poll.voted.all())

    return render(request, 'administration/pollanalysis.html', locals())



def getcandidatename(request):
    try: 
        candidate_id = request.GET["id"];
        try:
            candidate = User.objects.get(username=str(candidate_id)).student_set.get()
            return HttpResponse(candidate.name)
        except:
            return HttpResponse("~")

    except:
        return HttpResponse("~")


def generate_random_key(space):
    return "".join(random.sample(space, 6))


def generateids(request):
    response = ""

    try:
        password = request.POST["password"]
    except:
        return render(request, "administration/generate_id_confirm.html", {})
    else:
        if request.user.check_password(password):
            for student in Student.objects.all():
                # Get the details of the student
                user = student.user
                name = student.name
                student_id = user.username
                #Generate a random key
                passkey = generate_random_key(string.ascii_letters + string.digits)
                # Set the users password to the randomly generated passkey
                user.set_password(passkey)
                user.save()

                response = response + "<p>ID={}, Name={}, Passkey={}</p>".format(student_id, name, passkey)

            return HttpResponse(response)
        else:
            return HttpResponseRedirect("/manage/generateids?invalid_pass=True")

    

