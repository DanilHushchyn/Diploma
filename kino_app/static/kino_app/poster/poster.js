$('.content__btn_afisha','.content').on('click',function (event) {
    $('.afisha').slideDown("slow")
    $('.soon').slideUp("slow")
})
$('.content__btn_soon','.content').on('click',function (event) {
    $('.soon').slideDown("slow")
    $('.afisha').slideUp("slow")
})