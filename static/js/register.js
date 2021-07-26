function load_kab()
{
    $.ajax({
        type: "POST",
        url: "/register_btn",
        contentType: false,
        cache: false,
        processData: false,
        success: function(data){
           $(".kab").empty()
           for(const key in data.y){
                let time = document.createElement('div')
                time.className="form_radio_kab_btn"
                let id_kab = data.y[key].id
                let value_kab = data.y[key].value
	            time.innerHTML=`<input id=${id_kab} type="radio" name="radio_kab" value=${value_kab} checked><label for=${id_kab}>№${value_kab}</label>`
	            document.querySelector(".kab").append(time);
	            $(".form_radio_kab_btn").on("select", load())
           }
        }
    })
}

function load(){
    $.ajax({
        type: "POST",
        url: "/register_btn_time",
        contentType: false,
        cache: false,
        processData: false,
        success: function(data){
            $(".time").empty()
            for(const key in data.z){
                let time = document.createElement('div')
                time.className="form_radio_btn"
                let id = data.z[key].id
                let value = data.z[key].value
                time.innerHTML=`<input id=${id} type="radio" name="radio1" value=${value} checked><label for=${id}>${value}</label>`
                document.querySelector(".time").append(time);
            }
        }
    })
}

$(document).ready(function(){
     load_kab();
});