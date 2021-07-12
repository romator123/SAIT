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
                $("#content").empty()
                let output='<ul>';
                for(let key in data.x) {
                    output += '<li>' + data.x[key] +'</li>';
                }
                output+="</ul>";
                $("#content").append(output);
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
