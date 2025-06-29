import os
import requests
import json

class CozeAPIClient:
    """
    Coze API客户端工具类
    统一管理API令牌获取和基本配置
    """
    
    def __init__(self):
        self.bot_id = "7487100580821893160"
        self.api_url = "https://api.coze.cn/open_api/v2/chat"
        self.token = None
    
    def get_token(self, interactive=True):
        """
        获取API令牌
        
        参数:
            interactive: 是否允许交互式输入令牌
        
        返回:
            API令牌字符串，如果获取失败返回None
        """
        if self.token:
            return self.token
        
        # 首先尝试从环境变量获取
        token = os.getenv('COZE_API_TOKEN')
        
        if token:
            self.token = token
            return token
        
        # 如果环境变量没有设置且允许交互式输入
        if interactive:
            print("未设置环境变量 COZE_API_TOKEN")
            print("您可以通过以下方式设置环境变量：")
            print("Windows PowerShell: $env:COZE_API_TOKEN='your_token_here'")
            print("Windows CMD: set COZE_API_TOKEN=your_token_here")
            print("Linux/macOS: export COZE_API_TOKEN='your_token_here'")
            print()
            
            token = input("请输入您的Coze API令牌: ").strip()
            if token:
                self.token = token
                return token
        
        # 如果不允许交互式输入或用户没有输入令牌
        if not interactive:
            print("请设置环境变量 COZE_API_TOKEN")
            print("在Windows PowerShell中设置: $env:COZE_API_TOKEN='your_token_here'")
            print("在Windows CMD中设置: set COZE_API_TOKEN=your_token_here")
            print("在Linux/macOS中设置: export COZE_API_TOKEN='your_token_here'")
        
        return None
    
    def get_recipe(self, recipe_name, interactive=True, verbose=True):
        """
        调用智能体API获取菜谱信息
        
        参数:
            recipe_name: 要查询的菜谱名称
            interactive: 是否允许交互式输入令牌
            verbose: 是否显示详细调试信息
        
        返回:
            解析后的菜谱信息
        """
        # 获取令牌
        token = self.get_token(interactive)
        if not token:
            return "无法获取API令牌" if not interactive else None
        
        # 设置请求头
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # 构造请求体
        payload = {
            "bot_id": self.bot_id,
            "user": f"user_{abs(hash(recipe_name)) % 10000000}",  # 用户标识
            "query": f"{recipe_name}",
            "stream": False
        }
        
        if verbose:
            print(f"发送请求到: {self.api_url}")
            print(f"请求体: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        
        try:
            # 发送请求
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()  # 检查请求是否成功
            
            if verbose:
                print(f"响应状态码: {response.status_code}")
            
            # 解析响应数据
            response_data = response.json()
            
            if verbose:
                print(f"完整响应数据: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
            
            # 从响应中提取消息
            messages = response_data.get('messages', [])
            
            # 查找assistant角色且type为answer的消息内容
            for message in messages:
                if message.get('role') == 'assistant' and message.get('type') == 'answer':
                    message_content = message.get('content', '')
                    
                    if verbose:
                        print(f"提取的answer内容: {message_content}")
                    
                    # 尝试解析JSON内容
                    try:
                        recipe_data = json.loads(message_content)
                        return recipe_data
                    except json.JSONDecodeError:
                        # 如果不是JSON格式，直接返回文本内容
                        return message_content
            
            return "未找到answer类型的助手回复"
            
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return f"API请求失败: {str(e)}"
        except Exception as e:
            print(f"处理响应时出错: {e}")
            return f"处理响应时出错: {str(e)}" 