function load()
{
$.ajax({
        type: "POST",
        url: "/new_load",
        success: function(data){
            if(data.auth == true){
                console.log("asdsd")
            }}
})
}

$(document).ready(function(){
     load();
     setInterval('load()',5000);
});