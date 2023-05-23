
$('.content__btn_soon').on('click',function () {
     $(".film").fadeToggle('slow',function () {
         $.ajax({
             url: 'poster_soon_ajax',         /* Куда отправить запрос */
             method: 'get',             /* Метод запроса (post или get) */
             dataType: 'html',
             data: {'page': 'soon'},
             context: $('.film'),     /* Данные передаваемые в массиве */
             success: function (data) {
                 $(this).html(data);
                 $(".film").fadeToggle('slow')

             }
         });
     })


 })
$('.content__btn_afisha').on('click',function () {

    $(".film").fadeToggle('slow',function () {
        $.ajax({
            url: 'poster_soon_ajax',
            method: 'get',
            dataType: 'html',
            data: {'page': 'poster'},
            context: $('.film'),
            success: function (data) {
                $(this).html(data);
                $(".film").fadeToggle('slow')

            }
        });
    })

 })