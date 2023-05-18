let topCarouselTotal = $('#id_top_carousel-TOTAL_FORMS')
let topCarouselInitial = $('#id_top_carousel-INITIAL_FORMS')
let bottomCarouselTotal = $('#id_bottom_carousel-TOTAL_FORMS')

$('.card__item_add').on('click',function () {
    let newForm;
    if ($(this).attr('name') === 'top'){

        newForm = $(`
       <div class='card__item mr-5 mb-5'> 
           <button type='button' class='btn card__btn card__btn_add btn-primary mb-3'> <i class="fa-regular fa-image fa-xl p-3"></i> </button>
            <input type="file" name="top_carousel-${topCarouselTotal.val()}-img" class="form__horizontal-img mb-3" accept="image/*" id="id_top_carousel-${topCarouselTotal.val()}-img">
            <input type="url" name="top_carousel-${topCarouselTotal.val()}-link"  class="form__elem mb-2" placeholder="${linkLabel}" maxlength="200" id="id_top_carousel-${topCarouselTotal.val()}-link">
            
            <div class="mb-1">
                <label class="form-label" for="id_top_carousel-${topCarouselTotal.val()}-title_ru"> [ru]</label>
                <input type="text" name="top_carousel-${topCarouselTotal.val()}-title_ru"   class="form-control form__elem" placeholder="${titleLabel}" maxlength="50" id="id_top_carousel-${topCarouselTotal.val()}-title_ru">
            </div>
            
            <div class="mb-3">
                <label class="form-label" for="id_top_carousel-${topCarouselTotal.val()}-title_en"> [en]</label>
                <input type="text" name="top_carousel-${topCarouselTotal.val()}-title_en" class="form-control form__elem" placeholder="${titleLabel}" maxlength="50" id="id_top_carousel-${topCarouselTotal.val()}-title_en">
           </div>
           <input type="hidden" name="top_carousel-${topCarouselTotal.val()}-id"  id="id_top_carousel-${topCarouselTotal.val()}-id">
           <div type='button' class="btn card__btn card__btn_remove bg-danger w-auto"><i class="fa-solid fa-trash-can fa-xl p-3"></i></div>

       </div>

    `)
               topCarouselTotal.val(Number(topCarouselTotal.val())+1);

    }else{

    newForm =  $(`
       <div class='card__item  mr-5 mb-5'> 
           <button type='button' class='btn card__btn card__btn_add btn-primary mb-3'> <i class="fa-regular fa-image fa-xl p-3"></i> </button>
           <input type="file" name="bottom_carousel-${bottomCarouselTotal.val()}-img" class="form__horizontal-img mb-3" accept="image/*" id="id_bottom_carousel-${bottomCarouselTotal.val()}-img">
           <input type="url" name="bottom_carousel-${bottomCarouselTotal.val()}-link"  class="form__elem mb-3 " placeholder="${linkLabel}" maxlength="200" id="id_bottom_carousel-${bottomCarouselTotal.val()}-link">
           <input type="hidden" name="bottom_carousel-${bottomCarouselTotal.val()}-id"  id="id_bottom_carousel-${bottomCarouselTotal.val()}-id">
           <div type='button' class="btn card__btn card__btn_remove bg-danger w-auto"><i class="fa-solid fa-trash-can fa-xl p-3"></i></div>

       </div>
    `)
            bottomCarouselTotal.val(Number(bottomCarouselTotal.val())+1);

    }

    $(this).before(newForm)
})


$("[name$='DELETE'], [for$='DELETE']").hide()
$('body').on('click','.card__btn_remove',function () {
    $(this).parent().find('[name$=\'DELETE\']').attr('checked','checked')
    $(this).parent().fadeOut("slow", function() {

  })

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

