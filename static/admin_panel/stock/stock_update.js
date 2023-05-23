import {upload} from "../../js/upload_new.js";
upload('#banner-img',{
    accept: ['.png','.jpg','.jpeg','.svg'],
            update: true,

})
upload('#card-img',{
    accept: ['.png','.jpg','.jpeg','.svg'],
            update: true,

})

// upload('.gallery',{
//    accept: ['.png','.jpg','.jpeg','.svg'],
//             update: true,
//
// })

$('.on_off').parent().hide()
if($('.on_off').is(':checked')){
    $('input[role=\'switch\']').attr('checked',true)
}

$('input[role=\'switch\']').on('click',function () {
    if ($(this).is(':checked')){
        $('.on_off').attr('checked',true)

    }else{
        $('.on_off').attr('checked',false)


    }

})