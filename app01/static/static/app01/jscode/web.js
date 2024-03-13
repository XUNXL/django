//提醒用户密码规格 
Password_Reminder.style.display = 'none';
let password_border = document.getElementById('id_password');
document.getElementById("id_password").addEventListener("focus", function () {  //光标停留事件
    let password = this.value;
    let Password_Reminder = document.getElementById('Password_Reminder');
    if (password.length < 6) {
        Password_Reminder.style.display = 'block';
        Password_Reminder.textContent = '*密码不得少于6位';
        password_border.style.border = '1px solid red';
    } else {
        Password_Reminder.style.display = 'none';
        password_border.style.border = '1px solid gainsboro';
    }
});
document.getElementById('id_password').addEventListener('input', function () {  //输入事件
    let password = this.value;
    let Password_Reminder = document.getElementById('Password_Reminder');
    if (password.length < 6) {
        Password_Reminder.style.display = 'block';
        Password_Reminder.textContent = '*密码不得少于6位';
        password_border.style.border = '1px solid red';
    } else {
        Password_Reminder.style.display = 'none';
        password_border.style.border = '1px solid gainsboro';
    }
});
document.getElementById("id_password").addEventListener("blur", function () {  //光标离开事件
    let password = this.value;
    let Password_Reminder = document.getElementById('Password_Reminder');
    if (password.length < 6 && password.length != 0) {
        Password_Reminder.style.display = 'block';
        Password_Reminder.textContent = '*密码不得少于6位';
        password_border.style.border = '1px solid red';
    } else {
        Password_Reminder.style.display = 'none';
        password_border.style.border = '1px solid gainsboro';
    }
});
//提醒用户输入两次相同的密码  
confirm_password.style.display = 'none'
let confilm_password_border = document.getElementById('id_confirm_password');
document.getElementById("id_confirm_password").addEventListener("focus", function () {
    let password_confilm = this.value;
    let password = password_border.value;
    if (password_confilm !== password) {
        confirm_password.style.display = 'block';
        confirm_password.textContent = '*两次密码不一致';
        confilm_password_border.style.border = '1px solid red';
    } else {
        confirm_password.style.display = 'none';
        confilm_password_border.style.border = '1px solid gainsboro';
    }
});
document.getElementById("id_confirm_password").addEventListener("input", function () {
    let password_confilm = this.value;
    let password = password_border.value;
    if (password_confilm !== password) {
        confirm_password.style.display = 'block';
        confirm_password.textContent = '*两次密码不一致';
        confilm_password_border.style.border = '1px solid red';
    } else {
        confirm_password.style.display = 'none';
        confilm_password_border.style.border = '1px solid gainsboro';
    }
});

document.getElementById("id_confirm_password").addEventListener("blur", function () {
    let password_confilm = this.value;
    let password = password_border.value;
    if (password_confilm !== password) {
        confirm_password.style.display = 'block';
        confirm_password.textContent = '*两次密码不一致';
        confilm_password_border.style.border = '1px solid red';
    } else {
        confirm_password.style.display = 'none';
        confilm_password_border.style.border = '1px solid gainsboro';
    }
});

//日期填写格式提示
let birthday = document.getElementById('birthday');
birthday.style.display = 'none';
document.getElementById('id_birthdate').addEventListener('focus', function () {
    birthday.style.display = 'block';
    birthday.textContent = '*推荐格式“2002-7-24”';
});

document.getElementById('id_birthdate').addEventListener('blur', function () {
    birthday.style.display = 'none';
});