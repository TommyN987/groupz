from django.shortcuts import render

# Create your views here.


groups = [
    {'id': 1, 'name': "Let's learn Python"},
    {'id': 2, 'name': "Let's learn JavaScript"},
    {'id': 3, 'name': "Let's learn C++"},
    {'id': 4, 'name': "Let's learn Rust"},
]


def home(request):
    context = {'groups': groups}
    return render(request, 'base/home.html', context)


def group(request, pk):
    group = None
    for i in groups:
        if i['id'] == int(pk):
            group = i

    context = {'group': group}

    return render(request, 'base/group.html', context)
