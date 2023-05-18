$('.info__time').hover(function () {
    $(this).find('.info__descr').fadeToggle('slow')

})
$('.info__time').each(function () {
    $(this).find('.info__descr').hide()

})


$('#form-filter').on('change',function () {
     $.ajax({
        url: 'schedule',         /* Куда отправить запрос */
        method: 'get',             /* Метод запроса (post или get) */
        dataType: 'html',          /* Тип данных в ответе (xml, json, script, html). */
        data: $(this).serialize(),     /* Данные передаваемые в массиве */
        context: $('film'),     /* Данные передаваемые в массиве */
        success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
             //alert(data); /* В переменной data содержится ответ от index.php. */
            $('.film').html(data)
            $('.info__time').each(function () {
                $(this).find('.info__descr').hide()

            })
            $('.info__time').hover(function () {
                $(this).find('.info__descr').fadeToggle('slow')
            })
        }
    });
 })


