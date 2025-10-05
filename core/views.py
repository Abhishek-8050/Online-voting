from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Candidate, Voter, AdminUser   # AdminUser bhi import karo
import random


# Home page
def home(request):
    return render(request, "home.html")  # Temporary for testing  


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Candidate, Voter, AdminUser
import random

# Home page
def home(request):
    return render(request, "home.html")

# Admin form → submit ke baad add_candidate page pe bhejna hai
def admin_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        unique_code = request.POST.get("unique_code")

        # Save admin data in DB
        admin = AdminUser.objects.create(
            name=name,
            phone=phone,
            email=email,
            unique_code=unique_code
        )

        # ✅ session me admin ka unique_code save karo
        request.session["admin_code"] = admin.unique_code  

        return redirect("add_candidate")

    return render(request, "admin_form.html")


# Candidate add
def add_candidate(request):
    if request.method == "POST":
        name = request.POST.get("candidateName")
        admin_code = request.POST.get("admin_code")   # hidden field se milega

        try:
            admin = AdminUser.objects.get(unique_code=admin_code)
        except AdminUser.DoesNotExist:
            return HttpResponse("❌ Invalid Admin Code!")

        if name:
            unique_code = "CAND" + str(random.randint(1000, 9999))

            Candidate.objects.create(
                admin=admin,
                name=name,
                party="",
                unique_code=unique_code
            )

        return redirect("add_candidate")

    # ✅ sirf current admin ke candidates show karo
    admin_code = request.session.get("admin_code")
    candidates = Candidate.objects.filter(admin__unique_code=admin_code) if admin_code else []

    return render(request, "add_candidate.html", {
        "candidates": candidates,
        "admin_code": admin_code
    })




# Voter form page
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Candidate, Voter, AdminUser

def voter_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        unique_code = request.POST.get("unique_code")

        # ✅ Voter ko save karo
        voter = Voter.objects.create(
            name=name,
            phone=phone,
            email=email,
            unique_code=unique_code
        )

        # ✅ Check karo ki admin ka unique code match karta hai ya nahi
        if AdminUser.objects.filter(unique_code=unique_code).exists():
            # Agar match karta hai → us admin ke candidates dikhao
            return redirect("voting_page", unique_code=unique_code)
        else:
            return HttpResponse("❌ Invalid Unique Code, Voting not allowed!")

    return render(request, "voter_form.html")


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import AdminUser, Candidate

def voting_page(request, unique_code):
    # verify admin / session
    try:
        admin = AdminUser.objects.get(unique_code=unique_code)
    except AdminUser.DoesNotExist:
        return HttpResponse("❌ Invalid Voting Session Code")

    # only this admin's candidates
    candidates = Candidate.objects.filter(admin=admin)

    if request.method == "POST":
        # accept multiple possible field-names so template change not required
        candidate_id = request.POST.get("candidate_id") or request.POST.get("vote") or request.POST.get("vote_id")
        if not candidate_id:
            return HttpResponse("❌ No candidate selected.")

        # validate id
        try:
            cid = int(candidate_id)
        except (ValueError, TypeError):
            return HttpResponse("❌ Invalid candidate id.")

        # ensure candidate belongs to this admin
        try:
            candidate = Candidate.objects.get(id=cid, admin=admin)
        except Candidate.DoesNotExist:
            return HttpResponse("❌ Invalid Candidate Selected!")

        # increment votes if model has a votes field (optional)
        if hasattr(candidate, "votes"):
            candidate.votes = (candidate.votes or 0) + 1
            candidate.save()
        # otherwise, implement Vote model or whatever you prefer

        # redirect to thank you page (add URL + template as below)
        return redirect("thank_you")

    return render(request, "voting_page.html", {
        "candidates": candidates,
        "unique_code": unique_code
    })





#  this is for voting time limit setting
from django.shortcuts import render
from django.http import HttpResponse
from .models import VotingTime

def time_limit(request):
    if request.method == "POST":
        time_str = request.POST.get("time")  # format: HH:MM:SS
        if time_str:
            parts = time_str.split(":")  # ["HH", "MM", "SS"]

            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2]) if len(parts) == 3 else 0  # agar 2 part hai to sec = 0

            # Purane records inactive kar do
            VotingTime.objects.all().update(is_active=False)

            # Naya record save karo
            VotingTime.objects.create(
                hours=hours,
                minutes=minutes,
                seconds=seconds,
                is_active=True
            )

            return HttpResponse(f"✅ Voting Started for {hours}h {minutes}m {seconds}s!")

    return render(request, "time_limit.html")
def thank_you(request):
    return render(request, "thank_you.html")




