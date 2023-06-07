from django.shortcuts import render
# to display lists and details
from django.views.generic import ListView, DetailView
from .models import Recipe  # to access Recipe model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import RecipesSearchForm
import pandas as pd
from .utils import get_recipename_from_id, get_chart

# Create your views here.

# function to return home.html template


def welcome(request):
    return render(request, 'recipes/recipes_home.html')


class RecipeListView(LoginRequiredMixin, ListView):  # class-based 'protected' view
    model = Recipe  # specify model
    template_name = 'recipes/main.html'  # specify template


class RecipeDetailView(LoginRequiredMixin, DetailView):  # class-based 'protected' view
    model = Recipe  # specify model
    template_name = 'recipes/detail.html'  # specify template

# ----------------------------------------------------------------------------------------------------------------------------

# define function-based view - records()
# keep protected


@login_required
def records(request):
    form = RecipesSearchForm(request.POST or None)
    recipe_df = None  # initialize dataframe to None
    recipe_diff = None
    chart = None
    qs = None
    # check if the button is clicked
    if request.method == 'POST':
        recipe_diff = request.POST.get('recipe_diff')  # read recipe_name
        chart_type = request.POST.get('chart_type')  # read recipe chart type

        if recipe_diff == '#1':
            recipe_diff = 'Easy'
        if recipe_diff == '#2':
            recipe_diff = 'Medium'
        if recipe_diff == '#3':
            recipe_diff = 'Intermediate'
        if recipe_diff == '#4':
            recipe_diff = 'Hard'

        qs = Recipe.objects.all()  # apply filter to extract data
        id_searched = []
        for obj in qs:
            diff = obj.calculate_difficulty()
            if diff == recipe_diff:
                id_searched.append(obj.id)

        qs = qs.filter(id__in=id_searched)

        if qs:  # if data found
            # convert the queryset values to pandas dataframe
            recipe_df = pd.DataFrame(qs.values())
            chart = get_chart(chart_type, recipe_df,
                              labels=recipe_df['name'].values)

            recipe_df = recipe_df.to_html()  # convert the dataframe to HTML

    # print(recipe_df)

    context = {
        'form': form,
        'recipe_df': recipe_df,
        'recipe_diff': recipe_diff,
        'chart': chart,
        'qs': qs,
    }

    return render(request, 'recipes/search.html', context)
