//jQuery.fn.autoscroll = function(){
//    $('html,body').animate({
//        scrollTop: this.offset().top
//    }, 500);
//}
$(document).ready(function(){
    /** for the notices. */
    $("ul.msglist li").click(function(){
        $(this).parent().fadeOut();
    });
    
    /** handlers  for our generic prompts: yes/no */
    $("div.buttons a.no").click(function(){
        $.fancybox.close();
    });
    $("div.buttons a.yes").click(function(e){
        $(this).parents("ul.ullist li").animate({
            opacity: "hide"
        }, "slow");
        $.fancybox.close();
    });
    
    /** upon click displays the quiz-summary on the quiz-list page.*/
    $(".action.summary").click(function(){
        $(this).parents("ul.ulaction").siblings("div.quiz-summary").slideToggle("slow");
        $(this).toggleClass("active");
    });
    /** displays the tooltip on the quizlist actions. */
    //    $("ul.quizlt a.action").tipsy({
    //        fade: true,
    //    });
    /** tooltips on the quizoverview options */
    $("ul.quizOverView a").tipsy({
        fade: true
    });
    /** tooltips on the question-answer options */
    $(".editbox a").tipsy({
        fade: true,
        live: true,
        gravity: 'w',
    });
});

//// pie chart.
window.onload = function(){
    var r = Raphael("holder1");
//    r.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";
    r.g.text(300, 50, "Performance Analysis").attr({ "font-size": 20 });
    
    var pie = r.g.piechart(150, 200, 120, [55, 20, 13, 32], {
        legend: ["%%.%% - Correct", "%%.%% - InCorrect", "%%.%% - UnAttempted", "%%.%% - Partial"],
        legendpos: "east",
    });
    pie.hover(function(){
        this.sector.stop();
        this.sector.scale(1.1, 1.1, this.cx, this.cy);
        if (this.label) {
            this.label[0].stop();
            this.label[0].scale(1.5);
            this.label[1].attr({
                "font-weight": 800
            });
        }
    }, function(){
        this.sector.animate({
            scale: [1, 1, this.cx, this.cy]
        }, 500, "bounce");
        if (this.label) {
            this.label[0].animate({
                scale: 1
            }, 500, "bounce");
            this.label[1].attr({
                "font-weight": 400
            });
        }
    });
    
    ///// barchart.
    var r1 = Raphael("holder2", 600, 200 ), fin = function(){
        this.flag = r1.g.popup(this.bar.x, this.bar.y, this.bar.value || "0").insertBefore(this);
    }, fout = function(){
        this.flag.animate({
            opacity: 0
        }, 300, function(){
            this.remove();
        });
    }, fin2 = function(){
        var y = [], res = [];
        for (var i = this.bars.length; i--;) {
            y.push(this.bars[i].y);
            res.push(this.bars[i].value || "0");
        }
        this.flag = r.g.popup(this.bars[0].x, Math.min.apply(Math, y), res.join(", ")).insertBefore(this);
    }, fout2 = function(){
        this.flag.animate({
            opacity: 0
        }, 300, function(){
            this.remove();
        });
    };
    
    var data = $("input:hidden[name=qduration]").get();
    var value;
    var graphdata = [];
    
    for (i in data) { 
      value = parseInt($(data[i]).attr("value")) / 1000;
      graphdata.push( value );
    };
    console.log("data is : " + graphdata);
    r1.g.barchart(10, 10, 600, 220, [graphdata]).hover(fin, fout);
    
//    r1.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";
//    r1.g.text(160, 10, "Single Series Chart");
//    r1.g.text(480, 10, "Multiline Series Stacked Chart");
//    r1.g.text(160, 250, "Multiple Series Chart");
//    r1.g.text(480, 250, "Multiline Series Stacked Chart\nColumn Hover");
    
//    r1.g.hbarchart(330, 10, 300, 220, [[55, 20, 13, 32, 5, 1, 2, 10], [10, 2, 1, 5, 32, 13, 20, 55]], {
//        stacked: true
//    }).hover(fin, fout);
//    r1.g.hbarchart(10, 250, 300, 220, [[55, 20, 13, 32, 5, 1, 2, 10], [10, 2, 1, 5, 32, 13, 20, 55]]).hover(fin, fout);
//    var c = r1.g.barchart(330, 250, 300, 220, [[55, 20, 13, 32, 5, 1, 2, 10], [10, 2, 1, 5, 32, 13, 20, 55]], {
//        stacked: true,
//        type: "soft"
//    }).hoverColumn(fin2, fout2);
//    c.bars[1].attr({stroke: "#000"});
};


//create a question-form.
//create a question-form.
//create a question-form.
//create a question-form.
//create a question-form.
$(function(){
  $(".qbox").buttonset();
  //    $(".answer-option .radiobutton").buttonset();
  $('.add-answer').bind('click', function(){
      return addForm(this, 'form');
  });
  $('.delete-answer').live('click', function(){
      return deleteForm(this, 'form');
  });
  
  $('.qbox input:radio').live('click', function(el){
    var forms = $(".abox .answer-option");
    if ($(this).attr("value") === "MultipleChoice") {
      //todo to ensure, there are only four options.
      for (i = 0; i < 4 - forms.length; i++) {
          addForm("", 'form');
      }
      var frms = $(".abox .answer-option");
      for (i = 4; i < forms.length; i++) {
          var el = frms[i];
          deleteForm($(el).children('.delete-answer'), 'form');
      }
    }
    if ($(this).attr("value") === "TrueFalse") {
      //todo to ensure, there are only four options.
      for (i = 0; i < 2 - forms.length; i++) {
          addForm("", 'form');
      }
      var frms = $(".abox .answer-option");
      for (i = 2; i < forms.length; i++) {
          var el = frms[i];
          deleteForm($(el).children('.delete-answer'), 'form');
      }
    }
    if ($(this).attr("value") === "Essay") {
      //todo to ensure, there are only four options.
      for (i = 0; i < 1 - forms.length; i++) {
          addForm("", 'form');
      }
      var frms = $(".abox .answer-option");
      for (i = 1; i < forms.length; i++) {
          var el = frms[i];
          deleteForm($(el).children('.delete-answer'), 'form');
      }
    }
    if ($(this).attr("value") === "FillBlank") {
      //todo to ensure, there are only four options.
      for (i = 0; i < 3 - forms.length; i++) {
          addForm("", 'form');
      }
      var frms = $(".abox .answer-option");
      for (i = 3; i < forms.length; i++) {
          var el = frms[i];
          deleteForm($(el).children('.delete-answer'), 'form');
      }
    }
    if ($(this).attr("value") === "Passage") {
      //todo to ensure, there are only four options.
      for (i = 0; i < 1 - forms.length; i++) {
          addForm("", 'form');
      }
      var frms = $(".abox .answer-option");
      for (i = 1; i < forms.length; i++) {
          var el = frms[i];
          deleteForm($(el).children('.delete-answer'), 'form');
      }
    }
  });
});

function updateElementIndex(el, prefix, ndx){
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    
    if ($(el).attr("for")) 
        $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) 
        el.id = el.id.replace(id_regex, replacement);
    if (el.name) 
        el.name = el.name.replace(id_regex, replacement);
}

function addForm(btn, prefix){
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var row = $('.abox .answer-option:first').clone(false).get(0);
    $(row).removeAttr('id').insertAfter($('.abox .answer-option:last'));
    $(row).children().each(function(){
        updateElementIndex(this, prefix, formCount);
        $(this).val('');
        if ($(this).hasClass('add-answer')) {
            $(this).removeClass('add-answer').addClass('delete-answer');
        };
            });
    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
    return false;
}

function deleteForm(btn, prefix){
    var frms = $('.abox .answer-option');
    if (frms.length == 1) 
        return false;
    
    //remove the answer option with animation
    $(btn).parent().fadeOut('fast', function(){
        $(this).remove();
        var forms = $('.abox .answer-option');
        $('#id_' + prefix + '-INITIAL_FORMS').val(0);
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i = 0, formCount = forms.length; i < formCount; i++) {
            $(forms.get(i)).children().each(function(){
                updateElementIndex(this, prefix, i);
            });
        }
    });
    return false;
}

$(function(){
  var timeelapsed = 0;
  function updatetime(){
    timeelapsed = timeelapsed + 1;
    seconds = timeelapsed % 60;
    minutes = Math.floor(Math.floor(timeelapsed / 60) % 60);
    hours = Math.floor(timeelapsed / 3600);
    
    seconds = seconds + "";
    if (seconds.length == 1){
        seconds = "0" + seconds;
    }
    minutes = minutes + "";
    if (minutes.length == 1){
        minutes = "0" + minutes;
    }
    hours = hours + "";
    if (hours.length == 1){
        hours = "0" + hours;
    }
    timer = hours + ":" + minutes + ":" + seconds;
    $('input:hidden[name=duration]').val(timeelapsed * 1000);
    $('li.timer a.time').text(timer);
  };
  if ($('li.timer a.time')){
    setInterval(updatetime, 1000);
  }
});

//HummingbirdTracker = {};
//
//HummingbirdTracker.track = function(env) {
//  delete env.trackingServer;
//  delete env.trackingServerSecure;
//  env = {}
//  env.u = document.location.href;
//  env.bw = window.innerWidth;
//  env.bh = window.innerHeight;

//not required right now.
//  env.guid = document.cookie.match(/guid=([^\_]*)_([^;]*)/)[2];
//  env.gen = document.cookie.match(/gender=([^;]*);/)[1];
//  env.uid = document.cookie.match(/user_id=([^\_]*)_([^;]*)/)[2];

//  if(document.referrer && document.referrer != "") {
//    env.ref = document.referrer;
//  }

//  $('body').append('<img src="http://192.168.1.4:8000/tracking.gif?' + jQuery.param(env) + '"/>');
//};

//HummingbirdTracker.track();
