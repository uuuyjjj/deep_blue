// 全局JavaScript函数

document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有工具提示
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
    
    // 搜索框自动完成功能
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            // 可以在这里添加搜索建议功能
            if (this.value.length > 2) {
                // 模拟搜索建议
                console.log('搜索建议:', this.value);
            }
        });
    }
    
    // 平滑滚动功能
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // 添加高亮效果
                targetElement.classList.add('bg-primary', 'bg-opacity-10');
                setTimeout(() => {
                    targetElement.classList.remove('bg-primary', 'bg-opacity-10');
                }, 2000);
            }
        });
    });
    
    // 自动保存功能
    function setupAutoSave(textareaId, interval = 30000) { // 默认30秒保存一次
        const textarea = document.getElementById(textareaId);
        if (!textarea) return;
        
        let lastSavedValue = textarea.value;
        
        // 检查是否有保存的草稿
        const savedDraft = localStorage.getItem(textareaId + '_draft');
        if (savedDraft && savedDraft !== textarea.value) {
            if (confirm('检测到未保存的草稿，是否恢复？')) {
                textarea.value = savedDraft;
                lastSavedValue = savedDraft;
            }
        }
        
        // 定期保存草稿
        setInterval(() => {
            if (textarea.value && textarea.value !== lastSavedValue) {
                localStorage.setItem(textareaId + '_draft', textarea.value);
                lastSavedValue = textarea.value;
                
                // 显示保存指示（可选）
                const saveIndicator = document.createElement('div');
                saveIndicator.className = 'position-fixed bottom-3 right-3 bg-success text-white px-3 py-1 rounded shadow-lg z-50';
                saveIndicator.textContent = '草稿已保存';
                document.body.appendChild(saveIndicator);
                
                setTimeout(() => {
                    saveIndicator.remove();
                }, 2000);
            }
        }, interval);
        
        // 表单提交时清除草稿
        const form = textarea.closest('form');
        if (form) {
            form.addEventListener('submit', function() {
                localStorage.removeItem(textareaId + '_draft');
            });
        }
    }
    
    // 为所有文本区域设置自动保存
    document.querySelectorAll('textarea').forEach(textarea => {
        if (textarea.id) {
            setupAutoSave(textarea.id);
        }
    });
    
    // 移动端优化：点击标签筛选时的交互
    document.querySelectorAll('.list-group-item a').forEach(link => {
        link.addEventListener('click', function(e) {
            // 在移动端，点击标签后关闭菜单（如果是在折叠菜单中）
            const navbarCollapse = document.getElementById('navbarNav');
            if (navbarCollapse && window.innerWidth < 768) {
                const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                if (bsCollapse && bsCollapse._isShown()) {
                    bsCollapse.hide();
                }
            }
        });
    });
    
    // 添加笔记卡片的悬停效果
    document.querySelectorAll('.list-group-item').forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
            this.style.transition = 'all 0.2s ease';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
    
    // 添加日期格式化函数到Date原型（如果需要）
    if (!Date.prototype.format) {
        Date.prototype.format = function(fmt) {
            const o = {
                'M+': this.getMonth() + 1,
                'd+': this.getDate(),
                'H+': this.getHours(),
                'm+': this.getMinutes(),
                's+': this.getSeconds()
            };
            
            if (/(y+)/.test(fmt)) {
                fmt = fmt.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length));
            }
            
            for (let k in o) {
                if (new RegExp('(' + k + ')').test(fmt)) {
                    fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)));
                }
            }
            
            return fmt;
        };
    }
    
    // 添加错误处理
    window.addEventListener('error', function(e) {
        console.error('JavaScript错误:', e.error);
        // 可以在这里添加错误日志功能
    });
});