from django.shortcuts import render, get_object_or_404, redirect
from .forms import LoginUserForm, ElectionForm, PositionForm, CandidateForm, VoterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Election, Position, Voter, Candidate, Vote
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from functools import wraps

def voter_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if "voter_id" not in request.session:
            return redirect("my-login")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def home(request):
    return render(request, "maaun/home.html")

def my_login(request):
    form = LoginUserForm(request, data=request.POST)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
            
            messages.success(request, 'Login succeeded!')
        try:
            voter = Voter.objects.get(reg_no=username)
            if check_password(password, voter.password):  # Corrected password check
                # Store voter session manually
                request.session["voter_id"] = voter.id  
                request.session["voter_reg_no"] = voter.reg_no
                return redirect("v-dashboard")
        except Voter.DoesNotExist:
            pass

    context = {"form": form, "error": "Invalid credentials"}
    return render(request, "maaun/my-login.html", context)

def user_logout(request):
    logout(request)
    request.session.flush()  
    messages.success(request, 'You have logout!')
    return redirect("my-login")



@login_required(login_url='my-login')
def dashboard(request):
    presidential_position = Position.objects.filter(name__icontains='President').first()
    presidential_results = []
    if presidential_position:
        presidential_candidates = Candidate.objects.filter(position=presidential_position)
        for candidate in presidential_candidates:
            vote_count = Vote.objects.filter(candidate=candidate, position=presidential_position).count()
            presidential_results.append({'name': candidate.last_name, 'votes': vote_count}) # Use last_name

    vice_presidential_position = Position.objects.filter(name__icontains='Vice President').first()
    vice_presidential_results = []
    if vice_presidential_position:
        vice_presidential_candidates = Candidate.objects.filter(position=vice_presidential_position)
        for candidate in vice_presidential_candidates:
            vote_count = Vote.objects.filter(candidate=candidate, position=vice_presidential_position).count()
            vice_presidential_results.append({'name': candidate.last_name, 'votes': vote_count}) # Use last_name

    context = {
        "total_positions": Position.objects.count(),
        "total_elections": Election.objects.count(),
        "total_candidates": Candidate.objects.count(),
        "total_voters": Voter.objects.count(),
        "total_vote": Vote.objects.count(),
        'presidential_results': presidential_results,
        'vice_presidential_results': vice_presidential_results,
    }
    return render(request, "maaun/dashboard.html", context)


@login_required(login_url='my-login')
def elections(request):
    form = ElectionForm()
    if request.method == "POST":
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Succesfully Added Election!")
            return redirect("election")

    context = {"elections": Election.objects.all(), "form": form}
    return render(request, "maaun/election.html", context)

@login_required(login_url='my-login')
def positions(request):
    form = PositionForm()
    if request.method == "POST":
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Succesfully Added Position!")
            return redirect("position")
    positions = Position.objects.all()
    position_count = Position.objects.count
    context = {
        "positions": positions,
        "form": form,
        "position_count":position_count
        
        
        }
    return render(request, "maaun/position.html", context)

@login_required(login_url='my-login')
def candidates(request):
    form = CandidateForm()
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES)  # Handle image upload
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate Added Succesfully!")
            return redirect("candidate")
    candidates = Candidate.objects.all().order_by('position')
    candidate_count = Candidate.objects.count()
    context = {
                "candidates": candidates,    
                "form": form,
                "candidate_count":candidate_count
    
    
    }
    return render(request, "maaun/candidate.html", context)


@login_required(login_url='my-login')
def voters(request):
    form = VoterForm()

    if request.method == "POST":
        form = VoterForm(request.POST)
        if form.is_valid():
            voter = form.save(commit=False)
            voter.set_password(voter.reg_no)  
            voter.save()
            messages.success(request, "Voter added successfully!")
            return redirect("voter")
    voters = Voter.objects.all()
    voter_count = Voter.objects.count()
    context = {"voters":voters ,
                "form": form,
                "voter_count":voter_count
    
                }
    return render(request, "maaun/voter.html", context)

@login_required(login_url='my-login')
def final_result(request):
    positions = Position.objects.all()
    candidtes = Candidate.objects.all()
    context ={
        "positions":positions,
        "candidates":candidates
    }
    return render(request, 'maaun/final-result.html',context)

@login_required(login_url ='my-login')
def final_details(request, position_id): # Use pk instead of position_id
    position = get_object_or_404(Position, id=position_id)
    candidates = Candidate.objects.filter(position=position)
    results = []

    for candidate in candidates:
        vote_count = Vote.objects.filter(candidate=candidate, position=position).count()
        results.append({
            'candidate': candidate,
            'vote_count': vote_count,
        })
    results = sorted(results, key=lambda x: x['vote_count'], reverse=True)

    context = {
        "position": position,
        "results": results,
    }
    return render(request, 'maaun/final-details.html', context)



@voter_login_required
def voter_dashboard(request):
    if "voter_id" not in request.session:
        return redirect("my-login")  
    
    voter_reg_no = request.session.get("voter_reg_no", "N/A")
    candidates = Candidate.objects.all()
    positions = Position.objects.all()

    context = {
        
        "voter_reg_no": voter_reg_no,
        'candidates':candidates,
        'positions':positions,
    }
    

    return render(request, "maaun/v-dashboard.html", context)

@voter_login_required
def v_vote(request):
    if "voter_id" not in request.session:
        return redirect("v-voter_dashboard")  
    
    voter_reg_no = request.session.get("voter_reg_no", "N/A")
    candidates = Candidate.objects.all()
    positions = Position.objects.all()

    context = {
        
        "voter_reg_no": voter_reg_no,
        'candidates':candidates,
        'positions':positions,
    }


    return render(request, "maaun/v-vote.html", context)

@voter_login_required
def vote_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    voter_id = request.session.get('voter_id')
    if voter_id is None:
        messages.error(request, "voter session error")
        return redirect('v-vote')

    voter = Voter.objects.get(id=voter_id)

    position = candidate.position

    # Check if voter already voted for this position
    if Vote.objects.filter(voter=voter, position=position).exists():
        messages.success(request, "You have already voted for this position.")
        return redirect('v-vote')

    # Create the vote
    Vote.objects.create(voter=voter, candidate=candidate, position=position)

    messages.success(request,  "you have voted for this position.")
    return redirect('v-vote')

@voter_login_required
def candidates_list(request, position_id):
    position = get_object_or_404(Position, id=position_id)
    candidates = Candidate.objects.filter(position=position)
   
    election = position.election
    voter_id = request.session.get('voter_id') # get the voter_id from the session.
    if voter_id is None:
        messages.error(request, "voter session error")
        return redirect('v-vote')

    voter = Voter.objects.get(id=voter_id)

    voted_candidates = Vote.objects.filter(voter=voter, position=position).values_list('candidate_id', flat=True)
    

    context = {
        'position': position,
        'candidates': candidates,
        'election': election,
        'voted_candidates': voted_candidates,
    }

    return render(request, 'maaun/candidates-list.html', context)


@voter_login_required
def results(request):
    positions = Position.objects.all()

    context = {
        'positions': positions,
    }

    return render(request, 'maaun/results.html', context)

@voter_login_required
def results_detail(request, position_id):


    position = get_object_or_404(Position, id=position_id)
    candidates = Candidate.objects.filter(position=position)

    results_data = []
    for candidate in candidates:
        vote_count = Vote.objects.filter(candidate=candidate, position=position).count()
        results_data.append({
            'candidate': candidate,
            'vote_count': vote_count,
        })

    # sort the results by vote count.
    results_data = sorted(results_data, key=lambda x: x['vote_count'], reverse=True)

    context = {
        'position': position,
        'results': results_data,
    }

    return render(request, 'maaun/results_detail.html', context) 




@login_required(login_url='my-login')
def delete_item(request, model_name, item_id):
    """
    Generic delete view for Voters, Positions, and Candidates.
    """
    if request.method == "POST":
        try:
            if model_name == "voter":
                item = get_object_or_404(Voter, id=item_id)
                item.delete()
                messages.error(request, "Voter deleted successfully.")
                return redirect("voter")
            
            elif model_name == "position":
                item = get_object_or_404(Position, id=item_id)
                item.delete()
                messages.error(request, "Position deleted successfully.")
                return redirect("position")
            elif model_name == "candidate":
                item = get_object_or_404(Candidate, id=item_id)
                item.delete()
                messages.error(request, "Candidate deleted successfully.")
                return redirect("candidate")
            elif model_name == "election":
                item = get_object_or_404(Election, id=item_id)
                item.delete()
                messages.error(request, "Election deleted successfully.")
                return redirect("election")
            else:
                messages.error(request, "Invalid model name.")
                return redirect("dashboard")  # Redirect to a safe place
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect("dashboard")
    else:
        messages.error(request, "Invalid request method.")
        return redirect("dashboard")