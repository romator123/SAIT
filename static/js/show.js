$("input[name='radio_kab']").on("change", load_time())
let queue_time
function load_time(e){
    $('input[type="radio"]').click(function(){
        $.ajax({
            type: "PUT",
            url: "/show1?button=" + $('input[name="radio_kab"]:checked').val(),
            contentType: false,
            cache: false,
            processData: false,
            success: function(data){
                $(".content").empty()
                var table = document.createElement('table');
                for(const key in data.x){
                    let newRow = table.insertRow();
                    let kab = newRow.insertCell(0);
                    let time = newRow.insertCell(1);
                    let surname = newRow.insertCell(2);
                    let name = newRow.insertCell(3);
                    kab.innerHTML = data.x[key].kab;
                    time.innerHTML = data.x[key].time;
                    surname.innerHTML = data.x[key].surname;
                    name.innerHTML = data.x[key].name;
                    queue_time = data.x[key].time;
                }
                table.classList.add('person_table')
                let head = table.insertRow(0);
                head.style.position = "sticky";
                document.querySelector(".content").appendChild(table);
                data_late = data.x
            }
        })
    })
}

function time_check(){
    let close_time = document.querySelector('.person_table').rows[1].cells[1].textContent
    let date = new Date();
    let time = date.getHours() + ":" +  date.getMinutes();
    if(time >= close_time){

    }
    else{

    }
}

$(document).ready(function(){
     setInterval('load_time()',1000);
     setInterval('time_check()',5000);
});
