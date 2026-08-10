/*====================================================

Theme Manager

====================================================*/

const body=document.body;

const selector=document.getElementById(

    "theme-selector"

);

const THEMES=[

    "light",

    "dark",

    "pink"

];

//----------------------------------------

function applyTheme(theme){

    THEMES.forEach(

        t=>body.classList.remove(t)

    );

    body.classList.add(theme === "light" ? "light" : theme);

    selector.value=theme;

    localStorage.setItem(

        "theme",

        theme

    );

}

//----------------------------------------

selector.addEventListener(

    "change",

    function(){

        applyTheme(

            this.value

        );

    }

);

//----------------------------------------

const saved=

localStorage.getItem(

    "theme"

)||"light";

applyTheme(saved);