let input = document.querySelectorAll(".inp");
let submit_btn = document.querySelectorAll(".register_btn");
for(let el of input){
    el.addEventListener("input", function(){
        this.value = this.value.replace(/[^a-zа-яё\s]/gi, '');
        this.value = this.value[0].toUpperCase() + this.value.slice(1).toLowerCase();
    })
}
submit_btn.addEventListener("click", check())

function check(){
    for(let el of input){
        if(el.value = ""){
            return false;
        }
    }
})
$('form').submit(function(){
  if(!check){
    return false;
  }
});