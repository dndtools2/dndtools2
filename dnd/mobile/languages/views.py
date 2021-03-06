from django.db.models import Q

from django.shortcuts import render, get_object_or_404
from dnd.menu import menu_item, submenu_item

from dnd.filters import LanguageFilter
from dnd.mobile.dnd_paginator import DndMobilePaginator
from dnd.models import Language, Race


@menu_item("races_monsters")
@submenu_item("languages")
def language_index_mobile(request):
    f = LanguageFilter(request.GET, queryset=Language.objects.distinct())

    paginator = DndMobilePaginator(f.qs, request)

    form_submitted = 1 if '_filter' in request.GET else 0

    return render(request, 'dnd/mobile/languages/language_index.html', context=
      {'language_list': paginator.items(), 'paginator': paginator,
       'filter': f, 'form_submitted': form_submitted,},)


@menu_item("races_monsters")
@submenu_item("languages")
def language_detail_mobile(request, language_slug):
    language = get_object_or_404(
        Language.objects, slug=language_slug,
    )
    assert isinstance(language, Language)

    race_list = Race.objects.filter(Q(automatic_languages=language) | Q(bonus_languages=language)).select_related(
        'rulebook').distinct().all()

    paginator = DndMobilePaginator(race_list, request)

    return render(request, 'dnd/mobile/languages/language_detail.html', context={'language': language,
      'paginator': paginator, 'race_list': race_list, 'i_like_it_url': request.build_absolute_uri(),
      'inaccurate_url': request.build_absolute_uri(),},)
    