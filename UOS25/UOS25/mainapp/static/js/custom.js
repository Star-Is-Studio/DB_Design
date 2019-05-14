$(window).resize(function(){
    var windowWidth = window.outerWidth;
    console.log(windowWidth);
    if(windowWidth < 900){
        $("#sdBar").addClass("nav nav-pills nav-justified");
        $("#sdBar").removeClass("sideBar side-bar-small");
        $('.main-small').css("margin","0");
    }
    else{
        $("#sdBar").addClass("sideBar side-bar-small");
        $("#sdBar").removeClass("nav nav-pills nav-justified");
        $('.main-small').css("margin-left","250px");
    }
});