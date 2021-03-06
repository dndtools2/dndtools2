from django.shortcuts import render, get_object_or_404
from dnd.menu import menu_item, submenu_item
from dnd.mobile.dnd_paginator import DndMobilePaginator
from dnd.filters import DeityFilter
from dnd.models import Deity


@menu_item("deities")
def deity_list_mobile(request):
    f = DeityFilter(request.GET, queryset=Deity.objects.all())

    form_submitted = 1 if '_filter' in request.GET else 0

    paginator = DndMobilePaginator(f.qs, request)

    return render(request, 'dnd/mobile/deities/deity_list.html', context={'deity_list': paginator.items(),
      'paginator': paginator, 'filter': f, 'form_submitted': form_submitted,},)


@menu_item("deities")
def deity_detail_mobile(request, deity_slug):
    # fetch the deity
    deity = get_object_or_404(Deity.objects.select_related('favored_weapon', 'favored_weapon__rulebook'), slug=deity_slug)

    return render(request, 'dnd/mobile/deities/deity_detail.html', context={'deity': deity,
      'i_like_it_url': request.build_absolute_uri(), 'inaccurate_url': request.build_absolute_uri(),},)
