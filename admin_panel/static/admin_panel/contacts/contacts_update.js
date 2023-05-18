import {bytesToSize} from "../../js/upload.js";
let contactsTotal = $('#id_form-TOTAL_FORMS')
$("[name$='DELETE'], [for$='DELETE']").hide()
$('.form__horizontal-img').each(function () {
    let btnOpen = $('<button class="btn btn-primary choose-file-btn" type="button"><i class="fa-regular fa-image fa-xl p-3"></i></button>')
    $(this).before(btnOpen)
    let preview = $('<div class="preview d-flex flex-wrap justify-content-center"></div>');

    $(this).before(preview)
    $(this).hide()
})
$('.form__horizontal-img').each(async function () {
    let path = $(this).closest('.card-body').find('.logo-data').data('path');
    // let name = $(this).closest('.card-body').find('.logo-data').data('name');
    // let size = $(this).closest('.card-body').find('.logo-data').data('size');
    const srcToFile = async (src, fileName) => {
        const response = await axios.get(src, {
            responseType: "blob",
        });
        const mimeType = response.headers["content-type"];
        return new File([response.data], fileName, {type: mimeType});
    };
    // let datr = new DataTransfer()
    // datr.items.add(await srcToFile(path, name));
    // $(this).prop('files', datr.files)
    let name = String(path).split('/')[String(path).split('/').length-1]
    let file = await srcToFile(path, name)

    $(this).siblings('.preview').append(`
        <div class="preview__item d-inline position-relative text-center mt-3" style="width: 12rem" >
            <div class="preview__del text-danger" style="cursor:pointer;">
                <svg data-name="${name}"  xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                </svg>
            </div>
            <img class="img-fluid" style="width: 12rem" src="${path}" alt="${name}"/>
            <div className="preview__info d-flex  flex-column position-absolute bottom-0 start-0">
               <span>${bytesToSize(file.size)}</span>
            </div>
         </div>
    `)
    $('.preview__del').on('click', function (event) {
        // let inputFile = $(this).closest('.preview').siblings('.form__horizontal-img')
        // const dt = new DataTransfer();
        // let name = $(this).find('svg').data('name')
        // for (let i = 0; i < inputFile.prop('files').length; i++) {
        //     if (inputFile.prop('files')[i].name !== name) { // фильтруем элемент который надо удалить
        //         dt.items.add(inputFile.prop('files')[i])
        //     }
        // }
        // inputFile.prop('files', dt.files)  // присваиваем отфильтрованную коллекцию
        $(this).closest('.preview__item').remove()

    })
    $(this).closest('.card-body').find('.logo-data').remove()
    // let reader = new FileReader();

})
function UploadFunction() {
    $('.choose-file-btn').on('click', function () {
        $(this).siblings().click()
    })
    $('.form__horizontal-img').on('change', function () {
        let inputElem = $(this)
        let preview = inputElem.siblings('.preview')
        const file = this.files[0];
        let reader = new FileReader();
        reader.onload = function (event) {
            // let preview = $('<div class="preview d-flex flex-wrap justify-content-center"></div>');
            preview.empty()
            if (inputElem.hasClass('form__horizontal-img')) {
                preview.append($(`
                      <div class="preview__item d-inline position-relative text-center mt-3" style="width: 12rem" >
                        <div class="preview__del text-danger" style="cursor:pointer;">
                            <svg data-name="${file.name}"  xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                              <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                            </svg>
                        </div>           
                        <img class="img-fluid" style="width: 12rem" src="${event.target.result}" alt="${file.name}"/>                        
                        <div className="preview__info d-flex  flex-column position-absolute bottom-0 start-0">
                           <span>${bytesToSize(file.size)}</span>
                        </div>             
                     </div>
             `))
            }

            $('.preview__del').on('click', function (event) {
                let inputFile = $(this).closest('.preview').siblings('.form__horizontal-img')
                const dt = new DataTransfer();
                let name = $(this).find('svg').data('name')
                for (let i = 0; i < inputFile.prop('files').length; i++) {
                    if (inputFile.prop('files')[i].name !== name) { // фильтруем элемент который надо удалить
                        dt.items.add(inputFile.prop('files')[i])
                    }
                }
                inputFile.prop('files', dt.files)  // присваиваем отфильтрованную коллекцию
                $(this).closest('.preview__item').remove()

            })
        }
        reader.readAsDataURL(file);

    })
    $('button[title="Remove"]').on('click',function () {
        $(this).closest('.card').find('[name$=\'DELETE\']').attr('checked',true)
        $(this).closest('.card').fadeOut("slow", function() {
        })
    })
}
UploadFunction()

$('.btn-add-contact').on('click',function () {
    let newForm = $(`
    <div class="card">
        <div class="card-header">
              <div class="card-tools p-2">
                <button type="button" class="btn btn-tool" data-card-widget="remove" title="Remove">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                      <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"></path>
                    </svg>
                </button>
              </div>
        </div>
        <div class="card-body ">
            <div class="row mb-3">
                <label class="col-sm-2 col-form-label" for="id_form-${contactsTotal.val()}-name_ru">${title} [ru]</label>
                <div class="col-sm-10">
                    <input type="text" name="form-${contactsTotal.val()}-name_ru"  maxlength="100" class="form-control form-control-sm" placeholder="${title} [ru]" id="id_form-${contactsTotal.val()}-name_ru">
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-2 col-form-label" for="id_form-${contactsTotal.val()}-name_en">${title} [en]</label>
                <div class="col-sm-10">
                    <input type="text" name="form-${contactsTotal.val()}-name_en"  maxlength="100" class="form-control form-control-sm" placeholder="${title} [en]" id="id_form-${contactsTotal.val()}-name_en">
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-2 col-form-label" for="id_form-${contactsTotal.val()}-address_ru">${address} [ru]</label>
                <div class="col-sm-10">
                <textarea name="form-${contactsTotal.val()}-address_ru" cols="40" rows="10" class="form-control form-control-sm" placeholder="${address} [ru]" id="id_form-${contactsTotal.val()}-address_ru"></textarea>
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-2 col-form-label" for="id_form-${contactsTotal.val()}-address_en">${address} [en]</label>
                <div class="col-sm-10">
                <textarea name="form-${contactsTotal.val()}-address_en" cols="40" rows="10" class="form-control form-control-sm" placeholder="${address} [en]" id="id_form-${contactsTotal.val()}-address_en"></textarea>
                </div>
            </div>
           
            <div class="row mb-3">
                <label class="col-sm-2 col-form-label" for="id_form-${contactsTotal.val()}-coordinate">${coordinateLabel}</label>
                <div class="col-sm-10">
                    <textarea name="form-${contactsTotal.val()}-coordinate" cols="40" rows="10" maxlength="10000" class="form-control form-control-sm" placeholder="${coordinateLabel}" id="id_form-${contactsTotal.val()}-coordinate"></textarea>
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-2 col-form-label" for="id_form-${contactsTotal.val()}-logo">${logoLabel}</label>
                <div class="col-sm-10">
                <button class="btn btn-primary choose-file-btn" type="button"><i class="fa-regular fa-image fa-xl p-3"></i></button>
                <div class="preview d-flex flex-wrap justify-content-center"></div>
                <input type="file" name="form-${contactsTotal.val()}-logo" class="form-control form__horizontal-img form-control-sm" accept="image/*" id="id_form-${contactsTotal.val()}-logo" style="display: none;">
                </div>
            </div>
            <input type="hidden" name="form-${contactsTotal.val()}-id" id="id_form-${contactsTotal.val()}-id">
            <div class="row mb-3">
                <div class="col-sm-10 offset-sm-2">
                <div class="form-check">
                <input type="checkbox" name="form-${contactsTotal.val()}-DELETE" class="form-check-input" id="id_form-${contactsTotal.val()}-DELETE" style="display: none;">
                <label class="form-check-label" for="id_form-${contactsTotal.val()}-DELETE" style="display: none;">Удалить</label>
                </div>
                </div>
            </div>
        </div>
        <div class="card-footer">
        </div>
    </div>
    `)
    $('.form-collection').append(newForm)
    UploadFunction()
    contactsTotal.val(Number(contactsTotal.val())+1);

})
