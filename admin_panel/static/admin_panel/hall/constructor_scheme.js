$('.hall').on('click','.hall__item',function (event) {
    $(event.target).toggleClass('hall__seat')
    $(event.target).parent().toggleClass('hall__row_')
})

$('#calc-scheme').on('click',function (event) {
    $('.hall__row').each(function (index,value){
        $(value).children('.hall__seat').each(function (index,value) {
            $(value).html(index+1)
        })
    })
    $('.scheme_html').val($('.hall').html())
})

var row_number = 1
$('#add-row').on('click',function (event) {
    let newElement = $(`
        <div class="hall__row" data-number = ${row_number}>
          <div class="hall__item"></div>
          <div class="hall__item"></div>
          <div class="hall__item"></div>
          <div class="hall__item"></div>
          <div class="hall__item "></div>
          <div class="hall__item "></div>
          <div class="hall__item "></div>
          <div class="hall__item " ></div>
          <div class="hall__item "></div>
          <div class="hall__item "></div>
          <div class="hall__item "></div>
          <div class="hall__item "></div>
          <div class="hall__item "></div>
          <div class="hall__item "></div>
          <div class="hall__item "></div>
        </div>
    `)
    row_number += 1
    $('.hall').append(newElement)

})

$('#del-row').on('click',function (event) {
    $('.hall').children().last().remove()
})