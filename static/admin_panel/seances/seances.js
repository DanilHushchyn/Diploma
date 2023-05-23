let seanceId = 0
// $('.info__time').mouseenter(function () {
//     $(this).find('.info__descr').stop().show('fast')
//     $(this).find('.info__remove').stop().show('fast')
//     $(this).parents('.info__hall').find('.info__hall_scheme').stop().fadeToggle('fast')
//     seanceId = $(this).data('seance_id')
//     getTickets()
//
// })
// $('.info__time').mouseleave(function () {
//     $('.hall__booked').removeClass('hall__booked')
//
//     setTimeout(()=>{
//         $(this).find('.info__descr').stop().fadeOut('fast')
//         $(this).find('.info__remove').stop().fadeOut('fast')
//     },5000)
//     $(this).parents('.info__hall').find('.info__hall_scheme').stop().fadeToggle('fast')
// }
// )

$('#form-filter').on('change',function () {
     $.ajax({
        url: '/admin/seances',         /* Куда отправить запрос */
        method: 'get',             /* Метод запроса (post или get) */
        dataType: 'html',          /* Тип данных в ответе (xml, json, script, html). */
        data: $(this).serialize(),     /* Данные передаваемые в массиве */
        context: $('film'),     /* Данные передаваемые в массиве */
        success: function(data){   /* функция которая будет выполнена после успешного запроса.  */

            $('.film').html(data)
            $('.info__time').hover(function () {
                // $(this).find('.info__descr').stop().toggle('fast')
                // $(this).parents('.info__hall').find('.info__hall_scheme').stop().fadeToggle('fast')
                seanceId = $(this).data('seance_id')
                // getTickets()
            })
        }
    });
 })


//
// function getTickets() {
//     $.ajax({
//         url: `/get-booked-tickets/${seanceId}`,         /* Куда отправить запрос */
//         method: 'get',             /* Метод запроса (post или get) */
//         dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
//         data:  {
//             'seance_id': seanceId,
//         },
//         success: function(data){
//             for (let row in data){
//                 let rowElement = $(`.hall__row[data-number=${row}]`)
//                 for (let seat of data[row]){
//                    $( rowElement.children('.hall__seat').filter( function (index,value) {
//                         return value.innerText == seat
//                     })).toggleClass('hall__booked')
//                        // .replaceWith(`<div class="hall__booked">&#10006;</div>`)
//                 }
//                 // console.log(row,'hello')
//             }
//
//
//         }
//     });
// }
