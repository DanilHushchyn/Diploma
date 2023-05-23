
$('body').each(function (index,elem) {

    $(elem).css({
        'background':` url('${$(elem).data('background')}') center/100% 100% no-repeat`,
        'background-attachment':`fixed`,
    })
})
