"""
二次封装selenium的工具
"""


from selenium import webdriver
# 使用显示等待查找元素更好控制时间以及报错
from selenium.webdriver.support.wait import WebDriverWait
# 使用 EC模块对网页的元素是否存在进行判定
from selenium.webdriver.support import expected_conditions as EC


class Webdriver:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            options = webdriver.ChromeOptions()
            # 忽略https证书错误
            options.add_argument('--ignore-certificate-errors')
            # 忽略其他无关日志错误
            options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
            cls.__instance = webdriver.Chrome(options=options)
        return cls.__instance


class Tool:
    __instance = None       # 这个属性用来判断程序全局是否已经存在这个 class 的实例

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        """
        初始化浏览器
        """
        # if Tool.__init_flag:
        #     return
        # print("start initial the class obj")

        self.driver = Webdriver()
        # self.driver.set_window_size(1080,720)
        self.driver.maximize_window()

        # Tool.__init_flag = True


    def open_url(self, url):
        """
        打开网页
        """
        url = "http://" + url
        self.driver.maximize_window
        self.driver.get(url)

    def element_find(self, locator, timeout=5):
        """
        查找网页上单个元素
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return element
        except Exception as msg:
            print(f'该{locator}没有找到\n{msg}')

    def elements_find_list(self, locator, timeout=10):
        """寻找网络上同属性值的所有元素"""
        try:
            elements_list = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
            return elements_list
        except Exception as msg:
            print(f'该{locator}list没有找到\n{msg}')

    def send_key(self, locator=None, text=None):
        """
        输入字符
        """
        element = self.element_find(locator)
        # 输入之前清除输入框
        element.clear()
        element.send_keys(text)

    def clicks(self, locator, timeout=10):
        """点击元素"""
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()

    def quit_browser(self):
        """
        关闭浏览器
        """
        self.driver.quit()

    def refresh_windows(self):
        """
        刷新当前网页窗口
        """
        self.driver.refresh()

    def judge_element_view(self, locator, time=5):
        """
        判断元素的文本值是否可见
        可见返回元素本身
        不可见返回False
        """
        try:
            return WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(locator))
        except Exception as msg:
            print(f'{locator}该元素找不到:\n{msg}')
            return False

    def judge_element_text(self, locator, text, time=10):
        """
        获得元素的文本信息，判断是否相等
        相等就返回True
        """
        try:
            result = WebDriverWait(self.driver, time).until(EC.text_to_be_present_in_element(locator, text))
            return result
        except Exception as msg:
            result = f'该{locator}元素文本错误：\n{msg}'
            return result

    def get_web_text(self, locator, time=10):
        """ 得到网页上可见元素的文本信息 """
        try:
            text = WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(locator))
            return text.text
        except Exception as msg:
            print(f'{locator}文本不可见\n{msg}')
            return False

    def judge_element_value(self, locator=None, timeout=10, text=None):
        """判断元素的value值"""
        try:
            result = WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element_value(locator, text))
            return result
        except Exception as msg:
            print(f'该元素找不到,\n{msg}')

    def wait_element_vanish(self, locator=None, time=10):
        """
        等待元素消失
        元素消失返回false
        未消失，退出当前循环，继续循环
#### #设置时间的更改
        """
        while True:
            try:
                v = WebDriverWait(self.driver, time).until_not(EC.visibility_of_element_located(locator))
                print(f'可见元素已消失:{v}')
                break
            except:
                print('可见元素未消失')
                continue

    def get_input_text(self, locator):
        """获取输入框的文本信息"""
        text = self.judge_element_view(locator)
        return text.get_attribute('value')

    def judge_element_exist(self, element_list):
        """判断一系列元素是否存在"""
        for x in element_list:
            result = self.judge_element_view(x)
            # print(f'这是：{result}\n')
            if result is False:
                print(f'该{x}不可见')
                break
            else:
                return True

    def set_net_conditions(self, offline=False, latency=5, throughput=500 * 1024):
        """
        设置网络环境
        offline:网络状态设置，默认为Fales(不断网），True(断网）
        latency:网络延迟设置，默认5ms
        throughput:可以直接设置上下行网络速率
        """
        self.driver.set_network_conditions(offline=offline, latency=latency, throughput=throughput)

    def new_window_open(self, new_web):
        """打开新窗口"""
        new_web = "http://" + new_web
        # 创建js语句
        js = "window.open"+f'("{new_web}")'+";"
        # 执行js 语句
        self.driver.execute_script(js)

    def save_current_window(self):
        """保存当前窗口句柄"""
        # mainWindow变量保存当前窗口的句柄
        mainWindow = self.driver.current_window_handle
        return mainWindow

    def save_all_window(self):
        """储存所有窗口的句柄"""
        allHandles = self.driver.window_handles
        return allHandles

    def click_other_window(self, handle):
        """进入其他窗口"""
        self.driver.switch_to.window(handle)

    def switch_frame(self, frame_name=None):
        self.driver.switch_to.frame(frame_name)

    """综合公有方法"""
    def judge_account_state(self, account_type='Sign In / Sign up'):
        """
        判断账号是否登录
        以及账户类型
        MainElement.sidebar = 账户状态位置元组
        SideBarElement.account_state = 侧边栏位置元组
        account_type = 账户类型字符串

        """
        self.refresh_windows()
        self.clicks(MainElement.sidebar.value)
        result = self.judge_element_text(SideBarElement.account_state.value, account_type)
        if result is True:
            return True
        else:
            return False

    def sign_out(self, account_type='Sign In / Sign up'):
        """
        退出操作从主界面开始
        MainElement.sidebar: 侧边栏位置元组
        SideBarElement.account_state: 账号模块元组
        account_type = 账户类型字符串
        AccountElement.sign_out_but: 退出按钮位置元组
        AccountElement.out_ok_but: 退出确认OK弹窗位置元组
        """
        while True:
            state = self.judge_account_state(account_type)
            if state is False:
                print('执行分支')
                try:
                    self.refresh_windows()
                    print(1)
                    self.clicks(MainElement.sidebar.value)
                    print(2)
                    self.clicks(SideBarElement.account_state.value)
                    print(3)
                    self.clicks(AccountElement.sign_out_but.value)
                    print(4)
                    self.clicks(AccountElement.out_ok_but.value)
                    print(5)
                except:
                    continue
            else:
                break



