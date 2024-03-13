const button = document.querySelectorAll(".delete_button");
const table = document.querySelector(".history_record");
button.forEach(function (button) {
    button.addEventListener('click', function () {
        let row = button.parentNode.parentNode;
        let r = confirm("确定要删除吗？")
        if (r == true) {
            row.parentNode.removeChild(row);
        }
    });
});  //单个删除按钮

//全部删除
document.getElementById('delete_all_button').addEventListener('click', function () {
    let table = document.getElementById('history_record');
    let rows = table.getElementsByTagName('tr');
    let r = confirm("确定要全部删除吗？")
    if (r == true) {
        for (let i = rows.length - 1; i > 0; i--) {
            table.deleteRow(i);
        }
    }
});

//返回按钮
const back = document.querySelector(".turnback");
back.addEventListener('click', function () {
    window.location.href = '/index/';
});

