active = true

function select(param) {

    if (active) {

        lista_de_marcas = Array.from(document.getElementsByClassName("marca_checkbox"))
        let selected = param.firstElementChild

        lista_de_marcas.forEach(element => {



            element.checked = false


        });

        selected.checked = true

    }

    active = false


}