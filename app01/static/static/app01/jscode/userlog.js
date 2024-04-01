// 获取表体元素
let tbody = document.querySelector(".table-group-divider");
// 初始化行数计数器
let rowCount = 0;
// 添加每一行的序号
tbody.querySelectorAll("tr").forEach(function (row) {
    rowCount++;
    row.querySelector("th").textContent = rowCount;
});

