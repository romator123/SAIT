let input = document.querySelectorAll(".inp");

for(let el of input){
    el.addEventListener("input", function(){
        this.value = this.value.replace(/[^a-zа-яё\s]/gi, '');
        this.value = this.value[0].toUpperCase() + this.value.slice(1).toLowerCase();
    })
}