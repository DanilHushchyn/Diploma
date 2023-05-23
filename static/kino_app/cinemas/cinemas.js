$('.content__banner').each(function (index,elem) {
    $(elem).css({
        'background-repeat': 'no-repeat',
        'background-image': `linear-gradient(to right, RGBA(96, 96, 96,0.7),RGBA(96, 96, 96,0.7)) , url(${$(elem).data('background')}) `,
        'background-position': `0% 100%, center`,
        'background-size': `100% 150px, cover`,
        'opacity': '0.2 , 1'
    })
});
