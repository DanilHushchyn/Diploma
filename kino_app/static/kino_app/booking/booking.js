$('.content__banner').each(function (index,elem) {
    $(elem).css({
        'background-repeat': 'no-repeat',
        'background-image': `url(${$(elem).data('background')}) `,
        'background-position': `center`,
        'background-size': `cover`,
        'opacity': '1'
    })
});
$('.content__card').each(function (index,elem) {
    $(elem).css({
        'background-repeat': 'no-repeat',
        'background-image': `url(${$(elem).data('background')}) `,
        'background-position': `center`,
        'background-size': `cover`,
        'opacity': '1'
    })
});