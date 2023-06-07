// JavaScript code to search recipes on the search box, main template
function search_recipe() {
  let input = document.getElementById('searchbar').value;
  input = input.toLowerCase(); //store user search value in 'input' variable as lowercase
  let recipes = document.getElementsByClassName('recipe_searched'); //store list of recipes on database on variable 'recipes'

  let recipe_box = document.getElementsByClassName('search_results');
  recipe_box[0].style.display = 'block';

  for (i = 0; i < recipes.length; i++) {
    if (!recipes[i].innerHTML.toLowerCase().includes(input)) {
      //loop through recipes to display recipes matched with user search input
      recipes[i].style.display = 'none';
    } else {
      recipes[i].style.display = 'block';
    }
  }
  if (input == '') {
    recipe_box[0].style.display = 'none';
  }
}
