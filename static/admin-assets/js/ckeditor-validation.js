
// validation for empty field
jQuery.validator.addMethod("ckrequired", function (value, element) {  
    var idname = $(element).attr('id');  
    var editor = CKEDITOR.instances[idname];  
    var ckValue = GetTextFromHtml(editor.getData()).replace(/<[^>]*>/gi, '').trim();
    if (ckValue.length === 0 ) {    
        $(element).val(ckValue);
    }else {  
        $(element).val(editor.getData());
    }
    return $(element).val().length > 0;
}, "Please enter description");  

// validation for min length of 100 characters
jQuery.validator.addMethod("ckmin", function (value, element) {  
    var idname = $(element).attr('id');  
    var editor = CKEDITOR.instances[idname];  
    var ckValue = GetTextFromHtml(editor.getData()).replace(/<[^>]*>/gi, '').trim();
    if (ckValue.length < 100 ) {    
        $(element).val(ckValue);
    }else {  
        $(element).val(editor.getData());  
    }
    return $(element).val().length > 100;
}, "Minimum Characters length should be 100");  

// validation for max length of 800 Characters
jQuery.validator.addMethod("ckmax", function (value, element) {  
    var idname = $(element).attr('id');  
    var editor = CKEDITOR.instances[idname];  
    var ckValue = GetTextFromHtml(editor.getData()).replace(/<[^>]*>/gi, '').trim();
    if (ckValue.length > 800 ) {    
        $(element).val(ckValue);
    }else {  
        $(element).val(editor.getData());  
    }
    return $(element).val().length < 800;
}, "Maximum length should not exceed 800 characters");  

// validation for alowing only few special characters 
jQuery.validator.addMethod("ckspecial", function( value, element ) {
    var idname = $(element).attr('id');  
    var editor = CKEDITOR.instances[idname];  
    var ckValue = GetTextFromHtml(editor.getData()).replace(/<[^>]*>/gi, '').trim();
    var regex = new RegExp("^[ A-Za-z0-9_.,\'/-]*$");
    var key = ckValue;
    if (!regex.test(key)) {
        return false;
    }
    return true;
}, "Only Few special characters are allowed");


// validation for allowing only characters 
jQuery.validator.addMethod("ckcharonly", function( value, element ) {
    var idname = $(element).attr('id');  
    var editor = CKEDITOR.instances[idname];  
    var ckValue = GetTextFromHtml(editor.getData()).replace(/<[^>]*>/gi, '').trim();
    var regex = new RegExp("^[A-Za-z]*$");
    var key = ckValue;
    if (!regex.test(key)) {
        return false;
    }
    return true;
}, "Only characters are allowed");


function GetTextFromHtml(html) {  
    var dv = document.createElement("DIV");  
    dv.innerHTML = html;  
    return dv.textContent || dv.innerText || "";  
}