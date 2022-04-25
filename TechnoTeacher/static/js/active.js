$(document).ready(function(){
    $('.link_cource_active li a').each(function () {
            var location = window.location.href;
            var link = this.href; 
            if(location == link) {
                $(this).addClass('active');
            }
        });
    });