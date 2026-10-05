let counternumber = document.getElementById('counterValue')
let incrementbutton = document.getElementById('increment')
let decrementbutton = document.getElementById('decrement')
let resetbutton = document.getElementById('reset')

let count= 0;

incrementbutton.addEventListener('click', function(){
    count++;
    counternumber.innerHTML = count;
})

decrementbutton.addEventListener('click', function(){
    count--;
    counternumber.innerHTML = count;
})

resetbutton.addEventListener('click', function(){
    count = 0;
    counternumber.innerHTML = count;
})