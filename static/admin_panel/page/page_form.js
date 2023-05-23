import {upload} from "../../js/upload_new.js";

upload('#pic1',{
    accept: ['.png','.jpg','.jpeg','.svg']
})
upload('#pic2',{
    accept: ['.png','.jpg','.jpeg','.svg']
})
upload('#pic3',{
    accept: ['.png','.jpg','.jpeg','.svg']
})
upload('#banner-img',{
    accept: ['.png','.jpg','.jpeg','.svg']
})
// upload('.gallery',{
//     accept: ['.png','.jpg','.jpeg','.svg']
// })



$('.on_off').parent().hide()

$('input[role=\'switch\']').on('click',function () {
    if ($(this).is(':checked')){
        $('.on_off').attr('checked',true)

    }else{
        $('.on_off').attr('checked',false)


    }

})