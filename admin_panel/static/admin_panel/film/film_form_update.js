import {upload} from "../../js/upload.js";

upload('.form__horizontal-img',{
    multiple: false,
    accept: ['.png','.jpg','.jpeg','.svg']
})
upload('.form__vertical-img',{
    multiple: false,
    accept: ['.png','.jpg','.jpeg','.svg']
})