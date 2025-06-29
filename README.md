# 食光机小程序菜谱数据生成脚本

## 项目简介

这是一个基于Coze智能体API的菜谱数据生成工具，专为食光机小程序开发。该项目可以批量获取菜谱信息并将其保存到Excel数据库中，支持单个菜谱查询和批量处理。

## 功能特性

- 🍳 **智能菜谱生成**: 调用Coze智能体API，根据菜谱名称自动生成详细的菜谱信息
- 📊 **数据库管理**: 自动将菜谱数据保存到Excel格式的数据库中
- 🔄 **批量处理**: 支持从文本文件读取菜谱名称列表，批量生成菜谱数据
- 🔍 **单个查询**: 支持交互式单个菜谱查询和展示
- 🛡️ **数据安全**: 支持环境变量配置，保护API密钥安全

## 项目结构

```
菜谱内容与封面生成-cursor/
├── data/                           # 数据目录
│   └── database.xlsx              # Excel数据库文件
├── coze_api_utils.py             # Coze API工具类
├── recipe_bot_client.py           # 单个菜谱查询客户端
├── recipe_to_excel.py            # 批量菜谱数据生成脚本
├── 家常菜菜谱名称.txt              # 菜谱名称列表
├── requirements.txt              # 项目依赖
├── .gitignore                   # Git忽略文件
└── README.md                    # 项目说明文档
```

## 安装与配置

### 1. 环境要求

- Python 3.7+
- pip包管理器

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

使用环境变量设置API密钥（推荐方式）：

**Windows PowerShell:**
```powershell
$env:COZE_API_TOKEN="your_actual_token_here"
```

**Windows CMD:**
```cmd
set COZE_API_TOKEN=your_actual_token_here
```

**Linux/macOS:**
```bash
export COZE_API_TOKEN="your_actual_token_here"
```

如果未设置环境变量，程序运行时会提示您手动输入API令牌。

### 4. 获取Coze API Token

1. 访问 [Coze开放平台](https://www.coze.cn/)
2. 注册并登录账号
3. 创建智能体应用
4. 在API设置中获取Personal Access Token

## 使用方法

### 单个菜谱查询

运行交互式菜谱查询客户端：

```bash
python recipe_bot_client.py
```

程序会提示您输入菜谱名称，然后显示详细的菜谱信息，包括：
- 菜谱名称
- 烹饪时间
- 热量信息
- 难度等级
- 菜品描述
- 详细烹饪步骤
- 图片链接（如有）

### 批量菜谱数据生成

1. **准备菜谱名称列表**：
   编辑 `家常菜菜谱名称.txt` 文件，每行一个菜谱名称。

2. **运行批量处理脚本**：
```bash
python recipe_to_excel.py
```

3. **查看结果**：
   生成的数据将保存在 `data/database.xlsx` 文件中。

### Excel数据库结构

生成的Excel文件包含以下字段：

| 字段名 | 描述 | 类型 |
|--------|------|------|
| id | 菜谱唯一标识符 | 整数 |
| name | 菜谱名称 | 文本 |
| cook_time | 烹饪时间 | 文本 |
| calories | 热量信息 | 文本 |
| image | 图片链接 | 文本 |
| description | 菜品描述 | 文本 |
| steps | 烹饪步骤（JSON格式） | 文本 |
| tools | 所需工具（JSON格式） | 文本 |
| prep_steps | 准备步骤（JSON格式） | 文本 |
| tips | 烹饪小贴士（JSON格式） | 文本 |
| difficulty | 难度等级 | 文本 |
| created_at | 创建时间 | 日期时间 |
| updated_at | 更新时间 | 日期时间 |

## API响应格式示例

```json
{
    "name": "红烧肉",
    "cook_time": "60",
    "calories": "约500千卡/100克",
    "image": "https://example.com/image.jpg",
    "description": "红烧肉色泽红亮，肥而不腻，入口即化。",
    "steps": [
        {
            "step": 1,
            "content": "将五花肉切成大小均匀的方块..."
        }
    ],
    "tools": ["炒锅", "铲子"],
    "prep_steps": [
        {
            "step": 1,
            "content": "准备五花肉500克..."
        }
    ],
    "tips": ["选择肥瘦相间的五花肉", "糖色要炒制得当"],
    "difficulty": "中等"
}
```

## 错误处理

### 常见问题及解决方案

1. **API请求失败**：
   - 检查网络连接
   - 验证API Token是否正确
   - 确认API调用次数是否超限

2. **Excel文件无法写入**：
   - 检查文件是否被其他程序占用
   - 确认data目录是否存在
   - 验证文件权限

3. **JSON解析错误**：
   - 检查API响应格式
   - 验证智能体配置是否正确

## 开发说明

### 核心模块

1. **coze_api_utils.py**：
   - `CozeAPIClient`: Coze API客户端工具类
   - `get_token(interactive=True)`: 统一的令牌获取方法
   - `get_recipe(recipe_name, interactive=True)`: 调用API获取菜谱信息
   - 支持环境变量和交互式输入两种方式获取API令牌

2. **recipe_bot_client.py**：
   - `print_recipe(recipe_data)`: 格式化打印菜谱信息
   - 使用CozeAPIClient工具类进行API调用
   - 支持交互式令牌输入

3. **recipe_to_excel.py**：
   - `save_to_excel()`: 保存数据到Excel
   - `get_last_id()`: 获取数据库中最后一个ID
   - `main()`: 主处理流程
   - 使用CozeAPIClient工具类进行API调用
   - 仅支持环境变量方式获取API令牌

### 代码架构

项目采用模块化设计：
- **工具类封装**: `CozeAPIClient`统一管理API调用和令牌获取
- **功能分离**: 单个查询和批量处理分别实现
- **配置统一**: 所有API相关配置集中在工具类中
- **错误处理**: 完善的异常处理和用户提示

### 扩展开发

如需扩展功能，可以：
- 在`CozeAPIClient`中添加新的API方法
- 扩展Excel数据库结构，添加新的数据字段
- 实现不同格式的数据导出（JSON、CSV等）
- 添加图片下载和本地存储功能
- 实现菜谱数据的去重和更新逻辑
- 添加配置文件支持（如需要更复杂的配置管理）

## 注意事项

1. **API调用频率**：请注意Coze API的调用频率限制，避免过于频繁的请求。

2. **数据备份**：建议定期备份 `data/database.xlsx` 文件。

3. **网络环境**：确保网络环境可以正常访问Coze API服务。

4. **数据质量**：生成的菜谱数据质量取决于智能体的配置和训练效果。

## 许可证

本项目基于 MIT 许可证开源，详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

---

**注意**: 请妥善保管您的API密钥，不要将其提交到版本控制系统中。