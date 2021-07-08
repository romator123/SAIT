function load()
        {
            $.ajax({
                type: "POST",
                url: "{{url_for('app.info') }}",
                success: function(result) {
                    let json = JSON.parse(result)
                    for(let el of json){
                        $("#content").html(el.surname)
                        $("#content").html(el.name)
                        $("#content").html(el.middle_name)
                    }
                }
            })
        }

$(document).ready(function(){
     setInterval('load()',1000);
});