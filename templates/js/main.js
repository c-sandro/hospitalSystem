function users_update_input(){
    const paramObj = document.getElementById("param");
    let optionsValue = document.getElementById("options").value;

    switch(optionsValue){
        case '0':
            paramObj.type = "email";
            break;
        case '1':
            paramObj.type = "number";
            break;
    }
}

function patients_update_input(){
    const paramObj = document.getElementById("param");
    let optionsValue = document.getElementById("options").value;

    switch(optionsValue){
        case '0':
            paramObj.type = "text";
            paramObj.minLength = 0;
            paramObj.maxLength = 256;
            paramObj.value = "";
            break;
        case '1':
            paramObj.type = "text";
            paramObj.minLength = 11;
            paramObj.maxLength = 11;
            paramObj.value = "";
            break;
        case '2':
            paramObj.type = "number";
            paramObj.minLength = 0;
            paramObj.maxLength = 256;
            paramObj.value = "";
            break;
    }
}

function doctors_update_input(){
    const paramObj = document.getElementById("param");
    let optionsValue = document.getElementById("options").value;

    switch(optionsValue){
        case '0':
            paramObj.type = "text";
            paramObj.minLength = 0;
            paramObj.maxLength = 256;
            paramObj.value = "";
            break;
        case '1':
            paramObj.type = "text";
            paramObj.minLength = 11;
            paramObj.maxLength = 11;
            paramObj.value = "";
            break;
        case '2':
            paramObj.type = "number";
            paramObj.minLength = 0;
            paramObj.maxLength = 256;
            paramObj.value = "";
            break;
        case '3':
            paramObj.type = "number";
            paramObj.minLength = 0;
            paramObj.maxLength = 256;
            paramObj.value = "";
            break;
    }
}

function appointments_update_input(){
        const paramObj = document.getElementById("param");
        let optionsValue = document.getElementById("options").value;

        switch(optionsValue){
            case '0':
                paramObj.type = "number";
                paramObj.minLength = 0;
                paramObj.maxLength = 256;
                paramObj.value = "";
                break;
            case '1':
                paramObj.type = "text";
                paramObj.minLength = 11;
                paramObj.maxLength = 11;
                paramObj.value = "";
                break;
            case '2':
                paramObj.type = "number";
                paramObj.minLength = 0;
                paramObj.maxLength = 256;
                paramObj.value = "";
                break;
        }
    }