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
            if(data_late != data.x){
                $(".content").empty()
                var table = document.createElement('table');
                for(const key in data.x){
                    let newRow = table.insertRow(key);
                    let name = newRow.insertCell(0);
                    let surname = newRow.insertCell(1);
                    let age = newRow.insertCell(2);
                    name.innerHTML = data.x[key].name;
                    surname.innerHTML = data.x[key].surname;
                    age.innerHTML = data.x[key].age;
                }
                table.classList.add('person_table')
                let head = table.insertRow(0);
                head.style.position = "sticky";
                document.querySelector(".content").appendChild(table);
                /*let output='<ul>';
                for(let key in data.x) {
                    output += '<li>' + data.x[key] +'</li>';
                }
                output+="</ul>";
                $(".content").append(output);*/
                data_late = data.x
                console.log("123")
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
