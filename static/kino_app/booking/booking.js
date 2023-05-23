

function getBookedTickets() {
    let elementRow = 0;
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
            url: `/get-booked-tickets/${seance_id}`,         /* Куда отправить запрос */
            method: 'get',             /* Метод запроса (post или get) */
            dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
            data: {},     /* Данные передаваемые в массиве */
            success: function(data){
                for(let row in data){
                    elementRow = $(`.hall__row[data-number="${row}"]`,'.hall')
                    data[row].forEach((item,index,array)=>{
                        elementRow.find(`.hall__seat:contains(${item}):first`).addClass('hall__seat_booked');
                    })
                }
            }
    });
}
getBookedTickets()
let choosedTickets = {}
let price = Number($('.price').html())
let totalPrice = $('.tprice')
let ticketsCount = $('.tcount')
$('.hall__seat').on('click',function () {
    if($(this).hasClass('hall__seat_choosed')){

        $(this).toggleClass('hall__seat_choosed')
        ticketsCount.html(Number(ticketsCount.html())-1)
        totalPrice.html(Number(totalPrice.html())-price)

    }else {

        $(this).toggleClass('hall__seat_choosed')
        // choosedTickets.push([$(this).parent().data('number'),$(this).html()])
        ticketsCount.html(Number(ticketsCount.html())+1)
        totalPrice.html(Number(totalPrice.html())+price)

    }

})

$('.main-card__btn').on('click',function () {
    if ($('.hall__seat_choosed').length>0){
        $('.hall__seat_choosed').each(function (i) {
            choosedTickets[i] = {[$(this).parent().data('number')] : $(this).html()}
        });
        $.ajax({
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            url: urlBooking,         /* Куда отправить запрос */
            method: 'post',             /* Метод запроса (post или get) */
            dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */

            data: {
                'choosedTickets': JSON.stringify(choosedTickets),
                'seance_id': seance_id,
                'user_id': user_id,
            },     /* Данные передаваемые в массиве */

            success: function(data){
                ticketsCount.html(Number(0))
                totalPrice.html(Number(0))
                $('.hall__seat_choosed').toggleClass('hall__seat_choosed')
                getBookedTickets()
            }
        });
    }else{
        alert('Билеты не выбраны')
    }

})
