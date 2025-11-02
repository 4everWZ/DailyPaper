// 筛选和搜索功能
document.addEventListener('DOMContentLoaded', function() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('searchInput');
    const papers = document.querySelectorAll('.paper-card');
    
    let currentFilter = 'all';
    let searchTerm = '';
    
    // 筛选按钮点击事件
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // 更新按钮状态
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            currentFilter = this.dataset.filter;
            filterPapers();
        });
    });
    
    // 搜索输入事件
    searchInput.addEventListener('input', function() {
        searchTerm = this.value.toLowerCase();
        filterPapers();
    });
    
    // 筛选论文
    function filterPapers() {
        let visibleCount = 0;
        
        papers.forEach(paper => {
            const tags = paper.dataset.tags.split(',');
            const text = paper.textContent.toLowerCase();
            
            // 检查标签筛选
            const matchFilter = currentFilter === 'all' || tags.includes(currentFilter);
            
            // 检查搜索关键词
            const matchSearch = searchTerm === '' || text.includes(searchTerm);
            
            if (matchFilter && matchSearch) {
                paper.style.display = 'block';
                visibleCount++;
            } else {
                paper.style.display = 'none';
            }
        });
        
        // 显示无结果提示
        const container = document.getElementById('papers-container');
        let noResults = container.querySelector('.no-results');
        
        if (visibleCount === 0) {
            if (!noResults) {
                noResults = document.createElement('p');
                noResults.className = 'no-results';
                noResults.textContent = '未找到匹配的论文';
                container.appendChild(noResults);
            }
        } else {
            if (noResults) {
                noResults.remove();
            }
        }
    }
});
