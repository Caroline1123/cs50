document.addEventListener("DOMContentLoaded", function() {

    const randomButton = document.getElementById('random');
    randomButton.addEventListener('click', load_random)
})

function load_random() {
    let result = fetch('https://www.thecocktaildb.com/api/json/v1/1/random.php');
    result.then (data => 
        data.json()).then(d => {
            let recipe = d["drinks"][0];
            // Renders list of ingredients to the page
            const ingredients = document.getElementById("ingredients");
            ingredients.innerHTML="";
            for (let i = 1; i <= 15; i++) {
                let div = document.createElement("div");
                div.classList.add("row", "justify-content-center")
                let ingredientName = recipe[`strIngredient${i}`];
                let ingredientMeasure = recipe[`strMeasure${i}`];
                if (ingredientName && ingredientMeasure) {
                    div.innerHTML = `
                        <div class="col-2  text-end">
                            ${ingredientMeasure}
                        </div>
                        <div class="col-2 text-start ">
                            ${ingredientName}
                        </div> `;
                }
                ingredients.appendChild(div);
            }
            document.getElementById("cocktailName").innerText = `${recipe["strDrink"]}`;
            document.getElementById("preparation").innerText = `${recipe["strInstructions"]}`;
            document.getElementById("glass").innerText = `${recipe["strGlass"]}`;   
            document.getElementById("cocktailImage").src = `${recipe["strDrinkThumb"]}`;
            document.getElementById("recipe").classList.remove("d-none");
            });
        }

        
