// 获取DOM元素
const themeToggle = document.getElementById('theme-handoff');
const themeStyle = document.getElementById('theme');
// 从本地存储获取当前主题，默认为黑夜
let currentTheme = localStorage.getItem('theme') || 'dark';

function applyTheme(theme) {
    themeStyle.href = `${theme}_theme.css`;
    localStorage.setItem('theme', theme);
}
// 切换主题
function handoffTheme() {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(currentTheme);
}
// 事件监听
if (themeToggle) {
        themeToggle.addEventListener('click', handoffTheme);
    } else {
        console.error('找不到切换按钮元素');
    }

// 页面加载时应用保存的主题
document.addEventListener('DOMContentLoaded', () => {
    applyTheme(currentTheme);
});