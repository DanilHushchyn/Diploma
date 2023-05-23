export function upload(selector,options){

    let preview = document.createElement('div');
    preview.classList.add('preview');
    let inputFile = document.querySelector(selector);


    inputFile.setAttribute('accept','.html')



    inputFile.addEventListener('change',(event)=>{

       preview.innerHTML = '';
       let files = Array.from(event.target.files);
       files.forEach((file, index, array)=>{
           if(file.type.match('text/html')){
               let reader = new FileReader();
               reader.addEventListener('load',(event)=>{
                   preview.insertAdjacentHTML('afterbegin', `
                     <div class="preview__item">
                           ${updloadedTemplateLabel}: <span>${file.name}</span>
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
    btnOpen.innerHTML = updloadTemplateLabel;
    btnOpen.classList.add('btn','btn-primary','form__btn');
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

    inputFile.parentElement.after(preview);

    btnOpen.addEventListener('click',(event)=>{
         // перенаправляем клик с нашей красивой кнопки на дэфолтный инпут
        // и по умолчанию получаем проводник для выбора файла
          inputFile.click()

    })


}