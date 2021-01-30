otherInfoElements = document.querySelectorAll(`.OtherInfo`);
otherInfocCheckbox = document.querySelector(`input[name='OtherInfo']`);

inputElemsByMaterialInt = document.querySelectorAll(`#supliersSearchByMaterial > div > form > div > input[typeOfData='integer']`);
inputElemsByMaterialStr = document.querySelectorAll(`#supliersSearchByMaterial > div > form > div > input[typeOfData='string']`); // MaterialNameElem = inputElemsByMaterialStr[0].value
inputElemsByBankInt = document.querySelectorAll(`#supliersSearchByBank > div > form > div > input[typeOfData='integer']`);
inputElemsByBankStr = document.querySelectorAll(`#supliersSearchByBank > div > form > div > input[typeOfData='string']`);
inputElemsAddInt = document.querySelectorAll(`#supliersAddDelete > div > form > div > input[typeOfData='integer']`);
inputElemsAddStr = document.querySelectorAll(`#supliersAddDelete > div > form > div > input[typeOfData='string']`);

function SendReq(arr, action) {

    let result = document.querySelector('.scroll-area>table>tbody');
    let objectBuff, objectBuffkeys;

    if (action == "SearchByMaterial"){
        objectBuff = {"material_name": NaN, "measure_unit_name": NaN, "material_code": NaN, "class_code": NaN,
                        "group_code": NaN, "measure_unit_code": NaN};
    } else if (action == "SearchByBank"){
        objectBuff = {"city": NaN, "street": NaN, "index": NaN, "building": NaN};
    } else if (action == "Add" || action == "Delete"){
        objectBuff = {"sup_name": NaN, "org_address": NaN, "bank_address": NaN, "inn_code": NaN, "bank_acc": NaN};
    }
    objectBuffkeys = Object.keys(objectBuff);
    for (var i = 0; i < arr.length; i++){
        objectBuff[objectBuffkeys[i]] = arr[i];
    }

    let req = new XMLHttpRequest();
    req.open("POST", `/logistician/${action}`);
    req.setRequestHeader("Content-Type", "application/json"); 
    req.onreadystatechange = function () { 
        if (req.readyState === 4 && req.status === 200) { 
            var res = JSON.parse(this.responseText);
            var msg = 0;
            if (action == "SearchByMaterial"){
                while (result.firstChild)
                        result.firstChild.remove();
                for (var i = 0; i < res.length; i++){
                    var inhtml = `<tr>
                                    <td>${res[i][0]}</td>
                                    <td>${res[i][1]}</td>
                                    <td>${res[i][2]}</td>
                                    <td>${res[i][3]}</td>
                                    <td>${res[i][4]}</td>
                                    <td>${res[i][5]}</td>
                                </tr>`;
                    result.insertAdjacentHTML('beforeend', inhtml);
                    ++msg;
                }
                msg = "Найдено результатов: " + msg;
            } else if (action == "SearchByBank"){
                msg = "Найдено результатов: " + res["sum"];
            }
            else if (action == "Add" || action == "Delete"){
                msg = "Результат: " + res["res"];
                action = "AddDelete"
            }
            while (document.querySelector(`#supliers${action} ~ .alert`))
                document.querySelector(`#supliers${action} ~ .alert`).remove();
            var inthml = `<div class="row alert alert-info border border-secondary m-0 my-2" role="alert">
                                <div class="col-12">
                                    ${msg}
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Закрыть"><i class="fas fa-times"></i></button>
                                </div>
                            </div>`
            document.querySelector(`#supliers${action}`).insertAdjacentHTML('afterend', inthml);
        } 
    };
    var data = JSON.stringify(objectBuff); 
    req.send(data);
}

function OnInputChange(elem){
    OKflag = true;

    while (elem.nextSibling)
        elem.nextSibling.remove();

    if (elem.value == "") return OKflag;

    var inputsDictionary = {"MaterialName":"string", "MaterialCode":"integer", "MaterialClassCode":"integer",
                            "MaterialGroupCode":"integer", "MaterialUnitCode":"integer", "MaterialUnit":"string",
                             "Index":"integer", "City":"string", "Street":"string", "Building":"integer",
                             "SupName":"string", "InnCode":"integer", "OrgAddress":"string", "BankAddress":"string", "BankAcc":"integer"};
    var name = inputsDictionary[elem.getAttribute("name")];
    var pInt = parseInt(elem.value);
    var pIntLen = (pInt).toString().length
    var elemValLen = (elem.value).toString().length
    if (((isNaN(pInt) == true && name == "integer") || (pIntLen != elemValLen && name == "integer") ||
        ((isNaN(pInt) == false && name == "string" && pIntLen == elemValLen)))){
        var err = "Неверный ввод! " + ((isNaN(pInt) == true) ? "Введите число!" : (pIntLen != elemValLen) ? "Введите число!" : "Введите текст!");
        err = `<div class="row alert alert-danger border border-secondary m-0 my-1 p-0" role="alert">
                    <div class="col-12">
                        ${err}
                        <button type="button" class="close" data-dismiss="alert" aria-label="Закрыть"><i class="fas fa-times"></i></button>
                    </div>
                </div>`
        elem.insertAdjacentHTML('afterend', err);
        OKflag = false;
    }
    return OKflag;
};

function OtherInfoOnChecked(){
    if (otherInfocCheckbox.checked == true) {
        for (var i = 0; i < otherInfoElements.length; i++) {
            otherInfoElements[i].disabled = false;
        }
    }
    else {
        for (var i = 0; i < otherInfoElements.length; i++) {
            otherInfoElements[i].disabled = true;
        }
    }
};

function BtnOnClicked(action){
    Errors = 0;
    let arr = [];
    if (action == 'SearchByMaterial'){
        if (otherInfocCheckbox.checked == true) {
            for (var i = 0; i < inputElemsByMaterialStr.length; i++) {
                if (OnInputChange(inputElemsByMaterialStr[i]) == false) ++Errors;
                arr.push(inputElemsByMaterialStr[i].value);
            }
            for (var i = 0; i < inputElemsByMaterialInt.length; i++) {
                if (OnInputChange(inputElemsByMaterialInt[i]) == false) ++Errors;
                arr.push(parseInt(inputElemsByMaterialInt[i].value));
            }
        } else {
            if (OnInputChange(inputElemsByMaterialStr[0]) == false) ++Errors;
            arr.push(inputElemsByMaterialStr[0].value);
        }
    } else if (action == 'SearchByBank'){
        for (var i = 0; i < inputElemsByBankStr.length; i++) {
            if (OnInputChange(inputElemsByBankStr[i]) == false) ++Errors;
            arr.push(inputElemsByBankStr[i].value);
        }
        for (var i = 0; i < inputElemsByBankInt.length; i++) {
            if (OnInputChange(inputElemsByBankInt[i]) == false) ++Errors;
            arr.push(parseInt(inputElemsByBankInt[i].value));
        }
    } else if (action == 'Add' || action == 'Delete'){
        for (var i = 0; i < inputElemsAddStr.length; i++) {
            if (OnInputChange(inputElemsAddStr[i]) == false) ++Errors;
            arr.push(inputElemsAddStr[i].value);
        }
        for (var i = 0; i < inputElemsAddInt.length; i++) {
            if (OnInputChange(inputElemsAddInt[i]) == false) ++Errors;
            arr.push(parseInt(inputElemsAddInt[i].value));
        }
    }
    if (Errors == 0) SendReq(arr, action);
};

window.onload = function() {

    otherInfocCheckbox.checked = false;

    for (var i = 0; i < otherInfoElements.length; i++) {
        otherInfoElements[i].disabled = true;
    }

    console.log("JS is fully loaded!");
};