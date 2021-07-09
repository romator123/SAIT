
function load()
{
    $.ajax({
        type: "POST",
        url: "/info",
        data: {text: 'Текст'}
        dataType: 'html',
        success: function({{a}}){
            var json = jQuery.parseJSON({{a}})
            //var json = JSON.parse(result)
            console.log(json.s1)


            //let json =
            //for(let el of json){
                //$("#content").html(el.surname)
                //$("#content").html(el.name)
                //$("#content").html(el.middle_name)
                //}
        }
    })
}

$(document).ready(function(){
     setInterval('load()',1000);
});
