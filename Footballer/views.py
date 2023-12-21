from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from Footballer.models import Footballer, Game, Referee, Division, Club, Position
from Footballer.forms import GameForm, UserForm


def show_info(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="Судьи").exists():
            referee = Referee.objects.get(id_user_id=user.id)
            divisions = list(Division.objects.filter(referee_id=referee.id))
            return render(request, 'referee_view.html', {"referee": referee, "divisions": divisions})
        else:
            footballer = Footballer.objects.get(id_user_id=user.id)
            games = Game.objects.filter(footballer=footballer.id)
            games = list(games)
            return render(request, 'footballerInfo.html', {"footballer": footballer, "games": games, "request": 0})
    else:
        return redirect("")


def show_footballer(request, name_division, id_club, id_user):
    user = request.user
    if user.is_authenticated and user.groups.filter(name="Судьи").exists():
        footballer = Footballer.objects.get(id_user_id=id_user)
        games = Game.objects.filter(footballer=footballer.id)
        games = list(games)
        return render(request, 'footballerInfo.html', {"footballer": footballer, "games": games,
                                                       "name_division": name_division, "id_club": id_club, "request": 1})
    else:

        return render(request, 'notAccess.html')


def show_index(request):
    if request.method == "GET":
        cur_user = request.user
        if cur_user.is_authenticated:
            return redirect("/info")
        else:
            userform = UserForm()
            return render(request, 'index.html', {"form": userform})
    else:
        if request.POST.get("email") is not None:
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                username = User.objects.get(email=email).username
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect("/info")
            except Exception:
                print("NOT CORRECT EMAIL OR PASSWORD")
                return redirect("/")
        else:
            return redirect("/index/sign")


def signup(request):
    if request.method == "GET":
        userForm = UserForm()
        return render(request, 'sign.html', {"form": userForm})
    else:
        userForm = UserForm(request.POST)
        user = User.objects.create_user(email=request.POST.get("create_email"),
                                        username=request.POST.get("create_user_name"),
                                        password=request.POST.get("create_password"))
        if userForm.is_valid():
            obj = Footballer()
            obj.first_name = request.POST.get("create_first_name")
            obj.last_name = request.POST.get("create_last_name")
            obj.date_birth = request.POST.get("create_date")
            obj.club = Club.objects.get(id=userForm.data['club'])
            obj.Position = Position.objects.get(name=userForm.data['position'])
            obj.id_user_id = user.id
            obj.save()
        login(request, user)
    return redirect("/info")


def create_game(request, name_division, id_club, id_user):
    if request.method == "GET":
        gameForm = GameForm()
        return render(request, "templateForm.html", {"form": gameForm, "name_division": name_division, "id_footballer": Footballer.objects.get(id_user=id_user).id})
    else:
        gameForm = GameForm(request.POST)
        if gameForm.is_valid():
            obj = Game()
            obj.number = gameForm.cleaned_data['number']
            obj.goals = gameForm.cleaned_data['goals']
            obj.footballer = Footballer.objects.get(id_user_id=id_user)
            obj.division = Division.objects.get(name_division=name_division)
            obj.save()
            '''
            obj = Game.objects.create(
                footballer_id=Footballer.objects.get(id_user_id=id_user).id,
                division_id=Division.objects.get(name_division=name_division).referee,
                number=gameForm.cleaned_data['number'],
                goals=gameForm.cleaned_data['goals'])
            '''
            return redirect(f"/refereeView/{name_division}/{id_club}/{id_user}")
        else:
            print("ups")
            return redirect("/")


def delete_game(request, name_division, id_club, id_user, number_game):
    footballer_id = Footballer.objects.get(id_user_id=id_user).id
    game = Game.objects.filter(number=number_game, footballer_id=footballer_id).first().delete()
    return redirect(f"/refereeView/{name_division}/{id_club}/{id_user}")


def show_club_ofDivision(request, name_division):
    division = Division.objects.get(name_division=name_division)
    clubs = division.clubs.filter(division=division.name_division)
    footballersSumGoals = []
    clubsSumPeople = []
    for club in clubs:
        footballers = Footballer.objects.filter(club=Club.objects.get(id=club.id))
        sumGoals = 0
        numberplayers = 0
        for footballer in footballers:
            footballerGames = Game.objects.filter(footballer_id=footballer.id)
            sumGoals += sum(map(lambda x: x.goals, footballerGames))
            numberplayers += 1
        footballersSumGoals.append(sumGoals)
        clubsSumPeople.append(numberplayers)
    clubs = zip(clubs, footballersSumGoals, clubsSumPeople)

    return render(request, 'refereeViewClubs.html', {"clubs": clubs, "name_division": name_division})


def show_footballerFromGroup(request, id_club, name_division):
    footballers = Footballer.objects.filter(club=Club.objects.get(id=id_club))
    footballersSumGames = []
    footballersLastGames = []
    for footballer in footballers:
        footballerGames = Game.objects.filter(footballer_id=footballer.id)
        sumGoals = sum(map(lambda x: x.goals, footballerGames))
        footballersSumGames.append(sumGoals)
        footballersLastGames.append(max(map(lambda x: x.number, footballerGames), default=0))
    footballers = zip(footballers, footballersSumGames, footballersLastGames)
    return render(request, 'refereeViewFootballers.html',
                  {"footballers": footballers, "name_division": name_division, "id_club": id_club})


''' footballer testdjango  test2@test.ru
referee testdjango2  test@test.ru
footballer2 test3@test.ru testdjango3

footballerinfo <!-- <a href="{% url 'create_game' name_division id_club footballer.id_user_id %}" type="button" class="btn btn-primary">Add Game</a>-->
49  <a href="{% url 'delete_game' name_division id_club footballer.id_user_id game.number %}" type="button" class="btn btn-danger">Delete</a>
'''

'''
    else :
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.footballer = Footballer.objects.get(id_user_id=id_user)
            game.Referee = Referee.objects.get(id_user_id=request.user.id)
            game.save()
            return redirect(f"/showfootballer/{id_user}")
        else:
            print("ups")
            pass
        '''


# Create your views here.

# AJAX Views


def validate_username(request):
    username = request.GET.get('create_user_name', None)
    response = {
        'taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)


def check_numberGame(request, name_division, id_footballer):
    number = int(request.GET.get('number', None))
    if(number == ""):
        number = 0
    divisionObj = Division.objects.get(name_division=name_division)
    response = {
        'exist': Game.objects.filter(number=number, division=divisionObj, footballer_id=id_footballer).exists()
    }
    return JsonResponse(response)

