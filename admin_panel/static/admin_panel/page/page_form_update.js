import {upload} from "../../js/upload_new.js";

upload('#pic1',{
    accept: ['.png','.jpg','.jpeg','.svg'],
            update: true,
})
upload('#pic2',{
    accept: ['.png','.jpg','.jpeg','.svg'],
            update: true,

})
upload('#pic3',{
    accept: ['.png','.jpg','.jpeg','.svg'],
            update: true,

})
upload('#banner-img',{
    accept: ['.png','.jpg','.jpeg','.svg'],
            update: true,

})
// upload('.gallery',{
//     accept: ['.png','.jpg','.jpeg','.svg'],
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