$("input[name='radio_kab']").on("change", load_time())

function load_time(e){
    $('input[type="radio"]').click(function(){
        $.ajax({
            type: "PUT",
            url: "/register?button=" + $('input[name="radio_kab"]:checked').val(),
            contentType: false,
            cache: false,
            processData: false,
            success: function(data){
                $(".time").empty()
                for(let key in data.z){
                    let time = document.createElement('div')
                    time.className="form_radio_btn"
                    let id = data.z[key].id
                    let value = data.z[key].time
                    time.innerHTML=`<input id=${id} type="radio" name="radio1" value=${value}><label for=${id}>${value}</label>`
                    document.querySelector(".time").append(time);
                }
            }
        })
    })
}