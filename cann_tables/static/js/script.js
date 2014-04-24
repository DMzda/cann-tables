$(document).ready(function(){
    //Hide the choices 
    $("#chooseExpand").click(function(){
        var html = $(this).html();
        $("#choose").slideToggle(400, function(){
            if ($("#chooseExpand").text().indexOf("+") === -1) {
                $("#chooseExpand").html(html.replace("-", "+"));
            } else {
                $("#chooseExpand").html(html.replace("+", "-"));
            }
        });
    });

    //Hide if filtered
    $.each($("#choose :checkbox"), function(){
        if (this.checked) {
            $("#chooseExpand").trigger("click");
        }
        return false;
    });
});
