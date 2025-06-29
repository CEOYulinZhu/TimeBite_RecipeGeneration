from coze_api_utils import CozeAPIClient

def print_recipe(recipe_data):
    """
    格式化打印菜谱信息
    
    参数:
        recipe_data: 菜谱数据字典
    """
    if isinstance(recipe_data, str):
        print("获取到的原始响应:")
        print(recipe_data)
        return
    
    print("\n" + "="*50)
    print(f"【菜谱名称】: {recipe_data.get('name', '未知')}")
    print(f"【烹饪时间】: {recipe_data.get('cook_time', '未知')} 分钟")
    print(f"【热量】: {recipe_data.get('calories', '未知')}")
    print(f"【难度】: {recipe_data.get('difficulty', '未知')}")
    print(f"【图片链接】: {recipe_data.get('image', '无')}")
    print("\n【菜品描述】")
    print(recipe_data.get('description', '无描述'))
    
    print("\n【烹饪步骤】")
    steps = recipe_data.get('steps', [])
    for step in steps:
        print(f"步骤 {step.get('step', '?')}: {step.get('content', '')}")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    # 创建API客户端
    client = CozeAPIClient()
    
    # 获取用户输入菜谱名称
    recipe_name = input("请输入要查询的菜谱名称: ")
    
    # 调用API获取菜谱
    recipe_data = client.get_recipe(recipe_name, interactive=True)
    
    # 打印菜谱信息
    print_recipe(recipe_data) 