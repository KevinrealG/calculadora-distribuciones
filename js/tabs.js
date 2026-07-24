/*
==========================================================

Probability Calculator

tabs.js

Controlador de pestañas

Author : Kevin Sossa

==========================================================
*/

class TabsManager{

    constructor(){

        this.tabs=document.querySelectorAll(

            "#results-tabs .tabs-title"

        );

        this.panels=document.querySelectorAll(

            ".tabs-panel"

        );

    }

    //------------------------------------------------------
    // Activar pestaña
    //------------------------------------------------------

    activate(panelId){

        this.tabs.forEach(tab=>{

            tab.classList.remove(

                "is-active"

            );

        });

        this.panels.forEach(panel=>{

            panel.classList.remove(

                "is-active"

            );

        });

        const panel=document.getElementById(

            panelId

        );

        if(panel){

            panel.classList.add(

                "is-active"

            );

        }

        const link=document.querySelector(

            `a[href="#${panelId}"]`

        );

        if(link){

            link.parentElement.classList.add(

                "is-active"

            );

        }

    }

    //------------------------------------------------------
    // Siguiente pestaña
    //------------------------------------------------------

    next(){

        let index=this.currentIndex();

        index++;

        if(index>=this.panels.length)

            index=0;

        this.activate(

            this.panels[index].id

        );

    }

    //------------------------------------------------------
    // Pestaña anterior
    //------------------------------------------------------

    previous(){

        let index=this.currentIndex();

        index--;

        if(index<0)

            index=this.panels.length-1;

        this.activate(

            this.panels[index].id

        );

    }

    //------------------------------------------------------
    // Índice actual
    //------------------------------------------------------

    currentIndex(){

        for(let i=0;i<this.panels.length;i++){

            if(

                this.panels[i].classList.contains(

                    "is-active"

                )

            ){

                return i;

            }

        }

        return 0;

    }

    //------------------------------------------------------
    // Nombre pestaña actual
    //------------------------------------------------------

    current(){

        return this.panels[

            this.currentIndex()

        ].id;

    }

}

//==========================================================
// Instancia global
//==========================================================

window.Tabs=new TabsManager();


//==========================================================
// API pública para PyScript
//==========================================================

window.openGraph=function(){

    Tabs.activate(

        "graph-tab"

    );

}

window.openTable=function(){

    Tabs.activate(

        "table-tab"

    );

}

window.openFormula=function(){

    Tabs.activate(

        "formula-tab"

    );

}

window.openDescription=function(){

    Tabs.activate(

        "description-tab"

    );

}

window.openInterpretation=function(){

    Tabs.activate(

        "interpretation-tab"

    );

}