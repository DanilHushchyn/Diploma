import {upload} from "./upload_html.js";
upload('.file-html',{
    multiple: false,
    accept: ['.html']
})
$('.card__list').hide()

$('#selected_clients').on('change',function () {
    if ($(this).attr('checked',true)){
        $('.card__btn').css({
            display: 'block'
        })
    }

})
$('#all_clients').on('change',function () {
    if ($(this).attr('checked',true)){
        $('.card__btn').css({
            display: 'none'
        })
    }

})
$('.file-html').attr('required',false)
$("input[name='template']").on('change',function () {
    if ($(this).attr('id')==='new_template'){
        $('.card__file').css({
            display: 'flex'
        })
        $('.card__list').css({
            display: 'none'
        })
    }else{
        $('.card__file').css({
            display: 'none'
        })
        $('.card__list').css({
            display: 'flex'
        })
    }

})