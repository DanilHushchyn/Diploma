function bytesToSize(bytes) {
   var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
   if (bytes == 0) return '0 Byte';
   var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
   return Math.round(bytes / Math.pow(1024, i)) + ' ' + sizes[i];
}
export function upload(selector,options) {
    $(selector).each(function () {
        // Подготовка интерфейса
        let btnOpen = $('<button class="btn btn-primary choose-file-btn" type="button"><i class="fa-regular fa-image fa-xl p-3"></i></button>')
        $(this).before(btnOpen)
        $(btnOpen).on('click', function () {
            $(this).siblings('input[type=\'file\']').click()
        })

        let preview = $('<div class="preview d-flex flex-wrap justify-content-center"></div>');
        $(this).before(preview)
        $(this).hide()
    })
    if (options.update===true) {
        $(selector).each(function () {
            // Подготовка данных и инициализации FileList
            $(selector + '-data').each(async function () {
                let path = $(this).data('path');
                let name = String(path).split('/')[String(path).split('/').length-1]
                const srcToFile = async (src, fileName) => {
                    const response = await axios.get(src, {
                        responseType: "blob",
                    });
                    const mimeType = response.headers["content-type"];
                    return new File([response.data], fileName, {type: mimeType});
                };
                let file = await srcToFile(path, name)
                $(selector).siblings('.preview').append(`
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
                    $(this).closest('.preview__item').remove()

                })
            })

        })
    }

    function UploadFunction() {

        $(selector).on('change', function () {
            let inputElem = $(this)
            let preview = inputElem.siblings('.preview')
            // const file = this.files[0];
            preview.empty()
            for (let file of this.files) {
                let reader = new FileReader();
                reader.onload = function (event) {

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

                    $('.preview__del').on('click', function (event) {
                        let inputFile = $(this).closest('.preview').siblings(selector)
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
            }

        })
    }
    UploadFunction()

}
