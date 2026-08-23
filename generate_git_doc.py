#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成 Git 与 GitHub 远程仓库部署全步骤 Word 文档"""

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ===== 全局样式设置 =====
style = doc.styles['Normal']
style.font.name = '微软雅黑'
style.font.size = Pt(11)
style.paragraph_format.line_spacing = 1.5
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

for i in range(1, 4):
    heading_style = doc.styles[f'Heading {i}']
    heading_style.font.name = '微软雅黑'
    heading_style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    if i == 1:
        heading_style.font.size = Pt(18)
        heading_style.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB)
    elif i == 2:
        heading_style.font.size = Pt(15)
        heading_style.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
    elif i == 3:
        heading_style.font.size = Pt(13)
        heading_style.font.color.rgb = RGBColor(0x34, 0x49, 0x5E)


# ===== 辅助函数 =====
def add_code_block(code_text, caption=""):
    """添加代码块（灰底等宽字体）"""
    if caption:
        p = doc.add_paragraph()
        run = p.add_run(f"📌 {caption}")
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    p = doc.add_paragraph()
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x2D, 0x2D, 0x2D)
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), 'F5F5F5')
    shading_elm.set(qn('w:val'), 'clear')
    p.paragraph_format.element.get_or_add_pPr().append(shading_elm)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    return p


def add_tip(text):
    p = doc.add_paragraph()
    run = p.add_run(f"💡 提示：{text}")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0xE6, 0x7E, 0x22)
    run.italic = True
    return p


def add_warning(text):
    p = doc.add_paragraph()
    run = p.add_run(f"⚠️ 注意：{text}")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0xE7, 0x4C, 0x3C)
    run.bold = True
    return p


def add_step(num, text):
    """加粗的步骤标题"""
    p = doc.add_paragraph()
    run = p.add_run(f"步骤 {num}：{text}")
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB)
    return p


# ==========================================
# 封面 / 标题
# ==========================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(80)
run = p.add_run("Git 与 GitHub 远程仓库")
run.font.size = Pt(28)
run.font.color.rgb = RGBColor(0x1A, 0x56, 0xDB)
run.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("部署全步骤操作手册")
run.font.size = Pt(20)
run.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(30)
run = p.add_run("依据《暑假40天学习计划》第二阶段（Day 8-14）Git 版本控制要求整理")
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(10)
run = p.add_run("作者：刘鑫  |  邮箱：10252140412@stu.ecnu.edu.cn  |  2026年8月")
run.font.size = Pt(10)
run.font.italic = True

doc.add_page_break()

# ==========================================
# 目录
# ==========================================
doc.add_heading('📑 目录', level=1)
toc_items = [
    "〇、学习计划中的 Git 要求",
    "一、前期准备：安装 Git 与注册 GitHub 账号",
    "  1.1 安装 Git for Windows",
    "  1.2 注册 GitHub 账号",
    "  1.3 配置 Git 用户身份",
    "二、配置 SSH 密钥（免密推送，推荐）",
    "  2.1 生成 SSH 密钥",
    "  2.2 把公钥添加到 GitHub",
    "  2.3 验证连接",
    "三、创建本地仓库（git init）",
    "四、在 GitHub 上创建远程仓库",
    "五、关联本地与远程仓库（git remote add）",
    "六、首次提交与推送",
    "七、日常工作流：clone / pull / add / commit / push",
    "八、分支操作：branch / checkout / merge / rebase",
    "九、配置 .gitignore 忽略文件",
    "十、Fork + Pull Request 协作流程",
    "十一、常见问题排查",
]
for item in toc_items:
    p = doc.add_paragraph()
    run = p.add_run(item)
    run.font.size = Pt(11)
    if not item.startswith("  "):
        run.bold = True

doc.add_page_break()

# ==========================================
# 〇、学习计划中的 Git 要求
# ==========================================
doc.add_heading('〇、学习计划中的 Git 要求', level=1)
doc.add_paragraph('《暑假40天学习计划》中对 Git 版本控制的核心要求如下：')
add_table_with_data = None  # 占位，避免误用
table = doc.add_table(rows=1 + 5, cols=2)
table.style = 'Light Grid Accent 1'
hdr = table.rows[0].cells
hdr[0].text = '时间节点'
hdr[1].text = '任务要求'
rows = [
    ('Day 1（晚上）', '注册 GitHub 账号，创建 study-log 仓库记录每日学习'),
    ('Day 10（晚上）', '安装并学习 Git：git init / clone / add / commit'),
    ('Day 11（晚上）', 'Git 进阶：branch、merge、rebase；创建自己的 GitHub 学习仓库'),
    ('Day 12（上午）', '分支合并、解决冲突、Fork + Pull Request、.gitignore / stash / log、GitHub Pages'),
    ('Day 14/21/28/30/35/37', '各阶段成果：上传项目代码到 GitHub，写好 README，打 Tag'),
]
for ri, (a, b) in enumerate(rows):
    table.rows[ri + 1].cells[0].text = a
    table.rows[ri + 1].cells[1].text = b
for row in table.rows:
    for cell in row.cells:
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.size = Pt(10)
for cell in table.rows[0].cells:
    for p in cell.paragraphs:
        for run in p.runs:
            run.bold = True
doc.add_paragraph()
add_tip('Git 版本控制在"张豪实验室"和"米哈游岗位"两条路径中均为"✅ 需要"，优先级 🟡 高优先级。')

doc.add_page_break()

# ==========================================
# 一、前期准备
# ==========================================
doc.add_heading('一、前期准备：安装 Git 与注册 GitHub 账号', level=1)

doc.add_heading('1.1 安装 Git for Windows', level=2)
doc.add_paragraph('访问 Git 官网下载 Windows 安装包，一路点击 Next 安装即可（推荐保留默认选项）。')
add_code_block('下载地址：https://git-scm.com/download/win', '下载')
doc.add_paragraph('安装完成后，在任意文件夹空白处右键，选择「Git Bash Here」打开终端，输入以下命令验证：')
add_code_block('git --version', '验证安装')
add_code_block('# 输出示例\ngit version 2.55.0.windows.3', '预期输出')
add_tip('本机已安装 Git 2.55.0，可跳过安装步骤，直接进入 1.3 配置身份。')

doc.add_heading('1.2 注册 GitHub 账号', level=2)
doc.add_paragraph('1. 打开 GitHub 官网，点击右上角 Sign up 注册账号：')
add_code_block('https://github.com/', 'GitHub 官网')
doc.add_paragraph('2. 填写用户名（Username）、邮箱（Email）、密码（Password）。')
doc.add_paragraph('3. 邮箱会收到验证邮件，点击链接完成验证。')
add_warning('用户名（Username）会出现在仓库地址里（github.com/用户名/仓库名），建议使用简洁、专业、易记的英文名，之后在简历和联系导师邮件中都要用到。')

doc.add_heading('1.3 配置 Git 用户身份', level=2)
doc.add_paragraph('提交代码前需要告诉 Git "你是谁"。在 Git Bash 中执行以下两条命令（换成你自己的名字和邮箱）：')
add_code_block('git config --global user.name "刘鑫"\ngit config --global user.email "10252140412@stu.ecnu.edu.cn"', '全局配置身份')
add_tip('--global 表示对本机所有仓库生效；--local 表示仅当前仓库生效（优先级更高）。')
doc.add_paragraph('查看已配置的信息：')
add_code_block('git config --global user.name\ngit config --global user.email', '查看配置')

doc.add_page_break()

# ==========================================
# 二、配置 SSH 密钥
# ==========================================
doc.add_heading('二、配置 SSH 密钥（免密推送，推荐）', level=1)
doc.add_paragraph('通过 SSH 方式连接 GitHub，可以免去每次 push/pull 都要输入账号密码的麻烦，也更安全。')

doc.add_heading('2.1 生成 SSH 密钥', level=2)
doc.add_paragraph('在 Git Bash 中执行以下命令（-C 后面换成你自己的邮箱）：')
add_code_block('ssh-keygen -t ed25519 -C "10252140412@stu.ecnu.edu.cn"', '生成 ed25519 密钥')
doc.add_paragraph('命令执行后一路按回车即可：')
doc.add_paragraph('• 第一处回车：确认保存路径（默认 ~/.ssh/id_ed25519）')
doc.add_paragraph('• 第二处回车：设置密码（可直接回车跳过，即空密码）')
add_tip('ed25519 是当前推荐的非对称加密算法，比老式的 rsa 更快更安全。')

doc.add_heading('2.2 把公钥添加到 GitHub', level=2)
doc.add_paragraph('1. 查看并复制公钥内容：')
add_code_block('cat ~/.ssh/id_ed25519.pub', '查看公钥')
add_code_block('clip < ~/.ssh/id_ed25519.pub', 'Windows 下直接复制到剪贴板')
doc.add_paragraph('2. 登录 GitHub，点击右上角头像 → Settings → 左侧 SSH and GPG keys → 点击绿色按钮 New SSH key。')
doc.add_paragraph('3. Title 随便填（如 "My Windows Laptop"），Key 粘贴刚复制的公钥，点 Add SSH key 保存。')

doc.add_heading('2.3 验证连接', level=2)
add_code_block('ssh -T git@github.com', '测试 SSH 连接')
add_code_block('# 首次连接会询问是否信任该主机，输入 yes\nyes', '确认主机指纹')
add_code_block('# 看到下面这行就说明成功\nHi <用户名>! You\'ve successfully authenticated, but GitHub does not provide shell access.', '成功提示')

doc.add_page_break()

# ==========================================
# 三、创建本地仓库
# ==========================================
doc.add_heading('三、创建本地仓库（git init）', level=1)
doc.add_paragraph('进入你的项目文件夹（例如学习笔记目录），初始化一个本地 Git 仓库：')
add_code_block('cd /d/NoteBook        # 进入项目目录（Git Bash 路径写法）\ngit init               # 初始化仓库', '初始化本地仓库')
add_code_block('# 输出示例\nInitialized empty Git repository in D:/NoteBook/.git/', '预期输出')
add_tip('Git Bash 中磁盘路径写法：D 盘写作 /d，C 盘写作 /c，例如 /d/NoteBook 就是 D:\\NoteBook。')

doc.add_heading('（可选）用 git clone 直接拉取已有仓库', level=2)
doc.add_paragraph('如果你已经在 GitHub 上创建了仓库（或想复制别人的项目），可以用 clone 直接下载：')
add_code_block('git clone git@github.com:用户名/study-log.git', 'SSH 方式克隆')
add_code_block('git clone https://github.com/用户名/study-log.git', 'HTTPS 方式克隆')

doc.add_page_break()

# ==========================================
# 四、在 GitHub 上创建远程仓库
# ==========================================
doc.add_heading('四、在 GitHub 上创建远程仓库', level=1)
doc.add_paragraph('1. 登录 GitHub，点击右上角 + 号 → New repository。')
doc.add_paragraph('2. 填写仓库信息：')
doc.add_paragraph('• Repository name：study-log（学习日志仓库，按计划命名）')
doc.add_paragraph('• Description：可选，一句话描述，如"暑假40天学习日志"')
doc.add_paragraph('• 可见性：选择 Public（公开）或 Private（私有）')
doc.add_paragraph('3. 底部初始化选项：如果本地已有代码，就**不要勾选** "Add a README file" 等任何选项，直接点 Create repository。')
add_warning('如果勾选了 "Add a README file"，远程仓库会自带一次提交，之后再 push 本地代码会因历史不一致而报错。本地已有代码时保持全部不勾选。')

doc.add_paragraph('创建完成后，页面会显示两种连接方式，记下你的仓库地址：')
add_code_block('git@github.com:用户名/study-log.git        # SSH（推荐）\nhttps://github.com/用户名/study-log.git     # HTTPS', '仓库地址格式')

doc.add_page_break()

# ==========================================
# 五、关联本地与远程仓库
# ==========================================
doc.add_heading('五、关联本地与远程仓库（git remote add）', level=1)
doc.add_paragraph('回到本地仓库（Git Bash 中），把本地仓库和刚创建的远程仓库关联起来：')
add_code_block('git remote add origin git@github.com:用户名/study-log.git', '添加远程仓库 origin')
add_tip('origin 是远程仓库的默认别名，可理解为"远程仓库"的代称。add 只需执行一次。')
doc.add_paragraph('查看当前关联的远程仓库：')
add_code_block('git remote -v', '查看远程仓库')
add_code_block('# 输出示例\norigin  git@github.com:用户名/study-log.git (fetch)\norigin  git@github.com:用户名/study-log.git (push)', '预期输出')
add_tip('如果地址填错了，可以用 git remote set-url origin 新地址 来修改，或 git remote remove origin 删除后重新添加。')

doc.add_page_break()

# ==========================================
# 六、首次提交与推送
# ==========================================
doc.add_heading('六、首次提交与推送', level=1)
doc.add_paragraph('把本地代码提交并推送到 GitHub，完成"本地 ↔ 远程"的首次打通：')

add_step(1, '把文件加入暂存区')
add_code_block('git add .      # . 表示当前目录所有文件\n# 或指定某个文件：git add 文件名', '加入暂存区')

add_step(2, '提交到本地仓库')
add_code_block('git commit -m "first commit"', '提交（-m 后为提交说明）')

add_step(3, '把默认分支改名为 main（与 GitHub 保持一致）')
add_code_block('git branch -M main', '重命名分支')
add_tip('旧版本 Git 默认分支叫 master，GitHub 新仓库默认叫 main，用这步统一成 main。')

add_step(4, '推送到远程仓库')
add_code_block('git push -u origin main', '首次推送（-u 建立跟踪关系）')
add_tip('-u 参数会建立本地 main 与远程 origin/main 的跟踪关系，之后只需 git push 即可，不用再写 origin main。')

add_step(5, '回到 GitHub 刷新页面')
doc.add_paragraph('此时应能在仓库主页看到上传的文件，说明部署成功 ✅。')

doc.add_page_break()

# ==========================================
# 七、日常工作流
# ==========================================
doc.add_heading('七、日常工作流：clone / pull / add / commit / push', level=1)
doc.add_paragraph('这是学习计划要求的核心能力。每天记笔记、写代码后，按下面顺序执行即可：')

doc.add_heading('7.1 检查状态', level=2)
add_code_block('git status', '查看工作区状态（哪些文件改动/新增/删除）')

doc.add_heading('7.2 加入暂存区', level=2)
add_code_block('git add .', '把所有改动加入暂存区')

doc.add_heading('7.3 提交', level=2)
add_code_block('git commit -m "Day 10 线性代数笔记"', '提交并写明这次做了什么')
add_tip('提交说明（commit message）要写清楚"做了什么"，方便日后回看。')

doc.add_heading('7.4 推送到 GitHub', level=2)
add_code_block('git push', '推送到远程仓库（已建立跟踪关系）')

doc.add_heading('7.5 拉取远程更新（协作或换电脑时）', level=2)
add_code_block('git pull', '拉取并合并远程最新代码')
add_tip('换电脑或多人协作时，先 git pull 再开始工作，避免冲突。')

doc.add_heading('7.6 查看提交历史', level=2)
add_code_block('git log --oneline', '查看提交历史（一行一条，简洁）')
add_code_block('git log --oneline --graph --all', '查看分支图')

doc.add_page_break()

# ==========================================
# 八、分支操作
# ==========================================
doc.add_heading('八、分支操作：branch / checkout / merge / rebase', level=1)
doc.add_paragraph('分支（branch）是 Git 的核心概念。开发新功能前先开一个分支，测试通过后再合并回 main。')

doc.add_heading('8.1 创建并切换分支', level=2)
add_code_block('git branch dev        # 创建名为 dev 的分支\ngit checkout dev       # 切换到 dev 分支', '创建与切换')
add_code_block('git switch -c dev     # 新版 Git 可一步创建并切换', '简写')

doc.add_heading('8.2 查看所有分支', level=2)
add_code_block('git branch            # 当前分支前有 * 号\n# 输出示例\n* dev\n  main', '查看分支')

doc.add_heading('8.3 合并分支', level=2)
add_code_block('git checkout main     # 先切回 main\ngit merge dev          # 把 dev 合并进 main', '合并分支')

doc.add_heading('8.4 删除分支', level=2)
add_code_block('git branch -d dev     # 合并完成后删除 dev 分支', '删除分支')

doc.add_heading('8.5 rebase 与 merge 的区别', level=2)
doc.add_paragraph('• merge：保留完整分支历史，会产生一条"合并提交"。')
doc.add_paragraph('• rebase：把当前分支的提交"嫁接"到目标分支顶端，历史更线性、干净。')
add_warning('rebase 会改写提交历史，不要对已经 push 到远程的公共分支使用，个人学习阶段了解即可。')

doc.add_heading('8.6 解决冲突', level=2)
doc.add_paragraph('当两个分支改了同一文件的同一处，合并时会产生冲突（conflict）。此时 Git 会在文件中标记冲突位置：')
add_code_block('<<<<<<< HEAD\n你当前分支的内容\n=======\n另一个分支的内容\n>>>>>>> dev', '冲突标记')
doc.add_paragraph('手动保留正确内容，删除 <<<<<<< / ======= / >>>>>>> 三行标记，然后：')
add_code_block('git add 冲突文件\ngit commit -m "解决合并冲突"', '解决冲突')

doc.add_page_break()

# ==========================================
# 九、.gitignore
# ==========================================
doc.add_heading('九、配置 .gitignore 忽略文件', level=1)
doc.add_paragraph('.gitignore 用来告诉 Git 哪些文件/文件夹不要纳入版本控制（如缓存、虚拟环境、大文件、密钥等）。')
doc.add_paragraph('在项目根目录创建一个名为 .gitignore 的文件，内容示例：')
add_code_block('# Python 缓存\n__pycache__/\n*.pyc\n.ipynb_checkpoints/\n\n# 虚拟环境\nvenv/\nenv/\n\n# 编辑器与系统文件\n.vscode/\n.DS_Store\nThumbs.db\n\n# 敏感信息\n.env\n*.key\n', '.gitignore 示例')
add_warning('密钥、密码、token 等敏感文件一定要加入 .gitignore，绝不能提交到公开仓库。')

doc.add_heading('（可选）临时保存改动：git stash', level=2)
add_code_block('git stash           # 暂存当前未提交的改动\ngit stash pop       # 恢复最近的暂存', 'stash 用法')

doc.add_page_break()

# ==========================================
# 十、Fork + Pull Request
# ==========================================
doc.add_heading('十、Fork + Pull Request 协作流程', level=1)
doc.add_paragraph('这是 Day 12 要求的协作演练，也是开源贡献的标准流程。')

doc.add_heading('10.1 Fork（复刻仓库）', level=2)
doc.add_paragraph('在别人的 GitHub 仓库页面点击右上角 Fork 按钮，会把这个仓库复制到你自己账号下。')

doc.add_heading('10.2 克隆自己 Fork 的仓库', level=2)
add_code_block('git clone git@github.com:我的用户名/被Fork的仓库.git', '克隆')

doc.add_heading('10.3 修改后推送，发起 Pull Request', level=2)
add_code_block('git add .\ngit commit -m "修复了某问题"\ngit push', '提交并推送')
doc.add_paragraph('回到 GitHub 自己 Fork 的仓库页面，点击 Contribute → Open pull request，填写说明后提交。原仓库作者看到后可选择合并你的改动。')

doc.add_page_break()

# ==========================================
# 十一、常见问题排查
# ==========================================
doc.add_heading('十一、常见问题排查', level=1)

doc.add_heading('Q1：push 报错 Permission denied (publickey)', level=2)
doc.add_paragraph('SSH 密钥没配好或没添加到 GitHub。检查步骤：')
add_code_block('ssh -T git@github.com', '先测试连接')
doc.add_paragraph('确认 ~/.ssh/id_ed25519.pub 的内容已完整粘贴到 GitHub 的 SSH and GPG keys 中。')

doc.add_heading('Q2：push 报错 failed to push ... non-fast-forward', level=2)
doc.add_paragraph('远程仓库有你本地没有的提交（通常是创建仓库时勾选了 README）。先拉取再推送：')
add_code_block('git pull origin main --allow-unrelated-histories\ngit push', '拉取并允许合并无关历史')

doc.add_heading('Q3：remote origin already exists', level=2)
doc.add_paragraph('说明已经添加过 origin，查看或修改即可：')
add_code_block('git remote -v                                    # 查看\ngit remote set-url origin 新的仓库地址          # 修改', '查看/修改')

doc.add_heading('Q4：提交后才发现漏改 / 想撤销', level=2)
add_code_block('git reset HEAD~1      # 撤销最近一次 commit，改动回到暂存区\n# 或只改提交说明：git commit --amend', '撤销/修改提交')
add_warning('对已经 push 的提交慎用 reset，会影响远程历史；未 push 的提交可放心操作。')

doc.add_heading('Q5：忘记 git add 就 commit 了', level=2)
add_code_block('git add 漏掉的文件\ngit commit --amend --no-edit   # 把漏掉的文件补进上一次提交', '补提交')

# 结尾
doc.add_paragraph()
doc.add_page_break()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(120)
run = p.add_run("—— 手册完 ——")
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x7F, 0x8C, 0x8D)

doc.save('Git与GitHub远程仓库部署全步骤.docx')
print('已生成：Git与GitHub远程仓库部署全步骤.docx')
