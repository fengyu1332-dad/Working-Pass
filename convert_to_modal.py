#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将现有的专业星图HTML转换为使用模态框的版本
"""

from bs4 import BeautifulSoup
import re

# 读取现有HTML文件
with open('major_starmap_final.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# 找到所有专业卡片
major_cards = soup.find_all('div', class_='major-card')

modal_container = soup.new_tag('div')
modal_container['id'] = 'modal-container'

# 为每个专业创建模态框
for card in major_cards:
    card_id = card.get('id', '')
    major_code = card_id.replace('card-', '') if card_id else ''
    
    # 修改卡片，移除内部的detail-section，并修改onclick
    detail_section = card.find('div', class_='detail-section')
    
    if detail_section and major_code:
        # 保存detail-section的内容到模态框
        modal = soup.new_tag('div')
        modal['id'] = f'modal-{major_code}'
        modal['class'] = 'modal'
        modal['style'] = 'display: none;'
        
        modal_content = soup.new_tag('div')
        modal_content['class'] = 'modal-content'
        
        # 创建模态框头部
        modal_header = soup.new_tag('div')
        modal_header['class'] = 'modal-header'
        
        # 复制卡片头部
        card_header = card.find('div', class_='card-header')
        if card_header:
            title_div = soup.new_tag('div')
            title_div['class'] = 'modal-title'
            for child in card_header.children:
                title_div.append(child.copy())
            modal_header.append(title_div)
        
        # 添加关闭按钮
        close_btn = soup.new_tag('button')
        close_btn['class'] = 'modal-close'
        close_btn['onclick'] = f'closeModal("{major_code}")'
        close_btn.string = '✕'
        modal_header.append(close_btn)
        
        modal_content.append(modal_header)
        
        # 创建模态框主体
        modal_body = soup.new_tag('div')
        modal_body['class'] = 'modal-body'
        
        for child in detail_section.children:
            modal_body.append(child.copy())
        
        modal_content.append(modal_body)
        modal.append(modal_content)
        modal_container.append(modal)
        
        # 从原卡片中移除detail-section
        detail_section.decompose()
        
        # 修改卡片的onclick事件
        card['onclick'] = f'openModal("{major_code}")'


# 添加模态框样式
style_tag = soup.find('style')
additional_styles = '''
        .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 9999; overflow-y: auto; padding: 20px; }
        .modal-content { background: var(--surface-container); max-width: 900px; width: 100%; max-height: 90vh; overflow-y: auto; border-radius: 24px; box-shadow: 0 8px 48px rgba(0, 0, 0, 0.1); }
        .modal-header { display: flex; justify-content: space-between; align-items: center; padding: 24px; border-bottom: 1px solid var(--outline); position: sticky; top: 0; background: var(--surface-container); z-index: 10; }
        .modal-title { display: flex; align-items: center; gap: 16px; }
        .modal-title h2 { font-family: "Literata", serif; font-size: 28px; font-weight: 700; color: var(--secondary); margin: 0; }
        .modal-close { background: var(--secondary-container); border: none; width: 40px; height: 40px; border-radius: 50%; font-size: 24px; cursor: pointer; color: var(--secondary); transition: all 0.3s; }
        .modal-close:hover { background: var(--primary); color: white; }
        .modal-body { padding: 32px; }
        @media (max-width: 768px) { 
            .modal { padding: 10px; }
            .modal-content { max-height: 95vh; }
        }
'''
style_tag.string += additional_styles

# 修改JavaScript
script_tag = soup.find('script')

new_script = '''
        let currentModal = null;
        
        function openModal(code) {
            document.querySelectorAll('.modal').forEach(m => m.style.display = 'none');
            const modal = document.getElementById('modal-' + code);
            if (modal) {
                modal.style.display = 'flex';
                currentModal = code;
                document.body.style.overflow = 'hidden';
            }
        }
        
        function closeModal(code) {
            const modal = document.getElementById('modal-' + code);
            if (modal) {
                modal.style.display = 'none';
                currentModal = null;
                document.body.style.overflow = '';
            }
        }
        
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('modal') && currentModal) {
                closeModal(currentModal);
            }
        });
        
        function toggleCard(code) {
            // 保留这个函数但不做任何事，避免报错
            openModal(code);
        }
        
        function filterMajors(category) {
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.filter === category) btn.classList.add('active');
            });
            document.querySelectorAll('.major-card').forEach(card => {
                if (category === 'all' || card.dataset.category === category) card.classList.remove('hidden');
                else card.classList.add('hidden');
            });
        }
        
        function searchMajors(query) {
            const searchTerm = query.toLowerCase().trim();
            document.querySelectorAll('.major-card').forEach(card => {
                const name = card.dataset.name.toLowerCase();
                const category = card.dataset.category.toLowerCase();
                if (name.includes(searchTerm) || category.includes(searchTerm)) card.classList.remove('hidden');
                else card.classList.add('hidden');
            });
        }
        
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.getElementById('searchInput').value = '';
                filterMajors(btn.dataset.filter);
            });
        });
        
        document.getElementById('searchInput').addEventListener('input', (e) => searchMajors(e.target.value));
'''
script_tag.string = new_script

# 将模态框添加到页面中，在</body>之前
body_tag = soup.find('body')
container = body_tag.find('div', class_='container')
body_tag.insert(body_tag.index(container) + 1, modal_container)

# 保存结果
output_path = 'major_starmap_modal_final.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

print(f"✅ 成功生成模态框版本！")
print(f"📁 输出文件：{output_path}")
