function bytesToSize(bytes) {
   var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
   if (bytes == 0) return '0 Byte';
   var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
   return Math.round(bytes / Math.pow(1024, i)) + ' ' + sizes[i];
}
export function upload(selector,options){
    let preview = document.createElement('div');
    preview.classList.add('preview');
    let inputFile = document.querySelector(selector);
    if (options.multiple){
        inputFile.setAttribute('multiple',true);
    }
    if (options.accept && Array.isArray(options.accept)){
        inputFile.setAttribute('accept',options.accept.join(','))
    }


    inputFile.addEventListener('change',(event)=>{
       preview.innerHTML = '';
       let files = Array.from(event.target.files);
       files.forEach((file, index, array)=>{
           if(file.type.match('image')){

               let reader = new FileReader();
               reader.addEventListener('load',(event)=>{
                   let classImg = 'preview__img-horizontal'
                   if ('form__vertical-img' == inputFile.classList){
                       classImg =  'preview__img-vertical'
                   }
                   let url = reader.result;// получили адрес загруженной картинки
                   preview.insertAdjacentHTML('afterbegin', `
                     <div class="preview__item">
                        <div class="preview__del"><img src="${urlImgRemove}" data-name="${file.name}" alt=""></div>
                        
                        <img class="${classImg}" src="${url}" alt="${file.name}"/>
                        <div class="preview__info">
                            <span>${file.name}</span>
                            <span>${bytesToSize(file.size)}</span>
                        </div>
                     </div>
                    `);
               });
               // так как операция асинхронная мы её должны делать строго
               // после события load которое сейчас выше расположено
               reader.readAsDataURL(file); // читаем файл и получаем в результате url файла
           }
           return
       })
    });
    /**
     *  opacity используется для скрытия ввода файла вместо visibility: hiddenили
     *  display: none, потому что вспомогательные технологии интерпретируют последние
     *  два стиля как означающие, что ввод файла не является интерактивным.
     */
    inputFile.style.display = 'none';

    let btnOpen = document.createElement('button');
    btnOpen.innerHTML = 'Открыть';
    btnOpen.classList.add('btn-primary','form__btn');
    btnOpen.type = 'button';
    inputFile.before(btnOpen);
    /**
     * У наc есть картинка значок 'закрыть preview'
     * а у браузера есть по умолчанию событие dragstart
     * которое позволяет эти картинки перетаскивать что не красиво
     * чтобы это исключить надо отключить событие ondragstart
     */
    preview.ondragstart=function (){
        return false
    }
    preview.addEventListener('click',(event)=>{
        if ( event.target.closest('.preview__del')) {
            let block = event.target.closest('.preview__item');
            block.classList.add('removing'); // специальная анимация для красивого удаления картинки
            // чтобы анимация успела отработать до удаления делаем паузу на время анимации
            setTimeout(() => block.remove(), 300);
            let files = inputFile.files;
            let name = event.target.dataset.name;
            /**
             * Обычный массив тут не поможет только DataTransfer
             *
             * DataTransfer
             * нужен для того чтобы перезаписать в него отфильтрованный
             * псевдомассив и переприсвоить
             * содержимое свойству files нашего инпута
             */
            const dt = new DataTransfer();
            for (let i = 0; i < files.length; i++) {
                if (files[i].name !== name) { // фильтруем элемент который надо удалить
                    dt.items.add(files[i])
                }
            }
            inputFile.files = dt.files; // присваиваем отфильтрованную коллекцию
        }
    });
    inputFile.parentElement.after(preview);

    btnOpen.addEventListener('click',(event)=>{
         // перенаправляем клик с нашей красивой кнопки на дэфолтный инпут
        // и по умолчанию получаем проводник для выбора файла
          inputFile.click()

    })


}