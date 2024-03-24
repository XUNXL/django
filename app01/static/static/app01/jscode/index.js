// 获取当前页面的 URL
let currentUrl = window.location.href;

// 找到最后一个斜杠的位置
let lastSlashIndex = currentUrl.lastIndexOf("/");

// 找到倒数第二个斜杠的位置
let secondLastSlashIndex = currentUrl.lastIndexOf("/", lastSlashIndex - 1);

// 获取倒数第二个斜杠后面的内容
let afterSecondLastSlash = currentUrl.substring(secondLastSlashIndex + 1, lastSlashIndex);

let newUrl = currentUrl.substring(0, secondLastSlashIndex + 1) + "index/";
let newUrl1 = currentUrl.substring(0, secondLastSlashIndex + 1) + "submit/";
let newUrl2 = currentUrl.substring(0, secondLastSlashIndex + 1) + "introduction/";
let newUrl3 = currentUrl.substring(0, secondLastSlashIndex + 1) + "userlog/";

function turnTo(index) {
    if (index == 0) {
        window.location.href = newUrl;
    } else if (index == 1) {
        window.location.href = newUrl1;
    } else if (index == 2) {
        window.location.href = newUrl2;
    } else if (index == 3) {
        window.location.href = newUrl3;
    }
}

// 获取表体元素
let tbody = document.querySelector(".table-group-divider");
console.log(tbody);
// 初始化行数计数器
let rowCount = 0;

// 添加每一行的序号
tbody.querySelectorAll("tr").forEach(function (row) {
    rowCount++;
    row.querySelector("th").textContent = rowCount;
});
