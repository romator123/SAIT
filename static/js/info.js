
function load()
{
    $.ajax({
        type: "POST",
        url: "/info_new",
        contentType: false,
        cache: false,
        processData: false,
        success: function(data){
            console.log("1")
            $("#content").text(data.x);
            var header = '<h2>My name is ' + data.x.name + '</h2>';
            var output='<ul>';
            for(var key in data.x) {
                output += '<li>' + key + ':' + data.x[key] +'</li>';
            }
            output+="</ul>";
            $("#content").innerHTML=output;
            $("#content").innerHTML += header;
        }
    })
}

$(document).ready(function(){
     setInterval('load()',1000);
});
