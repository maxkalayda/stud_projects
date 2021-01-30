function sendData(button) {
    var reqType = button.getAttribute("id");
    console.log(reqType);
    
    var input1 = document.getElementById("InputID").value;
    var input2 = document.getElementById("InputLogin").value;
    var input3 = document.getElementById("InputPassword").value;
    console.log(input1, input2, input3);

    let dictionary = new Object();
    dictionary = {"id": input1, "login": input2, "passwd": input3};
    console.log(dictionary);
    
    url = "/admin/" + reqType;
    console.log(url);

    let request = new XMLHttpRequest();
    request.open("POST", url);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            console.log(this.responseText)
            var feedback = JSON.parse(this.responseText);
            console.log(feedback);
            while (document.querySelector('tbody>tr')){
                document.querySelector('tbody>tr').remove();
            }
            for (var i = 0; i < feedback.length; i++){
                var result = "<tr><td>" + feedback[i][0] + "</td><td>" + feedback[i][1] + "</td><td>" + feedback[i][2] + "</td></tr>";
                document.querySelector('table>tbody').insertAdjacentHTML('beforeend', result);
             }
        }        
    }
    var reqData = JSON.stringify(dictionary); 
    console.log(reqData);
    request.send(reqData);

}