$("input[name='radio_kab']").on("change", load_time())

function load_time(e){
    $('input[type="radio"]').click(function(){
        $.ajax({
            type: "PUT",
            url: "/show?button=" + $('input[name="radio_kab"]:checked').val(),
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
                }
                table.classList.add('queue_table')
                let head = table.insertRow(0);
                head.style.position = "sticky";
                document.querySelector(".content").appendChild(table);
                data_late = data.x
            }
            else{
                return 0;
            }
        }

            }
        })
    })
}