export function bytesToSize(bytes) {
   var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
   if (bytes == 0) return '0 Byte';
   var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
   return Math.round(bytes / Math.pow(1024, i)) + ' ' + sizes[i];
}
export function upload(selector,options){

    let preview = document.createElement('div');
    preview.classList.add('preview','d-flex' ,'flex-wrap' ,'justify-content-center');
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
                     <div class="preview__item d-inline position-relative text-center mt-3" style="width: 12rem" >
                        <div class="preview__del  text-danger" style="cursor:pointer;">
                            <svg data-name="${file.name}"  xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16">
                              <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                            </svg>
                        </div>           
                        <img class="img-fluid" style="width: 12rem" src="${url}" alt="${file.name}"/>                        
                        <div className="preview__info d-flex  flex-column position-absolute bottom-0 start-0">
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
     *  opacity используется для скрытия ввода файла вместо visibility: hidden или
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