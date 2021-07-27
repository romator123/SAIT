$("input[name='radio_kab']").on("click", load_time())

function load_time(e){
    $('input[type="radio"]').click(function(){
        $.ajax({
            type: "PUT",
            url: "/register",
            contentType: false,
            cache: false,
            processData: false,
            data: {text: $('input[name="radio_kab"]:checked').val()},
            success: function(data){
                console.log(data)
            }
        })
    })
}

function load(){
    $.ajax({
        type: "PUT",
        url: "/register",
        contentType: false,
        cache: false,
        processData: false,
        success: function(data){
            $(".time").empty()
            for(const key in data.z){
                let time = document.createElement('div')
                time.className="form_radio_btn"
                let id = data.z[key].id
                let value = data.z[key].time
                time.innerHTML=`<input id=${id} type="radio" name="radio1" value=${value} checked><label for=${id}>${value}</label>`
                document.querySelector(".time").append(time);
            }
        }
    })
}



$(document).ready(function() {
  $("div#div1").click(function() {
    $("div#div2").slideToggle();
  });
});


$('.inp').on('input', function(){
    if(CheckForm()){
        console.log(123)
    }
});

function CheckForm(){
    let requiredField = $(".inp"); // Получаем все элементы, которые указаны как обязательные к заполнению
    for(let i = 0; i < requiredField.length; i++) { // Обходим все полученные элементы
        if($(requiredField[i]).val() == '') { // Если хотя бы одно из обязательных полей не заполнено
            return false; // Возвращаем false
        }
    }
    return true;
}