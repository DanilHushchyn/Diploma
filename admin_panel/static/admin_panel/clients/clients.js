$('.form__elem_radio').each(function () {
    if ($(this).attr('checked')){
        $(this).parent().parent().css({
        background:'#00B894'
        })
    }
})
$('.form__elem_radio').on('mousedown','div',function (event) {

    $(this).find('input').click();

    $(this).parent().children().css({
        background:'#6C5CE7'
    })
    $(this).css({
        background:'#00B894'
    })
})