// $('.content__banner').each(function (index,elem) {
//     $(elem).css({
//         'background-repeat': 'no-repeat',
//         'background-image': `linear-gradient(to right, RGBA(96, 96, 96,0.7),RGBA(96, 96, 96,0.7)) , url(${$(elem).data('background')}) `,
//         'background-position': `0% 100%, center`,
//         'background-size': `100% 100px, cover`,
//         'opacity': '0.2 , 1'
//     })
// });
// $(document).ready(function() {
//     $('.carousel').lightSlider({
//         adaptiveHeight:true,
//         item:1,
//         slideMargin:0,
//         loop:true
//     });
// });
// $('.carousel__item').each(function (index,elem) {
//         $(elem).css({
//             'background-repeat' : 'no-repeat',
//             'background-image' : `url(${$(elem).data('background') }) `,
//             'background-position' : `top`,
//             'background-size' : `cover`,
//
//             })
// });

$('.info__time').hover(function () {
    $(this).find('.info__descr').fadeToggle('slow')

})
$('.info__time').each(function () {
    $(this).find('.info__descr').hide()

})

$('#form-filter').on('change',function () {
     $.ajax({
        url: urlSchedule,         /* Куда отправить запрос */
        method: 'get',             /* Метод запроса (post или get) */
        dataType: 'html',          /* Тип данных в ответе (xml, json, script, html). */
        data: $(this).serialize(),     /* Данные передаваемые в массиве */
        context: $('.film__info'),     /* Данные передаваемые в массиве */
        success: function(data){
            $(this).html(data)
            $('.info__time').each(function () {
                $(this).find('.info__descr').hide()

            })
            $('.info__time').hover(function () {
                $(this).find('.info__descr').fadeToggle('slow')
            })
        }
    });
 })

