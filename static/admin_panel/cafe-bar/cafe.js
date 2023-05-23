let cafeTotalForms = $('#id_menu-TOTAL_FORMS')

$('.btn-add').on('click',function (event) {
    let newRow = $(`
       <tr class="menu-form" data-widget="expandable-table" aria-expanded="true">
           <td><input type="text" name="menu-${cafeTotalForms.val()}-name_ru"  maxlength="150" id="id_menu-${cafeTotalForms.val()}-name_ru"></td>  
           <td><input type="text" name="menu-${cafeTotalForms.val()}-name_en"  maxlength="150" id="id_menu-${cafeTotalForms.val()}-name_en"></td>         
           <td><input type="number" name="menu-${cafeTotalForms.val()}-weight" min="0" id="id_menu-${cafeTotalForms.val()}-weight"></td>
           <td><input type="number" name="menu-${cafeTotalForms.val()}-price" min="0" id="id_menu-${cafeTotalForms.val()}-price"></td>                        
           <input type="hidden" name="menu-${cafeTotalForms.val()}-id" id="id_menu-${cafeTotalForms.val()}-id">
           <td>
               <input type="checkbox" name="menu-${cafeTotalForms.val()}-DELETE" id="id_menu-${cafeTotalForms.val()}-DELETE" hidden>
                <a class="btn-remove">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                      <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                    </svg>
                </a>
           </td>
       </tr>
    `)

    cafeTotalForms.val(Number(cafeTotalForms.val())+1)
    $('.table').append(newRow)
})

$("[name$='DELETE'], [for$='DELETE']").hide()
$('.table').on('click','.btn-remove',function (event) {
    $(this).siblings('[name$=\'DELETE\']').attr('checked','checked')
    $(this).parents("tr:first").fadeOut("slow", function() {
    // Animation complete.
  })

})