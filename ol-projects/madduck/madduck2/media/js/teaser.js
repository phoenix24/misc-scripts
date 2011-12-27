$(document).ready(function(){
    $("a.next").click(function(){
        if ($(".main").hasClass("teaser1")) {
            resetStep();
            $(".main").addClass("teaser2");
            $("a.previous").css("display", "block");
            return;
        }
        else {
            if ($(".main").hasClass("teaser2")) {
                resetStep();
                $(".main").addClass("teaser3");
                $("a.previous").css("display", "block");
                return;
            }
            if ($(".main").hasClass("teaser3")) {
                resetStep();
                $(".main").addClass("teaser4");
                $("a.next").css("display", "none");
                $(".form").css("display", "block");
                return;
            }
        }
    });
    $("a.previous").click(function(){
        if ($(".main").hasClass("teaser4")) {
            resetStep();
            $(".main").addClass("teaser3");
            $("a.next").css("display", "block");
            $(".form").css("display", "none");
            return;
        }
        else {
            if ($(".main").hasClass("teaser3")) {
                resetStep();
                $(".main").addClass("teaser2");
                $("a.next").css("display", "block");
                return;
            }
            if ($(".main").hasClass("teaser2")) {
                resetStep();
                $(".main").addClass("teaser1");
                $("a.previous").css("display", "none");
                return;
            }
        }
    });
    function resetStep(){
        $(".main").removeClass("teaser1").removeClass("teaser2").removeClass("teaser3").removeClass("teaser4");
        $(".form").css("display", "none");
    }
});
