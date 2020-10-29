document.addEventListener('DOMContentLoaded', () => {

    localStorage.clear();
  
})


function show_country_info(e){

    const parentElement = e.parentElement.parentElement.parentElement
    const country = parentElement.querySelector('h6').innerText.trim()

    if (!!localStorage.getItem(country)){
        localStorage.removeItem(country)
        const card = parentElement.querySelector('.card')
        card.style.display = 'none';

    }else{
        localStorage.setItem(country, JSON.stringify(true))
        const card = parentElement.querySelector('.card')
        card.style.display = 'block';
    }
}