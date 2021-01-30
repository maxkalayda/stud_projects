function loginBtnOnClicked(){
    if (document.querySelector(`input[name='inputPassword']`).value == "" || document.querySelector(`input[name='inputEmail']`).value == ""){
        while (document.querySelector('#mainContainer > div > div > div[role="alert"]'))
            document.querySelector('#mainContainer > div > div > div[role="alert"]').remove();
        var inthml = `<div class="row alert alert-danger border border-secondary m-0 my-1 p-0" role="alert">
                            <div class="col-12">
                                Поля не должны быть пустыми!
                                <button type="button" class="close" data-dismiss="alert" aria-label="Закрыть"><i class="fas fa-times"></i></button>
                            </div>
                        </div>`
        document.querySelector('#mainContainer > div > div').insertAdjacentHTML('afterbegin', inthml);
    }
    else {
        document.theForm.submit();
    }
};

window.onload = function() {
    console.log("JS is fully loaded!");
};