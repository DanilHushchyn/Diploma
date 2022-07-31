$(document).ready(function() {
    $('.carousel').lightSlider({
        adaptiveHeight:true,
        item:1,
        slideMargin:0,
        loop:true
    });
});

$('.carousel__item').each(function (index,elem) {
    if ($(elem).parent().data('number') == 1){
        $(elem).css({
            'background-repeat' : 'no-repeat',
            'background-image' : `linear-gradient(to right, RGBA(96, 96, 96,0.7),RGBA(96, 96, 96,0.7)) , url(${$(elem).data('background') }) `,
            'background-position' : `0% 100%, top`,
            'background-size' : `100% 150px, cover`,
            'opacity': '0.2 , 1'
            })
    }else{
        $(elem).css({
            'background-repeat' : 'no-repeat',
            'background-image' : `url(${$(elem).data('background') }) `,
            'background-position' : `top`,
            'background-size' : `cover`,

            })
    }
});

$('.carousel__item').on('click',function (event) {
    window.location.href = $(this).data('link');

})