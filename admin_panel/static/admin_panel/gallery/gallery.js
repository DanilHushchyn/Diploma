let carouselTotalForms = $('#id_form-TOTAL_FORMS')
$(".card__item").each(function () {
    $(this).children().removeClass('mb-3')
})
$('.gallery').parent().hide()
$('.card__item_add').on('click',function () {
    let newForm;
    newForm = $(`
       <div class="card__item mb-2 d-flex flex-column justify-content-center">
         <img class="card__preview card__preview_horizontal img-fluid" src="/static/kino_app/imgs/placeholderimg.png" style="width: 12rem;height: auto" alt="">
         <button type="button" class="btn card__btn card__btn_change btn-primary mb-3">  <i class="fa-regular fa-image fa-xl p-3"></i> </button>
         <div class="mb-3">
             <input type="file" name="form-${carouselTotalForms.val()}-img" class="form-control gallery d-none" multiple="" accept="image/*" id="id_form-${carouselTotalForms.val()}-img">
         </div>
             <input type="hidden" name="form-${carouselTotalForms.val()}-id" id="id_form-${carouselTotalForms.val()}-id">
         <div class="">
             <div class="form-check d-none">
                <input type="checkbox" name="form-${carouselTotalForms.val()}-DELETE" class="form-check-input" id="id_form-${carouselTotalForms.val()}-DELETE">
                <label class="form-check-label " for="id_form-${carouselTotalForms.val()}-DELETE">Удалить</label>
             </div>
         </div>
           <div type='button' class="btn card__btn card__btn_remove bg-danger w-auto"><i class="fa-solid fa-trash-can fa-xl p-3"></i></div>
       </div>
    `)
    carouselTotalForms.val(Number(carouselTotalForms.val())+1);

    $(this).before(newForm)

    $('.card__btn_change').off('click')
    $('.card__btn_change').on('click',function () {
    let preview = $(this).parent().find('.card__preview_horizontal')
    let inputChangedFile = $(this).parent().find('input[type=\'file\']').click()
    $(inputChangedFile).on('change',function () {
        const file = this.files[0];
        let reader = new FileReader();
          reader.onload = function(event){
              preview.attr('src',event.target.result)
          }
          reader.readAsDataURL(file);
    })
    })
})


$("[name$='DELETE'], [for$='DELETE']").hide()
$('body').on('click','.card__btn_remove',function () {
    $(this).parent().find('[name$=\'DELETE\']').attr('checked','checked')
    $(this).parent().hide()
    $(this).parent().removeClass('d-flex')

})

$('body').on('click','.card__btn_add',function () {
    // $(this).next().find('[name$=\'img\']').click()
    $(this).siblings('[name$=\'img\']').click()
})
$('body').on('change','.form__horizontal-img, .form__vertical-img',function () {
      let inputElem = $(this)
      const file = this.files[0];
      let reader = new FileReader();
      reader.onload = function(event){
        let preview;
        if (inputElem.hasClass('form__horizontal-img') ) {
             preview = $(`<img class=" card__preview card__preview_horizontal mb-3 img-fluid" src="${event.target.result}"/>`)
        }else{
             preview = $(`<img class="card__preview card__preview_vertical mb-3 img-fluid" src="${event.target.result}"/>`)

        }
         inputElem.siblings('.card__btn_add').replaceWith(preview)
      }
      reader.readAsDataURL(file);

})
var addPicBtn;
$('.card__preview').each(function () {
    if ($(this).attr('src') ==='/media/None') {
        addPicBtn = $(`<button type=\'button\' class=\'btn card__btn card__btn_add btn-primary\'> Выбрать картинку </button>`)
        $(this).replaceWith(addPicBtn)
    }
});


$('.card__btn_change').on('click',function () {
    let preview = $(this).parent().find('.card__preview_horizontal')
    let inputChangedFile = $(this).parent().find('input[type=\'file\']').click()
    $(inputChangedFile).on('change',function () {
        const file = this.files[0];
        let reader = new FileReader();
          reader.onload = function(event){
              preview.attr('src',event.target.result)
          }
          reader.readAsDataURL(file);
    })
})

