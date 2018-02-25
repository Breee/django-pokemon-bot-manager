from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# shows all permissions a user has
@login_required
def test(request):
    u = request.user
    print(u.user_permissions.all())
    return HttpResponse(u.user_permissions.all())
