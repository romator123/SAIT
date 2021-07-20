var data_late = ''

function load()
{
    $.ajax({
        type: "POST",
        url: "/info_new",
        contentType: false,
        cache: false,
        processData: false,
        success: function(data){
            if(JSON.stringify(data_late) !== JSON.stringify(data.x)){
                $(".content").empty()
                var table = document.createElement('table');
                for(const key in data.x){
                    let newRow = table.insertRow();
                    let name = newRow.insertCell(0);
                    let surname = newRow.insertCell(1);
                    let middle_name = newRow.insertCell(2);
                    name.innerHTML = data.x[key].name;
                    surname.innerHTML = data.x[key].surname;
                    middle_name.innerHTML = data.x[key].middle_name;
                }
                table.classList.add('person_table')
                let head = table.insertRow(0);
                head.style.position = "sticky";
                document.querySelector(".content").appendChild(table);
                data_late = data.x
            }
            else{
                return 0;
            }
        }
    })
}

$(document).ready(function(){
     setInterval('load()',1000);
});




