// 筛选、搜索、排序和懒加载功能
document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded');
    
    // 获取DOM元素
    const monthBtns = document.querySelectorAll('.month-btn');
    const statusBtns = document.querySelectorAll('.status-btn');
    const categoryBtns = document.querySelectorAll('.category-btn');
    const sortBtns = document.querySelectorAll('.sort-btn');
    const searchInput = document.getElementById('searchInput');
    const exportBtn = document.getElementById('exportBtn');
    const selectAllBtn = document.getElementById('selectAllBtn');
    const clearAllBtn = document.getElementById('clearAllBtn');
    const selectedCount = document.getElementById('selectedCount');
    const resultsCount = document.getElementById('resultsCount');
    const papersContainer = document.getElementById('papers-container');
    
    console.log('DOM elements:', {
        monthBtns: monthBtns.length,
        statusBtns: statusBtns.length,
        categoryBtns: categoryBtns.length,
        sortBtns: sortBtns.length,
        searchInput: !!searchInput,
        exportBtn: !!exportBtn,
        selectAllBtn: !!selectAllBtn,
        clearAllBtn: !!clearAllBtn,
        resultsCount: !!resultsCount,
        papersContainer: !!papersContainer
    });
    
    // 状态变量
    let allPapersData = [];  // 所有论文数据
    let currentMonth = 'all';  // 当前选中的月份
    let currentStatus = 'all';
    let currentCategory = 'all';
    let currentSort = 'date-desc';
    let searchTerm = '';
    let filteredPapers = [];
    let loadedCount = 0;
    const initialBatchSize = 20;  // 第一次加载20个
    const subsequentBatchSize = 10;  // 后续每次加载10个
    let isLoading = false;
    let observer = null;
    let monthsCache = {};  // 缓存已加载的月份数据
    
    // 加载月份索引
    async function loadMonthsIndex() {
        try {
            const response = await fetch('data/index.json');
            const monthsIndex = await response.json();
            console.log('Months index loaded:', monthsIndex);
            
            // 默认加载最新月份的数据
            if (monthsIndex.length > 0) {
                await loadMonthData('all');
            }
        } catch (e) {
            console.error('Failed to load months index:', e);
        }
    }
    
    // 加载指定月份的数据
    async function loadMonthData(month) {
        if (month === 'all') {
            // 加载所有月份
            try {
                const response = await fetch('data/index.json');
                const monthsIndex = await response.json();
                
                // 加载所有月份数据
                allPapersData = [];
                for (const monthInfo of monthsIndex) {
                    if (!monthsCache[monthInfo.month]) {
                        const monthResponse = await fetch(`data/${monthInfo.month}.json`);
                        monthsCache[monthInfo.month] = await monthResponse.json();
                    }
                    allPapersData.push(...monthsCache[monthInfo.month]);
                }
                console.log(`Loaded all months, total ${allPapersData.length} papers`);
            } catch (e) {
                console.error('Failed to load all months data:', e);
            }
        } else {
            // 加载单个月份
            if (!monthsCache[month]) {
                try {
                    const response = await fetch(`data/${month}.json`);
                    monthsCache[month] = await response.json();
                    console.log(`Loaded month ${month}, ${monthsCache[month].length} papers`);
                } catch (e) {
                    console.error(`Failed to load month ${month}:`, e);
                    return;
                }
            }
            allPapersData = monthsCache[month];
            console.log(`Using cached data for ${month}, ${allPapersData.length} papers`);
        }
        
        // 数据加载完成后，触发筛选
        filterAndSortPapers();
    }
    
    // 生成论文HTML
    function createPaperHTML(paper) {
        const tags = paper.tags ? paper.tags.map(tag => `<span class="tag">${tag}</span>`).join('') : '';
        
        // 提取代码链接
        let codeLink = '';
        if (paper.code_link) {
            codeLink = `<a href="${paper.code_link}" target="_blank" class="code-link">📄 Code/Project</a>`;
        }
        
        // 获取会议徽章
        let venueBadge = '';
        if (paper.conference) {
            const badgeInfo = getVenueBadge(paper.conference);
            if (badgeInfo) {
                venueBadge = `<span class="venue-badge ${badgeInfo.class}">${badgeInfo.text}</span>`;
            }
        }
        
        const status = paper.conference ? 'published' : 'preprint';
        const firstCategory = paper.categories && paper.categories.length > 0 ? paper.categories[0] : '';
        
        return `
            <article class="paper-card" data-date="${paper.published}" data-status="${status}" data-tags="${paper.tags ? paper.tags.join(',') : ''}" data-paper-id="${paper.id}">
                <div class="paper-select">
                    <input type="checkbox" class="paper-checkbox" id="check-${paper.id}" data-paper-id="${paper.id}">
                    <label for="check-${paper.id}"></label>
                </div>
                <div class="paper-content">
                    <h2 class="paper-title">
                        <a href="https://arxiv.org/abs/${paper.id}" target="_blank">${paper.title}</a>
                    </h2>
                    <div class="paper-meta">
                        <span class="meta-item">📅 ${paper.published}</span>
                        ${venueBadge}
                        ${codeLink}
                    </div>
                    <div class="paper-authors">
                        👥 ${paper.authors}
                    </div>
                    <div class="paper-tags">
                        ${tags}
                    </div>
                    <div class="paper-abstract">
                        <details>
                            <summary>查看摘要</summary>
                            <p>${paper.abstract}</p>
                        </details>
                    </div>
                </div>
            </article>
        `;
    }
    
    // 获取会议徽章信息
    function getVenueBadge(conference) {
        if (!conference) return null;
        
        // 根据会议名称中包含的关键词决定徽章样式
        const conferenceUpper = conference.toUpperCase();
        let badgeClass = 'badge-published';  // 默认样式
        
        // 顶级会议匹配
        if (conferenceUpper.includes('NEURIPS')) {
            badgeClass = 'badge-neurips';
        } else if (conferenceUpper.includes('ICLR')) {
            badgeClass = 'badge-iclr';
        } else if (conferenceUpper.includes('ICML')) {
            badgeClass = 'badge-icml';
        } else if (conferenceUpper.includes('CVPR')) {
            badgeClass = 'badge-cvpr';
        } else if (conferenceUpper.includes('ICCV')) {
            badgeClass = 'badge-iccv';
        } else if (conferenceUpper.includes('ECCV')) {
            badgeClass = 'badge-eccv';
        } else if (conferenceUpper.includes('ACL')) {
            badgeClass = 'badge-acl';
        } else if (conferenceUpper.includes('EMNLP')) {
            badgeClass = 'badge-emnlp';
        } else if (conferenceUpper.includes('NAACL')) {
            badgeClass = 'badge-naacl';
        } else if (conferenceUpper.includes('AAAI')) {
            badgeClass = 'badge-aaai';
        } else if (conferenceUpper.includes('IJCAI')) {
            badgeClass = 'badge-ijcai';
        }
        
        // 直接使用从 ArXiv comments 提取的完整会议名称
        return { class: badgeClass, text: conference };
    }
    
    // 更新研究领域按钮的数量
    function updateCategoryButtonCounts() {
        // 先筛选出符合当前状态的论文
        const statusFilteredPapers = allPapersData.filter(paper => {
            const status = paper.conference ? 'published' : 'preprint';
            return currentStatus === 'all' || status === currentStatus;
        });
        
        // 计算各个领域的数量
        const categoryCounts = {
            'all': statusFilteredPapers.length,
            'Computer Vision': 0,
            'Natural Language Processing': 0,
            'Machine Learning': 0,
            'Robotics': 0,
            'Multimodal': 0
        };
        
        statusFilteredPapers.forEach(paper => {
            const tags = paper.tags || [];
            tags.forEach(tag => {
                if (categoryCounts.hasOwnProperty(tag)) {
                    categoryCounts[tag]++;
                }
            });
        });
        
        // 更新按钮文本
        categoryBtns.forEach(btn => {
            const category = btn.dataset.category;
            const displayName = category === 'all' ? '全部' : 
                               category === 'Natural Language Processing' ? 'NLP' : category;
            const count = categoryCounts[category] || 0;
            btn.textContent = `${displayName} (${count})`;
        });
    }
    
    // 筛选和排序论文
    function filterAndSortPapers() {
        console.log('Filtering papers:', { currentStatus, currentCategory, searchTerm, currentSort });
        
        // 筛选
        filteredPapers = allPapersData.filter(paper => {
            const status = paper.conference ? 'published' : 'preprint';
            const tags = paper.tags || [];
            const text = `${paper.title} ${paper.authors} ${paper.abstract}`.toLowerCase();
            
            const matchStatus = currentStatus === 'all' || status === currentStatus;
            const matchCategory = currentCategory === 'all' || tags.includes(currentCategory);
            const matchSearch = searchTerm === '' || text.includes(searchTerm);
            
            return matchStatus && matchCategory && matchSearch;
        });
        
        console.log(`Filtered to ${filteredPapers.length} papers`);
        
        // 排序
        filteredPapers.sort((a, b) => {
            const dateA = new Date(a.published);
            const dateB = new Date(b.published);
            
            if (currentSort === 'date-desc') {
                return dateB - dateA;
            } else {
                return dateA - dateB;
            }
        });
        
        // 更新研究领域按钮的数量
        updateCategoryButtonCounts();
        
        // 更新显示
        if (resultsCount) {
            resultsCount.textContent = `显示 ${filteredPapers.length} 篇论文`;
        }
        
        // 重置懒加载
        loadedCount = 0;
        if (papersContainer) {
            papersContainer.innerHTML = '';
        }
        
        // 移除旧的 observer
        if (observer) {
            observer.disconnect();
        }
        
        // 加载第一批
        loadMorePapers();
    }
    
    // 加载更多论文
    function loadMorePapers() {
        if (isLoading || loadedCount >= filteredPapers.length) {
            console.log('Skip loading:', { isLoading, loadedCount, total: filteredPapers.length });
            return;
        }
        
        isLoading = true;
        
        // 第一次加载50个，后续每次10个
        const batchSize = loadedCount === 0 ? initialBatchSize : subsequentBatchSize;
        console.log(`Loading papers ${loadedCount} to ${loadedCount + batchSize} (batch size: ${batchSize})`);
        
        const endIndex = Math.min(loadedCount + batchSize, filteredPapers.length);
        const fragment = document.createDocumentFragment();
        
        for (let i = loadedCount; i < endIndex; i++) {
            const paperHTML = createPaperHTML(filteredPapers[i]);
            const temp = document.createElement('div');
            temp.innerHTML = paperHTML;
            fragment.appendChild(temp.firstElementChild);
        }
        
        // 移除旧的加载指示器
        const oldIndicator = document.getElementById('loading-indicator');
        if (oldIndicator) {
            oldIndicator.remove();
        }
        
        papersContainer.appendChild(fragment);
        loadedCount = endIndex;
        isLoading = false;
        
        console.log(`Loaded ${endIndex} papers total`);
        
        // 如果还有更多，设置加载触发器
        if (loadedCount < filteredPapers.length) {
            setupLoadTrigger();
        }
    }
    
    // 设置加载触发器
    function setupLoadTrigger() {
        let indicator = document.getElementById('loading-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'loading-indicator';
            indicator.className = 'loading-indicator';
            indicator.style.height = '100px';
            indicator.style.margin = '20px 0';
            indicator.style.textAlign = 'center';
            indicator.style.color = '#666';
            indicator.textContent = '加载更多...';
            papersContainer.appendChild(indicator);
        }
        
        // 创建新的 observer
        if (observer) {
            observer.disconnect();
        }
        
        observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    console.log('Loading more papers (intersection detected)');
                    loadMorePapers();
                }
            });
        }, {
            rootMargin: '200px'
        });
        
        observer.observe(indicator);
    }
    
    // 月份筛选
    monthBtns.forEach(btn => {
        btn.addEventListener('click', async function() {
            console.log('Month button clicked:', this.dataset.month);
            monthBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentMonth = this.dataset.month;
            
            // 显示加载提示
            if (resultsCount) {
                resultsCount.textContent = '加载中...';
            }
            if (papersContainer) {
                papersContainer.innerHTML = '<div style="text-align: center; padding: 40px; color: #666;">加载中...</div>';
            }
            
            // 加载月份数据
            await loadMonthData(currentMonth);
        });
    });
    
    // 发表状态筛选
    statusBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('Status button clicked:', this.dataset.status);
            statusBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentStatus = this.dataset.status;
            filterAndSortPapers();
        });
    });
    
    // 研究领域筛选
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            console.log('Category button clicked:', this.dataset.category);
            categoryBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentCategory = this.dataset.category;
            filterAndSortPapers();
        });
    });
    
    // 排序按钮
    sortBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            console.log('Sort button clicked:', this.dataset.sort);
            e.preventDefault();
            sortBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentSort = this.dataset.sort;
            filterAndSortPapers();
        });
    });
    
    // 搜索输入
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            searchTerm = this.value.toLowerCase();
            console.log('Search term:', searchTerm);
            filterAndSortPapers();
        });
    }
    
    // 更新选中数量
    function updateSelectedCount() {
        const count = document.querySelectorAll('.paper-checkbox:checked').length;
        if (selectedCount) {
            selectedCount.textContent = count;
        }
    }
    
    // 监听复选框变化（使用事件委托）
    if (papersContainer) {
        papersContainer.addEventListener('change', function(e) {
            if (e.target.classList.contains('paper-checkbox')) {
                updateSelectedCount();
            }
        });
    }
    
    // 全选功能
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', function() {
            const checkboxes = document.querySelectorAll('.paper-checkbox');
            checkboxes.forEach(cb => cb.checked = true);
            updateSelectedCount();
            console.log('All papers selected');
        });
    }
    
    // 清空选择
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', function() {
            const checkboxes = document.querySelectorAll('.paper-checkbox');
            checkboxes.forEach(cb => cb.checked = false);
            updateSelectedCount();
            console.log('All selections cleared');
        });
    }
    
    // 导出功能
    if (exportBtn) {
        exportBtn.addEventListener('click', function(e) {
            console.log('Export button clicked');
            e.preventDefault();
            exportToBibTeX();
        });
    }
    
    // 导出为 BibTeX
    function exportToBibTeX() {
        // 获取所有选中的复选框
        const checkboxes = document.querySelectorAll('.paper-checkbox:checked');
        
        if (checkboxes.length === 0) {
            alert('请至少选择一篇论文导出！');
            return;
        }
        
        // 获取选中的论文ID
        const selectedIds = Array.from(checkboxes).map(cb => cb.dataset.paperId);
        
        // 从所有论文数据中找到对应的论文
        const selectedPapers = allPapersData.filter(paper => selectedIds.includes(paper.id));
        
        let bibtex = '';
        selectedPapers.forEach((paper, index) => {
            const arxivId = paper.id;
            const year = paper.published.split('-')[0];
            
            bibtex += `@article{${arxivId.replace('.', '_')},\n`;
            bibtex += `  title={${paper.title}},\n`;
            bibtex += `  author={${paper.authors}},\n`;
            bibtex += `  year={${year}},\n`;
            bibtex += `  journal={arXiv preprint arXiv:${arxivId}}`;
            if (paper.conference) {
                bibtex += `,\n  note={${paper.conference}}`;
            }
            bibtex += `\n}\n\n`;
        });
        
        console.log(`Exporting ${selectedPapers.length} selected papers`);
        downloadFile(bibtex, 'papers.bib', 'text/plain');
    }
    
    // 下载文件
    function downloadFile(content, filename, contentType) {
        const blob = new Blob([content], { type: contentType });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        console.log('File download triggered:', filename);
    }
    
    // 初始化 - 加载数据
    console.log('Initializing...');
    loadMonthsIndex();
});
